from openai import OpenAI, APIStatusError
from configs import Settngs

# Each key has its own permissions configured in LiteLLM.
keys = {
    "basic": Settngs.BOOKSTORE_BASIC_KEY,
    "pro": Settngs.BOOKSTORE_PRO_KEY,
}

models = [
    "local-llama-small-ctx",
    "local-llama-large-ctx"
]


def create_client(api_key):
    return OpenAI(api_key=api_key, base_url=Settngs.BASE_URL)


def test_access(key_name, api_key, model):
    client = create_client(api_key)

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": "Give one short customer-service tip for a bookstore."
                }
            ],
            max_tokens=80,
        )

        print(f"  [ALLOWED] {key_name} -> {model}")
        print(f"  Response: {response.choices[0].message.content}")

    except APIStatusError as exc:
        print(f"  [DENIED]  {key_name} -> {model}")
        print(f"  HTTP status: {exc.status_code}")
        print(f"  Details: {exc.message}")

    except Exception as exc:
        print(f"  [ERROR]   {key_name} -> {model}")
        print(f"  {type(exc).__name__}: {exc}")


for key_name, api_key in keys.items():
    print(f"\nTesting {key_name.upper()} key")

    for model in models:
        test_access(key_name, api_key, model)
