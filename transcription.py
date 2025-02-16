import assemblyai as aai
import os

def transcribe_audio(audio_file):
    """
    Transcribe the uploaded audio file using AssemblyAI and return the transcription.

    Args:
        audio_file (str): The path to the audio file to be transcribed.

    Returns:
        str: The transcription of the audio file with speaker labels.
    """
    # Set the AssemblyAI API key from environment variables
    aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")

    # Configure the transcription settings to include speaker labels
    config = aai.TranscriptionConfig(
        speaker_labels=True,
    )

    # Create a transcriber instance
    transcriber = aai.Transcriber()

    # Transcribe the audio file using the specified configuration
    transcript = transcriber.transcribe(audio_file, config)

    # Initialize an empty string to accumulate the transcription
    cumulative_transcript = ""

    # Iterate over each utterance in the transcript and format it with speaker labels
    for utterance in transcript.utterances:
        cumulative_transcript += f"Speaker {utterance.speaker}: {utterance.text}\n"

    # Return the cumulative transcription
    return cumulative_transcript