import asyncio
import random
from abc import ABC
from typing import Optional, List
import g4f
from langchain.llms.base import LLM
from langchain.llms.utils import enforce_stop_tokens

import nest_asyncio

nest_asyncio.apply()
loop = asyncio.get_event_loop()


class AnswerResult:
    """消息实体"""
    history: List[List[str]] = []
    llm_output: Optional[dict] = None


def call_g4f_model():
    my_list = ["gptgo", "chatbase"]
    random_value = random.choice(my_list)
    print("call_g4f_model", random_value)
    return random_value


def call_g4f_provider(model: str, messages: []):
    response: str
    try:

        if model == "you":
            provider = g4f.Provider.You
            response = loop.run_until_complete(provider.create_async(
                model="gpt-3.5-turbo",
                messages=messages,
            ))
        if model == "chatbase":
            provider = g4f.Provider.ChatBase
            response = loop.run_until_complete(provider.create_async(
                model="gpt-3.5-turbo",
                messages=messages,
            ))
        if model == "bing":
            provider = g4f.Provider.Bing
            response = loop.run_until_complete(provider.create_async(
                model="gpt-3.5-turbo",
                messages=messages,
            ))
        if model == "gptgo":
            provider = g4f.Provider.GptGo
            response = loop.run_until_complete(provider.create_async(
                model="gpt-3.5-turbo",
                messages=messages,
            ))

        if model == "chatgptai":
            response = g4f.ChatCompletion.create(model="gpt-3.5-turbo",
                                                 provider=g4f.Provider.ChatgptAi,
                                                 messages=messages,
                                                 stream=False, )
        if model == "aivvm":
            response = g4f.ChatCompletion.create(model="gpt-3.5-turbo",
                                                 provider=g4f.Provider.Aivvm,
                                                 messages=messages,
                                                 stream=False, )
        if model == "vitalentum":
            response = g4f.ChatCompletion.create(model="gpt-3.5-turbo",
                                                 provider=g4f.Provider.Vitalentum,
                                                 messages=messages,
                                                 stream=False, )

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
