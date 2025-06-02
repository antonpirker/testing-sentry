import asyncio
import sys
import os
import random
from typing import Any

from pydantic import BaseModel
import sentry_sdk
from agents import Agent, AgentHooks, RunContextWrapper, Runner, Tool, function_tool, add_trace_processor

from agents.tracing.scope import Scope
from agents.tracing.processor_interface import TracingProcessor
from agents.tracing.spans import Span, TSpanData
from agents.tracing.traces import Trace

from agents.tracing.setup import TraceProvider
import agents
from agents import (
    AgentSpanData,
    CustomSpanData,
    FunctionSpanData,
    GenerationSpanData,
    GuardrailSpanData,
    HandoffSpanData,
    MCPListToolsSpanData,
    ModelSettings,
    Span,
    SpanData,
    SpeechGroupSpanData,
    SpeechSpanData,
    Trace,
    TranscriptionSpanData,

)

# class CustomAgentHooks(AgentHooks):
#     def __init__(self, display_name: str):
#         self.event_counter = 0
#         self.display_name = display_name
#         self.current_transaction = None
#         self.current_span = None

#     async def on_start(self, context: RunContextWrapper, agent: Agent) -> None:
#         self.event_counter += 1
#         print(f"### ({self.display_name}) {self.event_counter}: Agent {agent.name} started")

#     async def on_end(self, context: RunContextWrapper, agent: Agent, output: Any) -> None:
#         self.event_counter += 1
#         print(
#             f"### ({self.display_name}) {self.event_counter}: Agent {agent.name} ended with output {output}"
#         )

#     async def on_handoff(self, context: RunContextWrapper, agent: Agent, source: Agent) -> None:
#         self.event_counter += 1
#         print(
#             f"### ({self.display_name}) {self.event_counter}: Agent {source.name} handed off to {agent.name}"
#         )

#     async def on_tool_start(self, context: RunContextWrapper, agent: Agent, tool: Tool) -> None:
#         self.event_counter += 1
#         print(
#             f"### ({self.display_name}) {self.event_counter}: Agent {agent.name} started tool {tool.name}"
#         )

#     async def on_tool_end(
#         self, context: RunContextWrapper, agent: Agent, tool: Tool, result: str
#     ) -> None:
#         self.event_counter += 1
#         print(
#             f"### ({self.display_name}) {self.event_counter}: Agent {agent.name} ended tool {tool.name} with result {result}"
#         )


@function_tool
def random_number(max: int) -> int:
    """
    Generate a random number up to the provided maximum.
    """
    return random.randint(0, max)


@function_tool
def multiply_by_two(x: int) -> int:
    """Simple multiplication by two."""
    return x * 2


class FinalResult(BaseModel):
    number: int


multiply_agent = Agent(
    name="Multiply Agent",
    instructions="Multiply the number by 2 and then return the final result.",
    tools=[multiply_by_two],
    output_type=FinalResult,
    # hooks=CustomAgentHooks(display_name="Multiply Agent"),
)

start_agent = Agent(
    name="Start Agent",
    instructions="Generate a random number. If it's even, stop. If it's odd, hand off to the multiply agent.",
    tools=[random_number],
    output_type=FinalResult,
    handoffs=[multiply_agent],
    # hooks=CustomAgentHooks(display_name="Start Agent"),
)

PROMPT = (
    "You are a helpful research assistant. Given a query, come up with a set of web searches "
    "to perform to best answer the query. Output between 5 and 20 terms to query for."
)


class WebSearchItem(BaseModel):
    reason: str
    "Your reasoning for why this search is important to the query."

    query: str
    "The search term to use for the web search."


class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem]
    """A list of web searches to perform to best answer the query."""


planner_agent = Agent(
    name="PlannerAgent",
    instructions=PROMPT,
    model="gpt-4o",
    output_type=WebSearchPlan,
)

AGENTS_TO_OP = {
    "AgentSpanData": "ai.openai-agents.AgentSpanData",
    "CustomSpanData": "ai.openai-agents.CustomSpanData",
    "FunctionSpanData": "ai.openai-agents.FunctionSpanData",
    "GenerationSpanData": "ai.openai-agents.GenerationSpanData",
    "GuardrailSpanData": "ai.openai-agents.GuardrailSpanData",
    "HandoffSpanData": "ai.openai-agents.HandoffSpanData",
    "MCPListToolsSpanData": "ai.openai-agents.MCPListToolsSpanData",
    "ResponseSpanData": "ai.openai-agents.ResponseSpanData",
}
AGENTS_TO_NAME = {
    "AgentSpanData": "Agent Run Span",
    "CustomSpanData": "Custom Span",
    "FunctionSpanData": "Function Span",
    "GenerationSpanData": "Chat Completion Span",
    "GuardrailSpanData": "Guardrail Span",
    "HandoffSpanData": "Handoff Span",
    "MCPListToolsSpanData": "MCP List Tools Span",
    "ResponseSpanData": "Response Span",
}


class SentryTraceProvider:
    def __init__(self, original: TraceProvider):
        self.original = original

    def create_trace(
        self,
        name: str,
        trace_id: str | None = None,
        disabled: bool = False,
        **kwargs: Any,
    ) -> Trace:
        print(f"[SentryTraceProvider] create_trace: {name}")
        trace = self.original.create_trace(name, trace_id=trace_id, disabled=disabled, **kwargs)
        return trace

    def create_span(
        self,
        span_data: TSpanData,
        span_id: str | None = None,
        parent: Trace | Span[Any] | None = None,
        disabled: bool = False,
    ) -> Span[TSpanData]:
        print(f"[SentryTraceProvider] create_span: {span_data}")
        span = self.original.create_span(span_data, span_id, parent, disabled)

        current_span = Scope.get_current_span()
        current_trace = Scope.get_current_trace()
        # import ipdb; ipdb.set_trace()
        sentry_span = sentry_sdk.start_span(
            op=AGENTS_TO_OP[span_data.__class__.__name__],
            name=AGENTS_TO_NAME[span_data.__class__.__name__],
            attributes=span_data.export()
        )
        sentry_span.finish()
        return span

    def __getattr__(self, item: Any) -> Any:
        return getattr(self.original, item)



async def main() -> None:
    sentry_sdk.init(
        dsn=os.environ.get("SENTRY_DSN"),
        environment=os.environ.get("ENV", "test"),
        traces_sample_rate=1.0,
        send_default_pii=True,
        # debug=True,
    )

    # This will become OpenAiAgentsIntegration()
    # Monkey path trace provider of openai-agents
    name = 'GLOBAL_TRACE_PROVIDER'
    original = getattr(agents.tracing, name)
    already_wrapped = isinstance(original, SentryTraceProvider)
    if not already_wrapped:
        wrapper = SentryTraceProvider(original)
        for module_name, mod in sys.modules.items():
            if module_name.startswith('agents'):
                try:
                    if getattr(mod, name, None) is original:
                        setattr(mod, name, wrapper)
                except Exception:  # pragma: no cover
                    pass


    with sentry_sdk.start_span(name="main"):
        # await Runner.run(
        #     planner_agent,
        #     input="Whats the best snowboard?",
        # )
        # import ipdb; ipdb.set_trace()
        user_input = input("Enter a max number: ")
        await Runner.run(
            start_agent,
            input=f"Generate a random number between 0 and {user_input}.",
        )

    print("Done!")


if __name__ == "__main__":
    asyncio.run(main())
