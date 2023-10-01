import json
import parser

import time
import uuid
from typing import List, Optional, Dict
import pydantic
import uvicorn
from fastapi import Body, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, BaseConfig
from starlette.staticfiles import StaticFiles

from chain.chain import AlphaChain
from model.gpt4free_llm import GPT4LLM

BaseConfig.arbitrary_types_allowed = True

class BaseResponse(BaseModel):
    code: int = pydantic.Field(200, description="HTTP status code")
    msg: str = pydantic.Field("success", description="HTTP status message")

    class Config:
        schema_extra = {
            "examples": {
                "code": 200,
                "msg": "success",
            }
        }


class OpenaiMessage:
    role: str = pydantic.Field(..., description="role")
    content: str = pydantic.Field(..., description="content")

    def __init__(self, role: str, content: str) -> None:
        self.role = role
        self.content = content


class OpenaiChatChoice:
    finish_reason: str
    index: int
    message: OpenaiMessage

    def __init__(self, finish_reason: str, index: int, message: OpenaiMessage) -> None:
        self.finish_reason = finish_reason
        self.index = index
        self.message = message


class OpenaiChatMessage(BaseResponse):
    id: str = pydantic.Field(..., description="id")
    object: str = pydantic.Field(default="chat.completion", description="object")
    model: str = pydantic.Field(..., description="model")
    created: int = pydantic.Field(..., description="created")
    choices: List[OpenaiChatChoice] = pydantic.Field(..., description="choices")
    usage: Dict = pydantic.Field(..., description="usage")

    class Config:
        schema_extra = {
            "examples": {
                "id": "chatcmpl-7QyqpwdfhqwajicIEznoc6Q47XAyW",
                "object": "chat.completion",
                "choices": [
                    {
                        "finish_reason": "stop",
                        "index": 0,
                        "message": {
                            "content": "The 2020 World Series was played in Texas at Globe Life Field in Arlington.",
                            "role": "assistant"
                        }
                    }
                ],
                "created": 1677664795,
                "model": "gpt-3.5-turbo-0613",
                "usage": {
                    "completion_tokens": 17,
                    "prompt_tokens": 57,
                    "total_tokens": 74
                }
            }
        }


class OpenaiModelData:
    id: str
    object: str
    created: int
    owned_by: str

    def __init__(self, id: str, object: str, created: int, owned_by: str) -> None:
        self.id = id
        self.object = object
        self.created = created
        self.owned_by = owned_by


class OpenaiDataResponse(BaseResponse):
    object: str = pydantic.Field(default="list", description="object")
    data: List[OpenaiModelData] = pydantic.Field(
        default=[
            OpenaiModelData("deepai", "model", 1686935002, "organization-owner"),
            OpenaiModelData("yqcloud", "model", 1686935002, "organization-owner"),
            OpenaiModelData("gptgo", "model", 1686935002, "organization-owner"),
            OpenaiModelData("aivvm", "model", 1686935002, "organization-owner"),
        ], description="data")

    class Config:
        schema_extra = {
            "examples": {
                "object": "list",
                "data": [
                    {
                        "id": "model-id-0",
                        "object": "model",
                        "created": 1686935002,
                        "owned_by": "organization-owner"
                    },
                    {
                        "id": "model-id-1",
                        "object": "model",
                        "created": 1686935002,
                        "owned_by": "organization-owner",
                    },
                    {
                        "id": "model-id-2",
                        "object": "model",
                        "created": 1686935002,
                        "owned_by": "openai"
                    },
                ],
            }

        }


async def openai_chat(
        model: str = Body(default="yqcloud", description="LLM", examples="yqcloud"),
        messages: List[Dict] = Body(
            None,
            description="questions and answers",
            examples=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Who won the world series in 2020?"},
            ],
        ),
):
    history_messages = messages[:-1]
    chat_history = []
    temp_history = ["", ""]
    for history in history_messages:
        if history["role"] == "user":
            temp_history[0] = history["content"]
        if history["role"] == "assistant":
            temp_history[1] = history["content"]
            chat_history += [temp_history]

    msg = messages[-1]
    if msg["role"] == "user":
        question = msg["content"]
        ac = AlphaChain(llm=GPT4LLM(model_name=model))
        for res in ac.query(question, chat_history):
            pass
        print(res.history)
        resp = res.llm_output["answer"]

        rt = OpenaiChatMessage(
            id=uuid.uuid4().hex,
            model=model,
            created=time.time(),
            choices=[OpenaiChatChoice(
                finish_reason="stop",
                index=0,
                message=OpenaiMessage(role="assistant", content=resp)
            )],
            usage={
                "completion_tokens": 10,
                "prompt_tokens": 20,
                "total_tokens": 30
            },
        )
        return rt

    return BaseResponse(code=500)


async def openai_models():
    return OpenaiDataResponse()


def api_start(host, port):
    global app

    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.post("/v1/chat/completions", response_model=OpenaiChatMessage)(openai_chat)
    app.get("/v1/models", response_model=OpenaiDataResponse)(openai_models)

    app.mount("/static", StaticFiles(directory="static"), name="static")

    uvicorn.run(app, host=host, port=port)


