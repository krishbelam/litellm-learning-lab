"""Demo 1: one request through LiteLLM Proxy.

The client uses the OpenAI SDK because LiteLLM exposes an OpenAI-compatible API.
The key below is a LiteLLM virtual key, not an Ollama or OpenAI provider key.
"""
import os
from openai import OpenAI
from configs import Settngs

client = OpenAI(api_key=Settngs.VIRTUAL_KEY, base_url=Settngs.BASE_URL)

response = client.chat.completions.create(
    model=Settngs.MODEL,
    messages=[
        {
            "role": "system",
            "content": "You are a concise and helpful assistant for a fictional bookstore.",
        },
        {
            "role": "user",
            "content": "A customer ordered a paperback, but the package arrived damaged. "
                       "Give a polite three-step support response.",
        },
    ],
    temperature=2,
)

print(response.choices[0].message.content)
