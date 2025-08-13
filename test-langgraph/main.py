import os
import json

from typing import Annotated
from typing_extensions import TypedDict

import sentry_sdk
from sentry_sdk.integrations.langchain import LangchainIntegration

from langchain_tavily import TavilySearch
from langchain_core.messages import ToolMessage

from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.types import Command, interrupt


class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]


def main():
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN", None),
        environment=os.getenv("ENV", os.path.basename(os.getcwd())),
        traces_sample_rate=1.0,
        send_default_pii=True,
        debug=True,
        integrations=[
            LangchainIntegration(include_prompts=True),
        ],
    )

    tool = TavilySearch(max_results=2)
    tools = [tool]
    tool_node = ToolNode(tools=[tool])

    llm = init_chat_model("openai:gpt-4.1")
    llm_with_tools = llm.bind_tools(tools)

    def chatbot(state: State):
        return {"messages": [llm_with_tools.invoke(state["messages"])]}

    graph_builder = StateGraph(State)
    graph_builder.add_node("chatbot", chatbot)
    graph_builder.add_node("tools", tool_node)
    graph_builder.add_conditional_edges("chatbot", tools_condition)
    # Any time a tool is called, we return to the chatbot to decide the next step
    graph_builder.add_edge("tools", "chatbot")
    graph_builder.add_edge(START, "chatbot")
    graph_builder.add_edge("chatbot", END)

    memory = InMemorySaver()
    graph = graph_builder.compile(checkpointer=memory)

    config = {"configurable": {"thread_id": "1"}}

    # Print my graph
    print(graph.get_graph().draw_ascii())

    def stream_graph_updates(user_input: str):
        for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}, config=config):
            for value in event.values():
                print("Assistant:", value["messages"][-1].content)

    with sentry_sdk.start_transaction(name="langgraph-chat"):
        while True:
            try:
                user_input = input("User: ")
                if user_input.lower() in ["quit", "exit", "q"]:
                    print("Goodbye!")
                    break
                stream_graph_updates(user_input)
            except:
                # fallback if input() is not available
                user_input = "What do you know about LangGraph?"
                print("User: " + user_input)
                stream_graph_updates(user_input)
                break


if __name__ == "__main__":
    main()
