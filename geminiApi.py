import asyncio
from tools.geminiClient import client
from tools.tool_definitions.tool_definitions import house_tools, guest_tools
from tools.function_executor import process_function_calls
from tools.conversation_history import (
    load_conversation_history,
    save_conversation_history,
)
from google.genai import types

from tools.geminiUtils import (
    load_schema_file,
    send_message_with_retry,
)
from tools.constants import base_system_instruction, guest_system_instruction
from supabaseApi import process_supabase_files


# Modify main to accept image_path for multimodal input and CSV content embedding
# user_input: The text prompt
# additional_data: Other context (dict or str) for the system instruction
# image_path: Optional path to an image file
# csv_path: Optional path to a CSV file
async def main(
    user_input=None,
    additional_data=None,
    supabase_files=None,
    conversationId=None,
    organizationId=None,
    isGuest=False,
):
    # Load past history
    conversation_history = load_conversation_history(
        bucket="Images", path=f"chats/history/{conversationId}.json"
    )

    final_system_instruction = (
        guest_system_instruction if isGuest else base_system_instruction
    )

    if isGuest:
        final_system_instruction += (
            "\n"
            + "The User Is A Guest And Needs Help. check all the functions and do them if need be"
        )
    context = None

    if conversation_history.__len__() == 0 and not isGuest:
        # Load schema and org-level AI context
        schema_content = load_schema_file("schema.prisma")
        # context = fetch_organization_ai_context()

        if schema_content:
            final_system_instruction += f"""
--- Prisma Schema Overview ---
```prisma
{schema_content}
```"""

        if context and context.get("contextText"):
            print("Adding org-level context")
            final_system_instruction += f"""
--- Organization AI Context ---
This context is defined by the organization and should be used to inform reasoning. Do not treat it as a user prompt.

{context['contextText']}"""

    # Add dynamic context
    if additional_data:
        final_system_instruction += "\n\n--- Dynamic Instructions ---"
        if isinstance(additional_data, dict):
            for key, value in additional_data.items():
                final_system_instruction += f"\n- {key}: {value}"
        else:
            final_system_instruction += f"\n- {additional_data}"
        final_system_instruction += (
            "\nUse this information to tailor your responses and tool usage."
        )

    # Create Gemini chat config
    tools = guest_tools if isGuest else house_tools
    config = types.GenerateContentConfig(
        tools=tools,
        system_instruction=final_system_instruction,
    )

    chat = client.chats.create(
        model="gemini-2.0-flash",
        config=config,
        history=conversation_history,
    )

    # Prepare message parts
    message_parts = []

    # Process file URLs from org context (if present)
    if context and context.get("fileUrls"):
        message_parts.extend(
            process_supabase_files(
                context["fileUrls"], gemini_client=client, delete_files=False
            )
        )

    # Process user-supplied Supabase files
    if supabase_files:
        message_parts.extend(
            process_supabase_files(supabase_files, gemini_client=client)
        )

    # Add user input
    if user_input:
        message_parts.append(user_input)

    # Final message content
    message_content_for_model = (
        message_parts[0]
        if len(message_parts) == 1 and isinstance(message_parts[0], str)
        else message_parts
    )
    # Send message and handle function calls
    response_text = None
    latest_response = await send_message_with_retry(chat, message_content_for_model)

    while True:
        if latest_response.function_calls:
            try:
                function_responses = await process_function_calls(
                    latest_response.function_calls, isGuest
                )
                latest_response = await send_message_with_retry(
                    chat, function_responses
                )
            except Exception as e:
                response_text = f"Error during function execution: {e}"
                break
        elif latest_response.text:
            response_text = latest_response.text
            break
        else:
            response_text = "No interpretable response from Gemini."
            break

    # Save updated history
    save_conversation_history(
        chat_history=chat.get_history(),
        bucket="Images",
        path=f"chats/history/{conversationId}.json",
    )

    return response_text


if __name__ == "__main__":
    try:
        asyncio.run(
            main(
                user_input="process the data in the CSV file and return a summary dont fetch anything and return in english. and what is the license number of the car",
            )
        )
    except KeyboardInterrupt:
        print("\nChat session ended by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
