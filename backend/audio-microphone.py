import asyncio
import sounddevice as sd
from amazon_transcribe.client import TranscribeStreamingClient
from amazon_transcribe.handlers import TranscriptResultStreamHandler
from amazon_transcribe.model import TranscriptEvent
from datetime import datetime
import aiofiles  # Async file operations

import httpx
import asyncio

import json
import logging
import boto3

from botocore.exceptions import ClientError


class ImageError(Exception):
    "Custom exception for errors returned by Amazon &titan-text-express; model"

    def __init__(self, message):
        self.message = message


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def generate_text(model_id, body):
    """
    Generate text using Amazon &titan-text-express; model on demand.
    Args:
        model_id (str): amazon.titan-text-express-v1.
        body (str) : The request body to use.
    Returns:
        response (json): The response from the model.
    """

    logger.info(
        "Generating text with Amazon &titan-text-express; model %s", model_id)

    bedrock = boto3.client(service_name='bedrock-runtime')

    accept = "application/json"
    content_type = "application/json"

    response = bedrock.invoke_model(
        body=body, modelId=model_id, accept=accept, contentType=content_type
    )
    response_body = json.loads(response.get("body").read())

    finish_reason = response_body.get("error")

    if finish_reason is not None:
        raise ImageError(f"Text generation error. Error is {finish_reason}")

    logger.info(
        "Successfully generated text with Amazon &titan-text-express; model %s", model_id)

    return response_body

def send_to_generate_summary(prompt, command):
    try:
        logging.basicConfig(level=logging.INFO,
                            format="%(levelname)s: %(message)s")

        model_id = 'amazon.titan-text-express-v1'

        # Example usage for summarizing a discussion
        discussion_prompt = prompt

        summary_command = command
        full_prompt = f"{discussion_prompt}\n\n{summary_command}"

        body = json.dumps({
            "inputText": full_prompt,
            "textGenerationConfig": {
                "maxTokenCount": 4096,
                "stopSequences": [],
                "temperature": 0,
                "topP": 1
            }
        })

        response_body = generate_text(model_id, body)
        print(f"Input token count: {response_body['inputTextTokenCount']}")

        for result in response_body['results']:
            print(f"Token count: {result['tokenCount']}")
            print(f"Output text: {result['outputText']}")
            print(f"Completion reason: {result['completionReason']}")

    except ClientError as err:
        message = err.response["Error"]["Message"]
        logger.error("A client error occurred: %s", message)
        print("A client error occured: " +
              format(message))
    except ImageError as err:
        logger.error(err.message)
        print(err.message)

    else:
        print(
            f"Finished generating text with the Amazon &titan-text-express; model {model_id}.")


async def handle_summary_action(data: None):
    url = "http://localhost:5111/transcript"
    
    # The data you want to send (the transcript and other information)
    transcript_data = """
    I think we should focus on improving the user interface.
    Yes, the current design is outdated and not very user-friendly.
    We also need to consider the performance issues.
    Agreed, but let's prioritize the UI first.
    I can start working on some new design mockups.
    I'll look into optimizing the backend performance.
    Great, let's reconvene next week with our progress.
    """

    summary_command = "Give me a summary of the discussion, in bullet points."
    full_prompt = f"{transcript_data}\n\n{summary_command}"
    
    send_to_generate_summary(transcript_data, summary_command)


# Define the action as a function reference, not executing it immediately
keyword_actions = {
    "Jarvis": handle_summary_action  # Store the function reference here
}

class MyEventHandler(TranscriptResultStreamHandler):
    def __init__(self, output_stream, source):
        super().__init__(output_stream)
        self.source = source

    async def handle_transcript_event(self, transcript_event: TranscriptEvent):
        results = transcript_event.transcript.results
        for result in results:
            if not result.is_partial:
                for alt in result.alternatives:
                    transcript_text = alt.transcript
                    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
                    log_entry = f"{timestamp} [{self.source}] {transcript_text}\n"
                    async with aiofiles.open(f"transcription_{datetime.now().strftime('%Y-%m-%d')}.txt", "a") as f:
                        await f.write(log_entry)
                    print(log_entry, end="")
                    for keyword, action in keyword_actions.items():
                        if keyword.lower() in transcript_text.lower():
                            asyncio.create_task(action(transcript_text))

async def audio_stream(device_name):
    loop = asyncio.get_event_loop()
    input_queue = asyncio.Queue()

    def callback(indata, frames, time, status):
        loop.call_soon_threadsafe(input_queue.put_nowait, (bytes(indata), status))

    stream = sd.RawInputStream(
        channels=1,
        samplerate=16000,
        callback=callback,
        blocksize=1024 * 2,
        dtype="int16",
        device=device_name
    )

    with stream:
        while True:
            indata, status = await input_queue.get()
            yield indata, status

async def write_chunks(stream, device_name):
    async for chunk, status in audio_stream(device_name):
        await stream.input_stream.send_audio_event(audio_chunk=chunk)
    await stream.input_stream.end_stream()

async def transcribe_audio(source, device_name):
    client = TranscribeStreamingClient(region="us-west-2")
    stream = await client.start_stream_transcription(
        language_code="en-US",
        media_sample_rate_hz=16000,
        media_encoding="pcm"
    )
    handler = MyEventHandler(stream.output_stream, source)
    await asyncio.gather(write_chunks(stream, device_name), handler.handle_events())

async def main():
    mic_task = asyncio.create_task(transcribe_audio("Microphone", None))  # Use default mic
    comp_audio_task = asyncio.create_task(transcribe_audio("Computer Audio", "BlackHole 2ch"))
    await asyncio.gather(mic_task, comp_audio_task)

if __name__ == "__main__":
    asyncio.run(main())
