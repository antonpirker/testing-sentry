import os
import time
from typing import Annotated

import sentry_sdk
from sentry_sdk.integrations.langchain import LangchainIntegration
from sentry_sdk.integrations.langgraph import LanggraphIntegration
from sentry_sdk.integrations.openai import OpenAIIntegration

from dotenv import load_dotenv

from langchain_core.messages import convert_to_messages
from langchain_core.tools import tool, InjectedToolCallId
from langgraph.prebuilt import create_react_agent, InjectedState
from langgraph.graph import StateGraph, START, MessagesState
from langgraph.types import Command


# We'll use `pretty_print_messages` helper to render the streamed agent outputs nicely

def init_sentry():
    sentry_sdk.init(
        dsn=os.environ.get("SENTRY_DSN"),
        environment=os.environ.get("ENV", "test"),
        traces_sample_rate=1.0,
        send_default_pii=True,
        debug=True,
        integrations=[
            LangchainIntegration(include_prompts=True),
            LanggraphIntegration(include_prompts=True),
        ],
        disabled_integrations=[OpenAIIntegration()]
    )

def pretty_print_message(message, indent=False):
    pretty_message = message.pretty_repr(html=True)
    if not indent:
        print(pretty_message)
        return

    indented = "\n".join("\t" + c for c in pretty_message.split("\n"))
    print(indented)


def pretty_print_messages(update, last_message=False):
    is_subgraph = False
    if isinstance(update, tuple):
        ns, update = update
        # skip parent graph updates in the printouts
        if len(ns) == 0:
            return

        graph_id = ns[-1].split(":")[0]
        print(f"Update from subgraph {graph_id}:")
        print("\n")
        is_subgraph = True

    for node_name, node_update in update.items():
        update_label = f"Update from node {node_name}:"
        if is_subgraph:
            update_label = "\t" + update_label

        print(update_label)
        print("\n")

        messages = convert_to_messages(node_update["messages"])
        if last_message:
            messages = messages[-1:]

        for m in messages:
            pretty_print_message(m, indent=is_subgraph)
        print("\n")


def create_handoff_tool(*, agent_name: str, description: str | None = None):
    name = f"transfer_to_{agent_name}"
    description = description or f"Transfer to {agent_name}"

    @tool(name, description=description)
    def handoff_tool(
        state: Annotated[MessagesState, InjectedState], 
        tool_call_id: Annotated[str, InjectedToolCallId],
    ) -> Command:
        tool_message = {
            "role": "tool",
            "content": f"Successfully transferred to {agent_name}",
            "name": name,
            "tool_call_id": tool_call_id,
        }
        return Command(  
            goto=agent_name,  
            update={"messages": state["messages"] + [tool_message]},  
            graph=Command.PARENT,  
        )
    return handoff_tool

# Handoffs
transfer_to_hotel_assistant = create_handoff_tool(
    agent_name="hotel_assistant",
    description="Transfer user to the hotel-booking assistant.",
)
transfer_to_flight_assistant = create_handoff_tool(
    agent_name="flight_assistant",
    description="Transfer user to the flight-booking assistant.",
)

# Simple agent tools
def book_hotel(hotel_name: str):
    """Book a hotel"""
    return f"Successfully booked a stay at {hotel_name}."

def book_flight(from_airport: str, to_airport: str):
    """Book a flight"""
    return f"Successfully booked a flight from {from_airport} to {to_airport}."

def create_agents():
    flight_assistant = create_react_agent(
        model="openai:gpt-3.5-turbo",
        tools=[book_flight, transfer_to_hotel_assistant],
        prompt="You are a flight booking assistant",
        name="flight_assistant"
    )
    hotel_assistant = create_react_agent(
        model="openai:gpt-3.5-turbo",
        tools=[book_hotel, transfer_to_flight_assistant],
        prompt="You are a hotel booking assistant",
        name="hotel_assistant"
    )
    return flight_assistant, hotel_assistant

def create_multi_agent_graph(flight_assistant, hotel_assistant):
    return (
        StateGraph(MessagesState)
        .add_node(flight_assistant)
        .add_node(hotel_assistant)
        .add_edge(START, "flight_assistant")
        .compile()
    )

def main():
    load_dotenv()
    init_sentry()
    with sentry_sdk.start_transaction(name="multi_agent_booking", op="langgraph"):
        flight_assistant, hotel_assistant = create_agents()
        multi_agent_graph = create_multi_agent_graph(flight_assistant, hotel_assistant)
        
        user_request = "book a flight from BOS to JFK and a stay at McKittrick Hotel"
        sentry_sdk.set_context("user_request", {
            "content": user_request,
            "request_type": "booking",
            "entities": ["flight", "hotel"]
        })
        

        for chunk in multi_agent_graph.stream(
            {
                "messages": [
                    {
                        "role": "user", 
                        "content": user_request
                    }
                ]
            },
            subgraphs=True
        ):
            pretty_print_messages(chunk)

if __name__ == "__main__":
    main()
    time.sleep(1)