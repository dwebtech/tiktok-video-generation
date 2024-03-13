import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("PERPLEXITY_API_KEY")

messages = [
    {
        "role": "system",
        "content": (
            "You are an artificial intelligence assistant that helps to generate engaging travel information "
            "You will be provided with a location, city or country and are supposed to give information about this place in an"
            "engaing way. The respose should be around 7 sentences. "
        ),
    },
    {
        "role": "user",
        "content": (
            "Marocco?"
        ),
    },
]

client = OpenAI(api_key=API_KEY, base_url="https://api.perplexity.ai")

# chat completion without streaming
response = client.chat.completions.create(
    model="mistral-7b-instruct",
    messages=messages,
)
print(response)

