import requests

from chain.chain import AlphaChain
from model.gpt4free_llm import GPT4LLM


def test_math():
    ac = AlphaChain(llm=GPT4LLM(model_name="yqcloud"))
    print(ac.math_query("杜兰特多少岁,岁数加上100是多少"))


def test_search():
    ac = AlphaChain(llm=GPT4LLM(model_name="yqcloud"))
    print(ac.search_query("中国的首都是什么"))


def test_query():
    ac = AlphaChain(llm=GPT4LLM(model_name="yqcloud"))
    for res in ac.query("中国的首都是什么", []):
        pass
    print(res.history)
    print(res.llm_output)


if __name__ == '__main__':
    # test_math()
    # test_search()
    test_query()
