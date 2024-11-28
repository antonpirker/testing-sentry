import os

import sentry_sdk


def main():
    sentry_sdk.init(
        dsn=os.environ["SENTRY_DSN"],
        enable_tracing=True,
        debug=True,
    )

    pipeline_name = "My AI pipeline"

    with sentry_sdk.start_span(op="main"):  # thats the transaction created by FastAPI (or other framework)
        with sentry_sdk.start_span(op="ai.pipeline", name=pipeline_name):
            with sentry_sdk.start_span(op="some-other-span"):  # simulating span from other integrations.
                for i in range(5):
                    with sentry_sdk.start_span(op="ai.chat_completions.create.openai", name="My Chat completion") as span:
                        span.set_data("ai.input_messages", ["Hello, how are you?"])
                        span.set_data("ai.model_id", "ai-007")
                        span.set_data("ai.streaming", True)
                        span.set_data("ai.responses", ["I'm fine", "Thank you!"])
                        span.set_data("ai.pipeline.name", pipeline_name)

                        span.set_measurement("ai_completion_tokens_used", 7)
                        span.set_measurement("ai_prompt_tokens_used", 6)
                        span.set_measurement("ai_total_tokens_used", 13)


if __name__ == "__main__":
    main()