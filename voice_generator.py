from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
from tempfile import gettempdir

def synthesize_speech(text, voice_id="Stephen"):
    """Synthesize speech from the provided text using Amazon Polly."""

    # Create a session using the credentials and region defined in the AWS credentials file (~/.aws/credentials).
    session = Session()
    polly = session.client("polly")

    try:
        # Request speech synthesis
        response = polly.synthesize_speech(Text=text, OutputFormat="mp3", VoiceId=voice_id, Engine="neural")
    except (BotoCoreError, ClientError) as error:
        # The service returned an error, exit gracefully
        print(error)
        return None

    # Access the audio stream from the response
    if "AudioStream" in response:
        with closing(response["AudioStream"]) as stream:
            output = os.path.join(os.getcwd(), "speech.mp3")  # Save in the current working directory

            try:
                # Open a file for writing the output as a binary stream
                with open(output, "wb") as file:
                    file.write(stream.read())
            except IOError as error:
                # Could not write to file, exit gracefully
                print(error)
                return None

            return output

    else:
        # The response didn't contain audio data, exit gracefully
        print("Could not stream audio")
        return None
