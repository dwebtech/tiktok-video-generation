import os
from openai import OpenAI
from dotenv import load_dotenv

import services.voice_generator_service as voice_generator

load_dotenv()

def generate_script(location: str) -> str:
    API_KEY: str = os.getenv("PERPLEXITY_API_KEY")
    # Ask the user for input
    messages: list[dict[str, str]] = [
    {
        "role": "system",
        "content": (
            "You are an artificial intelligence assistant that helps to generate engaging travel information. "
            "You will be provided with a location, city or country and are supposed to give information about "
            "this place in an engaging way. The response should be around 4 sentences."
        ),
    },
    {
        "role": "user",
        "content": location,  # Inject user input into the request
    },
]

    client: OpenAI = OpenAI(api_key=API_KEY, base_url="https://api.perplexity.ai")

    # Chat completion without streaming
    response: OpenAI.ChatCompletion = client.chat.completions.create(
    model="mistral-7b-instruct",
    messages=messages,
    )
    message_content: str = response.choices[0].message.content
    return message_content

if __name__ == "__main__":
    location: str = input("Please enter the location: ")
    message_content: str = generate_script(location)
    print(message_content)
