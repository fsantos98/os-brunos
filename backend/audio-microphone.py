import asyncio
import sounddevice as sd
from amazon_transcribe.client import TranscribeStreamingClient
from amazon_transcribe.handlers import TranscriptResultStreamHandler
from amazon_transcribe.model import TranscriptEvent
from datetime import datetime
import aiofiles  # Async file operations
import requests

import httpx
import asyncio

from generate_summary import send_to_generate_summary
from ai_assistant import get_timestamps_ai

async def handle_summary_action(transcript):
    url = "http://localhost:5111/transcripts"

    dates = get_timestamps_ai(transcript)

    print(dates)


    dates = [
        f"[{datetime.strptime(date, '%Y-%m-%d %H:%M').strftime('%Y-%m-%d %H:%M:%S')}]"
        for date in dates
    ]
    print(dates[0])
    print(dates[1])
    payload = {
        "start": dates[0],
        "end": dates[1],
    }

    print("send request to: ", url)
    print("payload: ", payload)
    try:
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            print("Response JSON:", response.json())
            # The data you want to send (the transcript and other information)
            transcript_data = ' '.join(response.json())

            summary_command = transcript
            full_prompt = f"{transcript_data}\n\n{summary_command}"
            
            send_to_generate_summary(transcript_data, summary_command, 1)
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")    
    



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
