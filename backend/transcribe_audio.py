import asyncio
import sounddevice as sd
from amazon_transcribe.client import TranscribeStreamingClient
from amazon_transcribe.handlers import TranscriptResultStreamHandler
from amazon_transcribe.model import TranscriptEvent
from datetime import datetime

async def handle_summary_action(transcript):
    print(f"Handling summary for: {transcript}")
    await asyncio.sleep(1)
    print("Summary action completed!")

keyword_actions = {
    "summary": handle_summary_action,
}

class MyEventHandler(TranscriptResultStreamHandler):
    async def handle_transcript_event(self, transcript_event: TranscriptEvent):
        results = transcript_event.transcript.results
        for result in results:
            if not result.is_partial:
                for alt in result.alternatives:
                    transcript_text = alt.transcript
                    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
                    with open(f"transcription_{datetime.now().strftime('%Y-%m-%d')}.txt", "a") as f:
                        f.write(f"{timestamp} {transcript_text}\n")
                    print(f"{timestamp} {transcript_text}")
                    for keyword, action in keyword_actions.items():
                        if keyword.lower() in transcript_text.lower():
                            asyncio.create_task(action(transcript_text))

async def audio_stream():
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
        device="BlackHole 2ch"  # Change this to your virtual audio device name
    )

    with stream:
        while True:
            indata, status = await input_queue.get()
            yield indata, status

async def write_chunks(stream):
    async for chunk, status in audio_stream():
        await stream.input_stream.send_audio_event(audio_chunk=chunk)
    await stream.input_stream.end_stream()

async def basic_transcribe():
    client = TranscribeStreamingClient(region="us-west-2")
    stream = await client.start_stream_transcription(
        language_code="en-US",
        media_sample_rate_hz=16000,
        media_encoding="pcm"
    )
    handler = MyEventHandler(stream.output_stream)
    await asyncio.gather(write_chunks(stream), handler.handle_events())

loop = asyncio.get_event_loop()
loop.run_until_complete(basic_transcribe())
loop.close()
