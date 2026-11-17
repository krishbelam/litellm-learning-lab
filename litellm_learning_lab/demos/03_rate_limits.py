"""Demo 3: observe a LiteLLM virtual-key rate limit.

Before running:
1. Create a dedicated test virtual key in LiteLLM.
2. Restrict it to `local-llama`.
3. Set a low requests-per-minute (RPM) limit on that key or its test team.
4. Export that virtual key as LITELLM_VIRTUAL_KEY.

The script deliberately sends concurrent requests. A 429 response is an
expected learning outcome only when the configured limit is reached. Depending
on the proxy version and configuration, the exact exception text can differ.
"""
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from openai import OpenAI, RateLimitError, APIError
from configs import Settngs

client = OpenAI(api_key=Settngs.VIRTUAL_KEY, base_url=Settngs.BASE_URL)


def make_request(number: int) -> str:
    try:
        req = f"Tip number {number}:- Give one short bookstore customer-service tip."
        response = client.chat.completions.create(
            model=Settngs.MODEL,
            messages=[
                {
                    "role": "user",
                    "content": req
                }
            ],
            max_tokens=80,
        )
        return f"------------ Request {number} @ {req} \n Response: {response.choices[0].message.content}"

    except RateLimitError as exc:
        return f"Request {number}: RATE LIMITED (HTTP 429) — {exc}"
    except APIError as exc:
        return f"Request {number}: API ERROR — {exc}"
    except Exception as exc:
        return f"Request {number}: UNEXPECTED ERROR — {type(exc).__name__}: {exc}"


print(
    f"Sending {Settngs.REQUEST_COUNT} requests with {Settngs.MAX_WORKERS} workers "
    f"through {Settngs.BASE_URL} using model alias {Settngs.MODEL!r}."
)

with ThreadPoolExecutor(max_workers=Settngs.MAX_WORKERS) as pool:
    futures = [pool.submit(make_request, i) for i in range(1, Settngs.REQUEST_COUNT + 1)]
    for future in as_completed(futures):
        print(f"{future.result()}\n")

print("\nIf every request succeeded, check that the test key/team actually has a low RPM limit.")
print("Do not use a production key for this experiment.")
