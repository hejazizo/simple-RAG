import os
from openai import OpenAI

OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")
if not OPEN_AI_API_KEY:
    raise ValueError("OPEN_AI_API_KEY is not set")

def call_llm(model_name, prompt_text):
    temperature = 0.7
    max_tokens = 1000

    client = OpenAI(api_key=OPEN_AI_API_KEY)

    response = client.chat.completions.create(
        model=model_name,
        messages=[{'role': 'user', 'content': prompt_text}],
        temperature=temperature,
        max_tokens=max_tokens
    )

    return response.choices[0].message.content.strip()
