import asyncio
import time
import requests
from filelock import FileLock

from bedrock import get_timestamps

# This example uses the sounddevice library to get an audio stream from the
# microphone. It's not a dependency of the project but can be installed with
# `pip install sounddevice`.
import sounddevice


from amazon_transcribe.client import TranscribeStreamingClient
from amazon_transcribe.handlers import TranscriptResultStreamHandler
from amazon_transcribe.model import TranscriptEvent


"""
Here's an example of a custom event handler you can extend to
process the returned transcription results as needed. This
handler will simply print the text out to your interpreter.
"""


async def handle_summary_action(transcript):
    print(f"Handling summary for: {transcript}")
    # Simulate a request or perform a task
    await asyncio.sleep(1)  # Replace with actual background task
    start_time, end_time  = get_timestamps(transcript)
    # URL to send the GET request to
    url = "http://localhost:3000/get_text"
    payload = {
        "start_time": start_time,
        "end_time": end_time,
    }

    print("send request to: ", url)
    print("payload: ", payload)
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        print("Response JSON:", response.json())
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")

keyword_actions = {
    "summary": handle_summary_action,
}


class MyEventHandler(TranscriptResultStreamHandler):
    async def handle_transcript_event(self, transcript_event: TranscriptEvent):
        # This handler can be implemented to handle transcriptions as needed.
        # Here's an example to get started.
         # Create a lock for the file.
        lock = FileLock("transcriptions.txt.lock")
        with lock:
            with open("transcriptions.txt", "a", encoding="utf-8") as file:
                results = transcript_event.transcript.results
                for result in results:
                    print(result.is_partial)
                    if not result.is_partial:
                        for alt in result.alternatives:
                            print(alt.transcript)
                            transcript_text = alt.transcript
                            timestamp_now = str(int(time.time()))
                            file.write(timestamp_now + " [PERSON] " + transcript_text + "\n")

                            for keyword, action in keyword_actions.items():
                                if keyword.lower() in transcript_text.lower():
                                    asyncio.create_task(action(transcript_text))


async def mic_stream():
    # This function wraps the raw input stream from the microphone forwarding
    # the blocks to an asyncio.Queue.
    loop = asyncio.get_event_loop()
    input_queue = asyncio.Queue()

    def callback(indata, frame_count, time_info, status):
        loop.call_soon_threadsafe(input_queue.put_nowait, (bytes(indata), status))

    # Be sure to use the correct parameters for the audio stream that matches
    # the audio formats described for the source language you'll be using:
    # https://docs.aws.amazon.com/transcribe/latest/dg/streaming.html
    stream = sounddevice.RawInputStream(
        channels=1,
        samplerate=16000,
        callback=callback,
        blocksize=1024 * 2,
        dtype="int16",
    )
    # Initiate the audio stream and asynchronously yield the audio chunks
    # as they become available.
    with stream:
        while True:
            indata, status = await input_queue.get()
            yield indata, status


async def write_chunks(stream):
    # This connects the raw audio chunks generator coming from the microphone
    # and passes them along to the transcription stream.
    async for chunk, status in mic_stream():
        await stream.input_stream.send_audio_event(audio_chunk=chunk)
    await stream.input_stream.end_stream()


async def basic_transcribe():
    # Setup up our client with our chosen AWS region
    client = TranscribeStreamingClient(region="us-west-2")

    # Start transcription to generate our async stream
    stream = await client.start_stream_transcription(
        language_code="en-US",
        media_sample_rate_hz=16000,
        media_encoding="pcm",
    )

    # Instantiate our handler and start processing events
    handler = MyEventHandler(stream.output_stream)
    print("Start talking you pato")
    await asyncio.gather(write_chunks(stream), handler.handle_events())


loop = asyncio.get_event_loop()
loop.run_until_complete(basic_transcribe())
loop.close()