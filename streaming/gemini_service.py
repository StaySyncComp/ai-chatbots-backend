import os
import json
from typing import Dict, Any, AsyncGenerator, Tuple
from google.genai import types
from tools.geminiClient import client
from tools.tool_definitions.tool_definitions import house_tools
from tools.function_executor import process_function_calls
from tools.conversation_history import (
    load_conversation_history,
    save_conversation_history,
)
from tools.geminiUtils import load_schema_file, send_message_with_retry
from tools.constants import base_system_instruction
from supabaseApi import process_supabase_files
from api.organizations import fetch_organization_ai_context
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio
from api.requestsApi import request_context, RequestContext
from tools.utils import save_websocket_context

model = "gemini-2.0-flash-live-001"


async def handle_legacy_request(
    prompt: str,
    additional_context: Dict[str, Any],
    conversation_id: str,
    organization_id: Any,
) -> str:
    # existing HTTP-based geminiApi.main logic
    import geminiApi

    files = additional_context.get("files", [])
    return await geminiApi.main(
        f"כדי לענות לי...: {prompt}",
        {**additional_context, "organizationId": organization_id},
        files,
        conversation_id,
        organization_id,
    )


async def initialize_gemini_session(payload) -> Tuple[Any, str]:
    if not payload["conversationId"] or not payload["organizationId"]:
        return None
    conversation_history = load_conversation_history(
        bucket="Images", path="chats/history/" + payload["conversationId"] + ".json"
    )
    context = fetch_organization_ai_context(payload["organizationId"])
    context_data = ""
    if context and context.get("contextText"):
        print("Adding org-level context")
        context_data += f"""
        --- Organization AI Context ---
        This context is defined by the organization and should be used to inform reasoning. Do not treat it as a user prompt.

        {context['contextText']}"""

    additional_data = payload.get("additionalContext", payload)
    if additional_data:
        context_data += "\n\n--- Dynamic Instructions ---"
        if isinstance(additional_data, dict):
            for key, value in additional_data.items():
                print(f"key: {key}, value: {value}")
                context_data += f"\n- {key}: {value}"
            context_data += (
                "\nUse this information to tailor your responses and tool usage."
            )
        else:
            context_data += f"\n- {additional_data}"
    config = {
        "response_modalities": ["TEXT"],
        "tools": house_tools,
        "system_instruction": types.Content(
            parts=[
                types.Part(
                    text="You are a helpful assistant and answer in a uppercase only",
                )
            ]
        ),
    }
    return conversation_history, config, context_data


async def shutdown_gemini_session(session, conversation_id: str):
    hist = session.get_history()
    await save_conversation_history(
        chat_history=hist, bucket="Images", path=f"chats/history/{conversation_id}.json"
    )
    await session.close()


from api.requestsApi import request_context, RequestContext


async def wait_for_init(websocket: WebSocket) -> dict:
    """Waits for the first 'init' payload from frontend and saves request context"""
    # Save request context manually from websocket scope
    await save_websocket_context(websocket)

    raw_data = await websocket.receive_text()
    init_msg = json.loads(raw_data)

    if init_msg.get("type") != "init":
        raise ValueError("Expected 'init' message first")

    print("🟢 Init received:", json.dumps(init_msg, indent=2))
    return init_msg


async def start_gemini_session(websocket: WebSocket, init: dict):
    history, config, context_data = await initialize_gemini_session(init.get("payload"))
    model = init.get("model", "gemini-2.0-flash-live-001")
    tools = init.get("tools", [])
    context_path = init.get("context_path", "./system_context.txt")
    schema_text = load_schema_file("schema.txt")
    print(f"Model: {model}")
    print(f"Tools: {tools}")
    print(f"Context path: {context_path}")

    config = {
        "response_modalities": ["TEXT"],
        "tools": house_tools,
    }

    async with client.aio.live.connect(model=model, config=config) as session:
        # Load context once
        if schema_text:
            system_turn = {
                "role": "model",
                "parts": [
                    {"text": f"this is the initial context: {schema_text}"},
                    {
                        "text": "Each time you think you have to ask a question think if you can get it yourself"
                    },
                ],
            }
            await session.send_client_content(turns=[system_turn], turn_complete=False)

        # Stream user messages
        while True:
            msg = await websocket.receive_text()
            print(f"[User]: {msg}")
            await _stream_response(session, websocket, msg)


async def _stream_response(session, websocket: WebSocket, user_input: str):
    await session.send_client_content(
        turns={"role": "user", "parts": [{"text": user_input}]},
        turn_complete=True,
    )

    try:
        async for chunk in session.receive():
            if chunk.server_content:
                if chunk.text is not None:
                    await websocket.send_json({"delta": chunk.text})
                    await asyncio.sleep(0.05)

            elif chunk.tool_call:
                function_responses = await process_function_calls(
                    chunk.tool_call.function_calls
                )
                await session.send_tool_response(function_responses=function_responses)
                print("Function responses:", function_responses)
        await websocket.send_json({"done": True})
    except Exception as e:
        print(f"[Streaming error] {e}")
        await websocket.send_json({"error": str(e)})
        await websocket.send_json({"done": True})
