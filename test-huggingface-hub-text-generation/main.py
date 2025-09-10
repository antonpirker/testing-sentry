import os

import sentry_sdk
from sentry_sdk.integrations.huggingface_hub import HuggingfaceHubIntegration

from huggingface_hub import InferenceClient


def main():
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN", None),
        environment=os.getenv("ENV", "local"),
        traces_sample_rate=1.0,
        send_default_pii=True,
        debug=True,
        integrations=[
            HuggingfaceHubIntegration(include_prompts=True),
        ],
    )

    # Connect to local text generation server
    local_server_url = "http://localhost:8000"

    print(f"🔄 Connecting to local server: {local_server_url}")
    print("📝 Make sure to start the local server first:")
    print("   ./run_server.sh")
    print()

    with sentry_sdk.start_transaction(name="huggingface-hub-text-generation"):
        client = InferenceClient(model=local_server_url)

        prompt = "The sky is"
        import ipdb; ipdb.set_trace()
        response = list(client.text_generation(
            prompt,
            max_new_tokens=40,
            temperature=0.7,
            do_sample=True,
            details=True,
            stream=True,
        ))
        print(response)

if __name__ == "__main__":
    main()
