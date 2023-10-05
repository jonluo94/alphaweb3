import hashlib
import json
import os
import parser

import time
import uuid
from typing import List, Optional, Dict
import pydantic
import uvicorn
from fastapi import Body, FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, BaseConfig
from starlette.staticfiles import StaticFiles

from chain.chain import AlphaChain
from model.gpt4free_llm import GPT4LLM, call_g4f_model
from util.token_util import check_token, get_token, check_token_balance, compute_token_balance

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


class DataResponse(BaseResponse):
    data: Dict = pydantic.Field(..., description="data")

    class Config:
        schema_extra = {
            "examples": {
                "data": {
                    "token": "token",
                },
            }

        }


async def openai_chat(
        authorization: Optional[str] = Header(None),
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
    # 检查token
    token = authorization.replace("Bearer ", "")
    if not check_token(token):
        return OpenaiChatMessage(code=500, msg="tokenerror")
    if not check_token_balance(token):
        return OpenaiChatMessage(code=500, msg="balance is 0")

    model = call_g4f_model()
    history_messages = messages[:-1]

    chat_history = []
    system_role = ""
    user_content = ""
    for history in history_messages:
        if history["role"] == "system":
            system_role = history["content"]
        if history["role"] == "user":
            user_content = history["content"]
        if history["role"] == "assistant":
            chat_history += [[user_content, history["content"]]]

    msg = messages[-1]
    if msg["role"] == "user":
        question = msg["content"]
        ac = AlphaChain(llm=GPT4LLM(model_name=model))
        for res in ac.query(question, chat_history, system_role):
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
        # 计算
        bal = compute_token_balance(token)
        print(token, bal)
        return rt

    return OpenaiChatMessage(code=500)


async def chat_token(
        user_name: str = Body(..., description="user_name", examples="user"),
        user_secret: str = Body(..., description="user_secret", examples="secret"),
):
    # 要加密的数据
    data = f"alphaweb3-{user_name}"

    hashed = hashlib.md5(data.encode())
    secret = hashed.hexdigest()
    # 获取哈希值
    if secret != user_secret:
        return DataResponse(msg="secreterror", data={})

    token = f"alphaweb3-{user_name}-{user_secret}"
    sha256 = hashlib.sha256()
    sha256.update(token.encode('utf-8'))
    token_value = sha256.hexdigest()
    print(user_name, secret, token_value)  # 输出哈希值

    user, balance = get_token(token_value)
    return DataResponse(data={"token": token_value, "balance": balance})


async def chat_token_balance(
        authorization: Optional[str] = Header(None),
):
    token = authorization.replace("Bearer ", "")
    user, balance = get_token(token)
    return DataResponse(data={"userName": user, "balance": balance})


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

    app.post("/v1/login", response_model=DataResponse)(chat_token)
    app.get("/v1/balance", response_model=DataResponse)(chat_token_balance)
    app.post("/v1/chat/completions", response_model=OpenaiChatMessage)(openai_chat)

    app.mount("/static", StaticFiles(directory="static"), name="static")

    uvicorn.run(app, host=host, port=port)
