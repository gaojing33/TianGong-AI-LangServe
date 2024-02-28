import os
from dotenv import load_dotenv
from fastapi import Body, Depends, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from langchain_openai import ChatOpenAI
from langserve import add_routes
from pydantic import BaseModel, validator
from src.agents.agent import openai_agent
from src.agents.automobile_esg_agent import auto_esg_agent

load_dotenv()

bearer_scheme = HTTPBearer()
BEARER_TOKEN = os.environ.get("BEARER_TOKEN")
assert BEARER_TOKEN is not None


def validate_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    if credentials.scheme != "Bearer" or credentials.credentials != BEARER_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    return credentials


class InputModel(BaseModel):
    input: str

    @validator("input")
    def check_input(cls, v):
        if not isinstance(v, str):
            raise ValueError("input must be a string")
        return v


class OutputModel(BaseModel):
    output: str

    @validator("output")
    def check_input(cls, v):
        if not isinstance(v, str):
            raise ValueError("output must be a string")
        return v


app = FastAPI(
    title="TianGong AI Server",
    version="1.0",
    description="TianGong AI API Server",
    dependencies=[Depends(validate_token)],
)

model = ChatOpenAI(
    model="gpt-4-turbo-preview",
    temperature=0,
    streaming=True,
)

add_routes(
    app,
    model,
    path="/openai",
)

add_routes(
    app,
    openai_agent(),
    path="/openai_agent",
    input_type=InputModel,
    output_type=OutputModel,
)

add_routes(
    app,
    auto_esg_agent(),
    path="/automobile_esg_agent",
    input_type=InputModel,
    output_type=OutputModel,
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
