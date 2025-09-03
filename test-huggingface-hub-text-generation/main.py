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
        try:
            print(f"🔄 Test: Generating text for '{prompt}'")

            # Use the real InferenceClient with local server
            response = client.text_generation(
                prompt,
                max_new_tokens=40,
                temperature=0.7,
                do_sample=True,
            )

            print("✅ Success!")
            print(f"   Prompt: {prompt}")
            print(f"   Generated: {response}")
            print()

        except Exception as e:
            print(f"❌ Failed: {type(e).__name__}: {e}")
            print("💡 Make sure the local server is running:")
            print("   ./run_server.sh")
            print()


if __name__ == "__main__":
    main()
