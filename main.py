import json
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import geminiApi
from tools.utils import save_request_context
from typing import Union

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://bloom.staysync.co.il",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



from pydantic import BaseModel, Field, Extra


class AdditionalContext(BaseModel):
    files: list[str] = Field(default_factory=list)

    class Config:
        extra = "allow"


class LogRequest(BaseModel):
    prompt: str = "hello"
    additionalContext: dict = {}
    conversationId: str | None = None
    organizationId: Union[str, int]


@app.get("/")
def index():
    return {
        "message": "Data Logging Microservice is running. Send POST requests to /log"
    }


@app.post("/log")
async def log_incoming_data(request: Request, payload: LogRequest):
    try:
        await save_request_context(request, payload=payload)
        print(payload)
        logging.info(f"Received data body: {json.dumps(payload.dict(), indent=2)}")

        if payload.organizationId is None:
            return {
                "status": "error",
                "message": "Request body must contain organizationId",
            }, 400

        files_links = payload.additionalContext.get("files", [])
        additional_data = payload.additionalContext

        gemini_response = await geminiApi.main(
            payload.prompt,
            additional_data,
            files_links,
            payload.conversationId,
            payload.organizationId,
        )

        logging.info(f"Gemini response: {gemini_response}")

        return {
            "status": "success",
            "message": "Data and cookies received and processed",
            "gemini_response": gemini_response,
        }

    except Exception as e:
        logging.error(f"Error processing request: {e}", exc_info=True)
        return {"status": "error", "message": f"Internal server error: {e}"}, 500


@app.post("/guest")
async def guest_chat(request: Request, payload: LogRequest):
    try:
        await save_request_context(request, payload=payload)
        logging.info(f"Received data body: {json.dumps(payload.dict(), indent=2)}")

        if payload.organizationId is None:
            return {
                "status": "error",
                "message": "Request body must contain organizationId",
            }, 400

        files_links = payload.additionalContext.get("files", [])
        additional_data = payload.additionalContext

        gemini_response = await geminiApi.main(
            payload.prompt,
            additional_data,
            files_links,
            payload.conversationId,
            payload.organizationId,
            True,
        )

        logging.info(f"Gemini response: {gemini_response}")

        return {
            "status": "success",
            "message": "Data and cookies received and processed",
            "gemini_response": gemini_response,
        }

    except Exception as e:
        logging.error(f"Error processing request: {e}", exc_info=True)
        return {"status": "error", "message": f"Internal server error: {e}"}, 500


if __name__ == "__main__":
    import uvicorn

    logging.info("Starting data logging microservice on port 5000...")
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
