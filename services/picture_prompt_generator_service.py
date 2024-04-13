import os
import re
from typing import List, Tuple
from xml.dom.minidom import Document
from openai import OpenAI
from dotenv import load_dotenv
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings

load_dotenv()

class CustomSemanticChunker(SemanticChunker):
    def split_text(
        self,
        text: str,
    ) -> List[str]:
        # Splitting the essay on '.', '?', ',' and '!'
        single_sentences_list = re.split(r"(?<=[.?!,])\s+", text)
        # Merge subsentences that are smaller than 5 words and end on a comma with the next sentence
        merged_sentences = []
        i = 0
        while i < len(single_sentences_list):
            current_sentence = single_sentences_list[i]
            if i < len(single_sentences_list) - 1:
                next_sentence = single_sentences_list[i + 1]
                if len(current_sentence.split()) < 5 and current_sentence.endswith(","):
                    merged_sentence = current_sentence + " " + next_sentence
                    merged_sentences.append(merged_sentence)
                    i += 2  # Skip the next sentence
                else:
                    merged_sentences.append(current_sentence)
                    i += 1
            else:
                merged_sentences.append(current_sentence)
                i += 1
        single_sentences_list = merged_sentences

        # having len(single_sentences_list) == 1 would cause the following
        # np.percentile to fail.
        if len(single_sentences_list) == 1:
            return single_sentences_list
        distances, sentences = self._calculate_sentence_distances(single_sentences_list)
        if self.number_of_chunks is not None:
            breakpoint_distance_threshold = self._threshold_from_clusters(distances)
        else:
            breakpoint_distance_threshold = self._calculate_breakpoint_threshold(
                distances
            )

        indices_above_thresh = [
            i for i, x in enumerate(distances) if x > breakpoint_distance_threshold
        ]

        chunks = []
        start_index = 0

        # Iterate through the breakpoints to slice the sentences
        for index in indices_above_thresh:
            # The end index is the current breakpoint
            end_index = index

            # Slice the sentence_dicts from the current start index to the end index
            group = sentences[start_index : end_index + 1]
            combined_text = " ".join([d["sentence"] for d in group])
            chunks.append(combined_text)

            # Update the start index for the next group
            start_index = index + 1

        # The last group, if any sentences remain
        if start_index < len(sentences):
            combined_text = " ".join([d["sentence"] for d in sentences[start_index:]])
            chunks.append(combined_text)
        return chunks

def generate_image_prompts_for_text(text: str, location: str) -> List[Tuple[str, str]]:
    """Generates picture prompts for a given text and location."""
    segments: List[str] = generate_semantic_segments(text)
    return [(segment, create_picture_prompt_for_segment(segment, location)) for segment in segments]


def generate_semantic_segments(text: str) -> List[str]:
    """Splits the input text semantically into segments using OpenAI embeddings and Langchain."""
    text_splitter: SemanticChunker = SemanticChunker(OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY")), breakpoint_threshold_type="percentile", breakpoint_threshold_amount=0.5)
    docs: List[Document] = text_splitter.create_documents([text])
    return list(map(lambda doc: doc.page_content, docs))

def generate_semantic_segments_subsentences(text: str) -> List[str]:
    """Splits the input text semantically into segments using OpenAI embeddings and Langchain with preprocessing."""
    text_splitter: CustomSemanticChunker = CustomSemanticChunker(OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY")), breakpoint_threshold_type="percentile", breakpoint_threshold_amount=0.5)
    docs: List[Document] = text_splitter.create_documents([text])
    return list(map(lambda doc: doc.page_content, docs))

def create_picture_prompt_for_segment(segment: str, location: str) -> str:
    """Creates a picture prompt for a given segment and location."""
    messages: list[dict[str, str]] = [
        {
            "role": "system",
            "content": (
                "Given a location and additional information, you create a picture prompt."
                "Describe what a picture visualizing the additional information would look like in one short sentence."
                "Just give a one sentence description including the location. Here is an example"
                "For input Location: Pittsburgh, Additional Information: Wander through the historic neighborhoods of the North Side and the South Side, where you'll find a perfect blend of modern innovation and traditional charm."
                "This could be an answer: Historic buildings in Pittsburgh South Side with some people walking the streets."
            ),
        },
        {
            "role": "user",
            "content": f"Location: f{location}, Additional Information: {segment}. Now give me a picture prompt:",  # Inject user input into the request
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
    segments: List[str] = generate_semantic_segments_subsentences(text)
    for segment in segments:
        print(segment + '\n')
        print(create_picture_prompt_for_segment(segment, location) + '\n\n')

if __name__ == "__main__":
    main()

