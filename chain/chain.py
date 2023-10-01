import os
from typing import List

from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain import LLMMathChain

from model.gpt4free_llm import GPT4LLM
from tool.tool import SerpstackSearch


class AlphaChain:
    llm: GPT4LLM

    def __init__(self, llm: GPT4LLM = GPT4LLM()):
        self.llm = llm

    def query(self, query, history: List[List[str]] = []):
        return self.llm.generatorAnswer(query, history)

    def math_query(self, query):
        llm_math_chain = LLMMathChain(llm=self.llm, verbose=True)
        # 创建一个功能列表，指明这个 agent 里面都有哪些可用工具，agent 执行过程可以看必知概念里的 Agent 那张图
        tools = [
            Tool(
                name="Calculator",
                func=llm_math_chain.run,
                description="useful for when you need to answer questions about math"
            )
        ]

        # 初始化 agent
        agent = initialize_agent(tools, self.llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

        try:
            return agent.run(query)
        except Exception as e:
            return str(e)

    def search_query(self, query):
        tools = [
            Tool(
                name="Search",
                func=SerpstackSearch.search,
                description="useful for when you need to answer questions about current events"
            )
        ]

        # 初始化 agent
        agent = initialize_agent(tools, self.llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
        try:
            return agent.run(query)
        except Exception as e:
            return str(e)
