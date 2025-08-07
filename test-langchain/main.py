import os

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

import sentry_sdk
from sentry_sdk.ai.monitoring import ai_track
from sentry_sdk.integrations.langchain import LangchainIntegration


@ai_track("My sync LangChain AI pipeline")
def my_pipeline(llm):    
    with sentry_sdk.start_transaction(name="langchain-sync"):
        # Sync create message
        messages = [
            SystemMessage(content="You are a helpful assistant."),
            HumanMessage(content="Hi!"),
        ]
        response = llm.invoke(messages)
        print("Response:")
        print(response.dict())

        # Sync create streaming message
        print("Response (Stream):")
        for chunk in llm.stream(messages):
            print(chunk.dict())


def main():
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN", None),
        environment=os.getenv("ENV", "local"),
        traces_sample_rate=1.0,
        send_default_pii=True,
        debug=True,
        integrations=[
            LangchainIntegration(include_prompts=True), 
        ],
    )

    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    my_pipeline(llm)    


if __name__ == "__main__":
    main()