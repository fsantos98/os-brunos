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

#from generate_summary import send_to_generate_summary
from generate_summary_openapi import send_to_generate_summary
from ai_assistant import get_timestamps_ai
#from generate_image import send_to_generate_image

async def handle_summary_action(transcript):
    url = "http://ec2-18-246-27-158.us-west-2.compute.amazonaws.com:5111/transcripts"

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

#send_to_generate_summary("[2024-11-23 08:00:00] [Microphone] Good morning, team. Lets kick off todays stand-up. Sara, youre up first., [2024-11-23 08:00:10] [Computer Audio] Good morning! Yesterday, I finalized the onboarding flow and pushed it for review. I also looked into the accessibility issue reported on the settings page. Today, Ill address PR feedback and start fixing those focus management problems. No blockers for now.m[2024-11-23 08:00:30] [Microphone] Great. Thanks, Sara. John, how about you? [2024-11-23 08:00:40] [Computer Audio] Morning, everyone. I worked on indexing the database for search optimization yesterday. The results are decent but not great. Today, Ill profile the queries further and experiment with caching strategies. Ill also need to sync with the database team for configuration support., [2024-11-23 08:01:00] [Microphone] Makes sense. Let me know if you need help. Ill be finalizing the backend logic for the payment system refactor and squashing a few bugs flagged by QA. Lets aim to make solid progress today., [2024-11-23 08:01:20] [Microphone] Before we wrap up, Id like to address some common pain points. John, you mentioned memory usage issues with the new index. Can you elaborate?, [2024-11-23 08:01:30] [Computer Audio] Sure. When traffic spikes, the index uses a lot of memory, especially for multi-field queries. We might need to optimize which fields are indexed. [2024-11-23 08:01:50] [Microphone] Got it. Would reducing the fields being indexed help, or should we consider a more advanced database configuration?, [2024-11-23 08:02:00] [Computer Audio] Id say lets start with reducing the fields and running benchmarks. If that doesnt work, we can explore other options., [2024-11-23 08:02:20] [Microphone] Okay, lets keep each other posted on progress. Sara, anything else to flag before we move on?, [2024-11-23 08:02:30] [Computer Audio] Just a quick note. I might need to loop in the design team for some accessibility-related edge cases. Can we arrange that later?, [2024-11-23 08:02:50] [Microphone] Absolutely. Lets aim for a brief sync this afternoon., [2024-11-23 09:30:00] [Microphone] Alright, team, lets jump into sprint planning. First, John, lets go deeper into your search optimization work. How is the caching proposal coming along?, [2024-11-23 09:30:20] [Computer Audio] Ive been researching Redis as a caching solution. Its fast and supports persistence, but I want to ensure we handle invalidation properly., [2024-11-23 09:30:40] [Microphone] What strategies are you thinking of for invalidation? Event-driven or time-based?, [2024-11-23 09:30:50] [Computer Audio] A hybrid approach. Event-driven invalidation for critical data updates and time-based for less dynamic data. Ill need some input on how to classify the data., [2024-11-23 09:31:10] [Microphone] That sounds good. Sara, do you have thoughts on this?, [2024-11-23 09:31:20] [Computer Audio] We need to balance performance and complexity. For instance, user preferences could use time-based expiration, while transactional data should rely on event-driven., [2024-11-23 09:31:40] [Microphone] Great points. Lets document these classifications. John, can you take the lead?, [2024-11-23 09:31:50] [Computer Audio] Sure. Ill draft a proposal and share it in our next sync., [2024-11-23 09:32:10] [Microphone] Moving on. Sara, hows the accessibility work going?, [2024-11-23 09:32:20] [Computer Audio] Its progressing, but Ive hit a few snags with focus management. For example, navigating modal dialogs is tricky when screen readers are involved. Ill need the design team to validate some changes., [2024-11-23 09:32:40] [Microphone] Makes sense. Lets loop them in for a quick review this afternoon. Anything else?, [2024-11-23 09:32:50] [Computer Audio] Not for now., [2024-11-23 09:33:10] [Microphone] Finally, lets discuss the database migration next week. Any compatibility concerns so far?, [2024-11-23 09:33:20] [Computer Audio] Ive been testing the main modules, and they look good overall. However, I noticed some discrepancies in timestamp formats between the old and new systems. Ill sync with infrastructure later today., [2024-11-23 09:33:40] [Microphone] Good call. Lets address these issues by Friday so were migration-ready.", 'Can you make a summary of the meeting in bullet points, also make a mermaid graph about the employees', 1)
#prompt = "A blue backpack"
#saved_images = send_to_generate_image(prompt, folder="generated_images", number_of_images=1)
#print(saved_images)


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
