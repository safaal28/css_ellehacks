import assemblyai as aai
import os

def transcribe_audio(audio_file):
    aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")
    config = aai.TranscriptionConfig(
        speaker_labels=True,
    )
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file, config)

    cumulative_transcript = ""
    for utterance in transcript.utterances:
        # print(f"Speaker {utterance.speaker}: {utterance.text}")
        cumulative_transcript += f"Speaker {utterance.speaker}: {utterance.text}\n"

    return cumulative_transcript