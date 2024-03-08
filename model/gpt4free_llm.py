import asyncio
import random
from abc import ABC
from typing import Optional, List
import g4f
from g4f.client import Client
from langchain.llms.base import LLM
from langchain.llms.utils import enforce_stop_tokens

import nest_asyncio

nest_asyncio.apply()


class AnswerResult:
    """消息实体"""
    history: List[List[str]] = []
    llm_output: Optional[dict] = None


def call_g4f_model(model: str):
    my_list = ["gpt-4", "claude-v2", "dolphin-mixtral-8x7b", "airoboros-l2-70b"]
    if model in my_list:
        random_value = random.choice(my_list)
    else:
        random_value = my_list[0]
    print("call_g4f_model", random_value)
    return random_value


def call_g4f_provider(model: str, messages: []):
    response: str
    try:
        client = Client()
        res = client.chat.completions.create(
            model=model,
            messages=messages,
        )
        response = res.choices[0].message.content
        print(model, res.choices[0].message.content)

    except Exception as e:
        response = f"{model}:{e}"
        print(f"{model}:错误", e)

    return response


class GPT4LLM(LLM, ABC):
    history_len: int = 5
    model_name: str = None

    def __init__(self, model_name: str = "deepai"):
        super().__init__()
        self.model_name = model_name

    @property
    def _llm_type(self) -> str:
        return "GPT4LLM"

    @property
    def _history_len(self) -> int:
        return self.history_len

    def set_history_len(self, history_len: int = 5) -> None:
        self.history_len = history_len

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        print(f"\n<GPT4LLM 问题>:\n{prompt}")
        print(f"------------------------------------------")
        # create a chat completion
        response = call_g4f_provider(self.model_name,
                                     messages=[{"role": "user", "content": prompt}])

        if stop is not None:
            response = enforce_stop_tokens(response, stop)
        print(f"\n<GPT4LLM 回答>:\n{response}")
        print(f"==========================================")
        return response

    def generatorAnswer(self, prompt: str,
                        history: List[List[str]] = [],
                        system_role: str = ""):
        print(f"GPT4LLM generatorAnswer:{prompt}")
        chat_history = [{"role": "system", "content": system_role}]
        for hist in history[-self.history_len:-1] if self.history_len > 0 else []:
            question = hist[0] if hist[0] is not None else ""
            answer = hist[1] if hist[1] is not None else ""
            chat_history.append({"role": "user", "content": question})
            chat_history.append({"role": "assistant", "content": answer})
        # create a chat completion
        chat_history.append({"role": "user", "content": prompt})

        response = call_g4f_provider(self.model_name, messages=chat_history)
        answer_result = AnswerResult()
        history += [[prompt, response]]
        answer_result.history = history
        answer_result.llm_output = {"answer": response}
        print(f"response:{response}")
        print(f"+++++++++++++++++++++++++++++++++++")
        yield answer_result
