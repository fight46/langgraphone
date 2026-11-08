import os
from typing import Annotated, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import AnyMessage, HumanMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages

# 自动读取同目录 .env 文件中的环境变量
load_dotenv()

from langchain_openai import ChatOpenAI


# 定义图的状态：节点间共享的数据结构
class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


# 初始化大模型（DeepSeek 官方 OpenAI 兼容接口）
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1",
    temperature=0.7,
)


# 核心节点：调用大模型生成回答
def call_llm(state: State) -> State:
    result = llm.invoke(state["messages"])
    return {"messages": [result]}


# 搭建 LangGraph 工作流
workflow = StateGraph(State)
workflow.add_node("llm_node", call_llm)
workflow.add_edge(START, "llm_node")
workflow.add_edge("llm_node", END)
graph = workflow.compile()


# 程序入口
if __name__ == "__main__":
    messages: list[AnyMessage] = []
    while True:
        user_question = input("你：").strip()
        if user_question.lower() in {"exit", "quit", "q"}:
            print("对话结束。")
            break
        if not user_question:
            continue

        messages.append(HumanMessage(content=user_question))
        output = graph.invoke({"messages": messages})
        messages = output["messages"]
        print(f"AI：{messages[-1].content}\n")
