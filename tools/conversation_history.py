import os
import json
from tools.tool_helpers import dict_to_part, part_to_dict
from google.genai import types
from supabaseApi import upload_json_to_supabase, download_supabase_file

CONVERSATION_HISTORY_FILE = "conversation_history_2.json"


def load_conversation_history(bucket="Images", path="history.json") -> list:
    try:
        file_bytes = download_supabase_file(bucket, path)

        if not file_bytes:
            print("❌ No conversation history found")
            return []

        history_data = json.loads(file_bytes.decode("utf-8"))
        history_contents = []

        for turn in history_data:
            role = turn.get("role")
            parts = [dict_to_part(part) for part in turn.get("parts", [])]
            if role and parts:
                history_contents.append(types.Content(role=role, parts=parts))
        return history_contents
    except Exception as e:
        print(f"❌ Failed to load conversation history: {e}")
        return []


def save_conversation_history(chat_history, bucket="Images", path="history.json"):
    history_data = []
    for content in chat_history:
        history_data.append(
            {
                "role": content.role,
                "parts": [part_to_dict(part) for part in content.parts],
            }
        )
    upload_json_to_supabase(history_data, bucket, path)
