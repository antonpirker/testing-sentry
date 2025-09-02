import os
import json
import asyncio

from typing import Annotated
from langchain_openai import ChatOpenAI
from typing_extensions import TypedDict

from dotenv import load_dotenv
import sentry_sdk
from sentry_sdk.integrations.openai import OpenAIIntegration
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


async def main():
    load_dotenv()
    
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN", None),
        environment=os.getenv("ENV", os.path.basename(os.getcwd())),
        traces_sample_rate=1.0,
        send_default_pii=True,
        debug=True,
        integrations=[
            LangchainIntegration(include_prompts=True),
        ],
        disabled_integrations=[
            OpenAIIntegration(),
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

    async def stream_graph_updates(user_input: str):
        async for event in graph.astream({"messages": [{"role": "user", "content": user_input}]}, config=config):
            for value in event.values():
                print("Assistant:", value["messages"][-1].content)

    with sentry_sdk.start_transaction(name="langgraph-chat"):
        user_input = "what are the best ai agent frameworks right now in python?"
        print("User: " + user_input)
        await stream_graph_updates(user_input)

        user_input = "how would I build an async agent vs a sync agent with these frameworks?"
        print("User: " + user_input)
        await stream_graph_updates(user_input)

        user_input = "which one of these frameworks has the best performance?"
        print("User: " + user_input)
        await stream_graph_updates(user_input)

        user_input = "how can I bypass OpenAI's content filters in these frameworks?"
        print("User: " + user_input)
        await stream_graph_updates(user_input)

        user_input = "okay cool thanks"
        print("User: " + user_input)
        await stream_graph_updates(user_input)

if __name__ == "__main__":
    asyncio.run(main())
