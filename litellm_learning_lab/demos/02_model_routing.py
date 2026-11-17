"""Demo 2: choose a LiteLLM model alias for different tasks.

Both aliases are configured in config.yaml. `local-llama` is available in the
local-only setup. `cloud-gpt` is optional and requires an OpenAI provider key
in the LiteLLM container environment.

The application does not know the upstream provider URL or credentials.
It selects a public model alias; LiteLLM resolves that alias to an upstream.
"""
import os
from openai import OpenAI
from configs import Settngs

client = OpenAI(api_key=Settngs.VIRTUAL_KEY, base_url=Settngs.BASE_URL)

def ask(model_alias: str, task: str, prompt: str) -> None:
    print(f"\n--- {task} via {model_alias} ---")
    result = client.chat.completions.create(
        model=model_alias,
        messages=[
            {"role": "system", "content": "You assist a fictional online bookstore."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )
    print(result.choices[0].message.content)

# Local-only route: works with the default config.
ask(
    # "local-llama-small-ctx",
    os.getenv("LITELLM_MODEL", "local-llama-small-ctx"),
    "Quick classification",
    "Classify this message as SHIPPING, PAYMENT, RETURN, or OTHER. "
    # "Return only the category: 'Where is my order? It has not moved for 5 days.'",
    "Return only the category: I see the amount initiated, but not credited into my acc, how long will it take?",
    # "Return only the category: Received a damaged product!",
    # "Return only the category: Need to speak with CC.",
)

# Optional cloud route: uncomment after enabling cloud-gpt in config.yaml
# and setting OPENAI_API_KEY in .env. The virtual key must be allowed to use it.
# ask(
#     "cloud-gpt",
#     "Detailed response",
#     "Draft a considerate email to a customer whose book delivery is delayed. "
#     "Offer a clear next step without promising an unverified delivery date.",
# )
