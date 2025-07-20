import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

app = FastAPI(title="MCP Server")

# Allow CORS for local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load markdown docs at startup
DOC_FILES = [
    ".kiro/steering/development-workflow.md",
    ".kiro/steering/fastapi-standards.md",
    ".kiro/steering/project-context.md",
]

def load_markdown_docs():
    docs = ""
    for path in DOC_FILES:
        if os.path.exists(path):
            with open(path, "r") as f:
                docs += f"\n---\n# {os.path.basename(path)}\n" + f.read()
    return docs

MARKDOWN_DOCS = load_markdown_docs()

class ChatRequest(BaseModel):
    question: str

@app.get("/api/docs")
async def get_api_docs():
    """Fetch OpenAPI schema from main API server."""
    async with httpx.AsyncClient() as client:
        resp = await client.get("http://localhost:8000/openapi.json")
        return resp.json()

async def get_openapi_schema():
    async with httpx.AsyncClient() as client:
        resp = await client.get("http://localhost:8000/openapi.json")
        return resp.json()

async def ask_llm(question: str, openapi_schema: dict, markdown_docs: str) -> str:
    if not client:
        return "OpenAI API key not set. Please set OPENAI_API_KEY in your .env file."
    # Prepare context for the LLM
    context = (
        "You are an expert API assistant. Answer user questions about the following API. "
        "If the user asks for an example, provide a Python requests or curl example. "
        "Be concise and accurate.\n\n"
        "API OpenAPI schema (JSON):\n" + json.dumps(openapi_schema)[:4000] +  # Truncate if too long
        "\n\nAPI Documentation (Markdown):\n" + markdown_docs[:4000]  # Truncate if too long
    )
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": question}
            ],
            max_tokens=512,
            temperature=0.2,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error contacting OpenAI: {e}"

@app.post("/api/chat")
async def chat_with_docs(req: ChatRequest):
    """Answer questions about the API using OpenAI LLM with OpenAPI schema and markdown docs as context."""
    openapi = await get_openapi_schema()
    answer = await ask_llm(req.question, openapi, MARKDOWN_DOCS)
    return {"answer": answer}

if __name__ == "__main__":
    uvicorn.run("mcp_server:app", host="0.0.0.0", port=8100, reload=True) 