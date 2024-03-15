import os
from openai import OpenAI
from dotenv import load_dotenv

import voice_generator

load_dotenv()

API_KEY = os.getenv("PERPLEXITY_API_KEY")
# Ask the user for input
location = input("Please enter a location for travel information: ")

messages = [
    {
        "role": "system",
        "content": (
            "You are an artificial intelligence assistant that helps to generate engaging travel information. "
            "You will be provided with a location, city or country and are supposed to give information about this place in an "
            "engaging way. The response should be around 4 sentences."
        ),
    },
    {
        "role": "user",
        "content": location,  # Inject user input into the request
    },
]

client = OpenAI(api_key=API_KEY, base_url="https://api.perplexity.ai")

# Chat completion without streaming
response = client.chat.completions.create(
    model="mistral-7b-instruct",
    messages=messages,
)
message_content = response.choices[0].message.content

print(message_content)

voice_generator.synthesize_speech(message_content)