import asyncio
import os

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

import sentry_sdk
from sentry_sdk.ai.monitoring import ai_track
from sentry_sdk.integrations.langchain import LangchainIntegration


@ai_track("My async LangChain AI pipeline")
async def my_pipeline(llm):    
    with sentry_sdk.start_transaction(name="langchain-async"):
        # Async create message
        messages = [
            SystemMessage(content="You are a helpful assistant."),
            HumanMessage(content="Hi!"),
        ]
        response = await llm.ainvoke(messages)
        print("Response:")
        print(response.dict())

        # Async create streaming message
        print("Response (Stream):")
        async for chunk in llm.astream(messages):
            print(chunk.dict())


async def main():
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

    import random
    models = ["gpt-3.5-turbo", "gpt-4o-mini"]
    selected_model = random.choice(models)
    llm = ChatOpenAI(
        model=selected_model,
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    await my_pipeline(llm)    


asyncio.run(main())