import os
import mimetypes
import requests
import tempfile
import pandas as pd
from supabase import create_client
from dotenv import load_dotenv
import re
import json

load_dotenv()

# Supabase client setup
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def get_public_url(bucket: str, path: str) -> str:
    return f"{SUPABASE_URL}/storage/v1/object/public/{bucket}/{path}"


def download_supabase_file(bucket: str, path: str) -> bytes | None:
    try:
        # Construct public URL directly
        file_url = f"{SUPABASE_URL}/storage/v1/object/public/{bucket}/{path}"
        response = requests.get(file_url)
        response.raise_for_status()
        return response.content
    except Exception as e:
        print(f"❌ Failed to download file from Supabase: {e}")
        return None


def download_file_from_url(file_url: str) -> bytes | None:
    """
    Download a file directly from a full Supabase storage URL.
    Returns the file content as bytes, or None if download fails.
    """
    try:
        response = requests.get(file_url)
        response.raise_for_status()
        return response.content
    except Exception as e:
        print(f"❌ Failed to download file from URL: {e}")
        return None


def guess_file_type(file_path: str, mime_type: str = None) -> str:
    ext = os.path.splitext(file_path)[1].lower()

    if ext in [".csv"]:
        return "csv"
    if ext in [".xls", ".xlsx", ".xlsm"]:
        return "excel"
    if ext in [".json"]:
        return "json"
    if ext in [".pdf"]:
        return "pdf"
    if ext in [".txt", ".md"]:
        return "text"
    if ext in [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"]:
        return "image"

    # fallback to MIME type
    if not mime_type:
        mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type:
        return "unknown"
    if mime_type.startswith("image/"):
        return "image"
    if mime_type == "application/pdf":
        return "pdf"
    if mime_type == "application/json":
        return "json"
    if mime_type.startswith("text/"):
        return "text"

    return "unknown"


def extract_bucket_and_path_from_url(url: str):
    """
    Extract bucket and path from a Supabase public storage URL.
    """
    match = re.search(r"/storage/v1/object/public/([^/]+)/(.+)", url)
    if match:
        return match.group(1), match.group(2)
    return None, None


def delete_supabase_file(bucket: str, path: str) -> bool:
    """
    Delete a file from Supabase Storage.
    Returns True if successful, False otherwise.
    """
    try:
        result = supabase.storage.from_(bucket).remove([path])
        print(f"🗑️ Deleted file from Supabase: {bucket}/{path}")
        return True
    except Exception as e:
        print(f"❌ Failed to delete file from Supabase: {e}")
        return False


def process_supabase_files(
    file_refs: list[str], gemini_client, delete_files=True
) -> list:
    """
    Given a list of Supabase file references, return a list of Gemini-compatible message parts.

    """
    parts = []

    for link in file_refs:
        if not link:
            continue

        file_bytes = download_file_from_url(link)
        if not file_bytes:
            continue

        mime_type, _ = mimetypes.guess_type(link)
        file_type = guess_file_type(link, mime_type)

        try:
            if file_type in {"text", "json"}:
                text_content = file_bytes.decode("utf-8")
                tag = "JSON_DATA" if file_type == "json" else "TEXT"
                parts.append(f"<{tag}>\n{text_content}\n</{tag}>")
                print(f"✅ Processed {file_type.upper()} as text")

            elif file_type == "csv":
                text = file_bytes.decode("utf-8")
                parts.append(f"<CSV_DATA>\n{text}\n</CSV_DATA>")
                print(f"✅ Processed CSV file: {link}")

            elif file_type == "excel":
                with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
                    tmp.write(file_bytes)
                    tmp_path = tmp.name

                # Pandas will auto-detect engine with actual Excel files
                df = pd.read_excel(tmp_path)
                csv_like = df.to_csv(index=False)
                parts.append(f"<EXCEL_AS_CSV>\n{csv_like}\n</EXCEL_AS_CSV>")
                print(f"✅ Converted Excel to CSV format: {link}")

            elif file_type == "pdf" or file_type == "image":
                with tempfile.NamedTemporaryFile(
                    delete=False, suffix=os.path.splitext(link)[1]
                ) as tmp:
                    tmp.write(file_bytes)
                    tmp_path = tmp.name

                uploaded_file = gemini_client.files.upload(file=tmp_path)
                parts.append(uploaded_file)
                print(f"✅ Uploaded {file_type.upper()} file: {uploaded_file.name}")

            else:
                print(f"⚠️ Unsupported or unknown file type: {link}")
            bucket, path = extract_bucket_and_path_from_url(link)
            if bucket and path and delete_files:
                delete_supabase_file(bucket, path)

        except Exception as e:
            print(f"❌ Error processing {file_type} file {link}: {e}")

    return parts


def upload_json_to_supabase(data: list, bucket: str, path: str) -> bool:
    """
    Upload JSON data to Supabase Storage.
    """
    try:
        json_str = json.dumps(data, ensure_ascii=False, indent=4)
        # Delete the file if it already exists, then upload
        try:
            supabase.storage.from_(bucket).remove([path])
        except Exception:
            pass  # File may not exist — that's fine

        res = supabase.storage.from_(bucket).upload(
            path,
            json_str.encode("utf-8"),
            {"content-type": "application/json"},
        )
        print(f"✅ Uploaded JSON to Supabase at {bucket}/{path}")
        return True
    except Exception as e:
        print(f"❌ Failed to upload JSON to Supabase: {e}")
        return False
