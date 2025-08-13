import os

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain.agents import AgentExecutor, create_openai_tools_agent


import sentry_sdk
from sentry_sdk.ai.monitoring import ai_track
from sentry_sdk.integrations.langchain import LangchainIntegration
from sentry_sdk.integrations.openai import OpenAIIntegration


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

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant that can use tools to help answer questions."),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    agent = create_openai_tools_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    with sentry_sdk.start_transaction(name="langchain-sync"):
        res = agent_executor.invoke({"input": "What is 12 * 13? Use the tool."})
        print(res["output"])


if __name__ == "__main__":
    main()
