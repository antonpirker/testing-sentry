import os

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

import sentry_sdk
from sentry_sdk.ai.monitoring import ai_track
from sentry_sdk.integrations.langchain import LangchainIntegration
from sentry_sdk.integrations.openai import OpenAIIntegration


from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_tools_agent

@tool
def multiply(a: int, b: int) -> int:
    "Multiply two integers."
    return a * b


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
        disabled_integrations=[
            OpenAIIntegration(),
        ],
    )

    tools = [multiply]
    llm = ChatOpenAI(model="gpt-4o-mini")
    prompt = hub.pull("hwchase17/openai-tools-agent")  # ReAct-style prompt
    agent = create_openai_tools_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools)

    with sentry_sdk.start_transaction(name="langchain-sync"):
        res = agent_executor.invoke({"input": "What is 12 * 13? Use the tool."})
        print(res["output"])


if __name__ == "__main__":
    main()
