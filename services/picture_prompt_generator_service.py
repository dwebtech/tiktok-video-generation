import os
from typing import List
from xml.dom.minidom import Document
from openai import OpenAI
from dotenv import load_dotenv
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings

load_dotenv()

def generate_image_prompts_for_text(text: str, location: str) -> List[str]:
    """Generates picture prompts for a given text and location."""
    segments: List[str] = generate_semantic_segments(text)
    return [create_picture_prompt_for_segment(segment, location) for segment in segments]


def generate_semantic_segments(text: str) -> List[str]:
    """Splits the input text semantically into segments using OpenAI embeddings."""
    text_splitter: SemanticChunker = SemanticChunker(OpenAIEmbeddings(), breakpoint_threshold_type="percentile", breakpoint_threshold_amount=0.5)
    docs: List[Document] = text_splitter.create_documents([text])
    return list(map(lambda doc: doc.page_content, docs))

def create_picture_prompt_for_segment(segment: str, location: str) -> str:
    """Creates a picture prompt for a given segment and location."""
    messages: list[dict[str, str]] = [
        {
            "role": "system",
            "content": (
                "Given a location and additional information, you are supposed to create a picture prompt."
                "Describe what a picture visualizing the additional information would look like in one short sentence."
                "Just give the description and feel free to include the location."
                "For input Location: Pittsburgh, Additional Information: Wander through the historic neighborhoods of the North Side and the South Side, where you'll find a perfect blend of modern innovation and traditional charm."
                "This could be an answer: Historic buildings in Pittsburgh South Side with some people walking the streets."
            ),
        },
        {
            "role": "user",
            "content": f"Location: f{location}, Additional Information: {segment}",  # Inject user input into the request
        }
    ]

    client: OpenAI = OpenAI(api_key=os.getenv("PERPLEXITY_API_KEY"), base_url="https://api.perplexity.ai")

    response: OpenAI.ChatCompletion = client.chat.completions.create(
        model="mistral-7b-instruct",
        messages=messages,
    )
    return response.choices[0].message.content

def main():
    text: str = input("Please enter the text to split: ")
    location: str = input("Please enter the location: ")
    segments: List[str] = generate_semantic_segments(text)
    for segment in segments:
        print(segment + '\n')
        print(create_picture_prompt_for_segment(segment, location) + '\n\n')

if __name__ == "__main__":
    main()

