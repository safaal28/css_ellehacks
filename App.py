import streamlit as st
import cohere
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
from dotenv import load_dotenv
from transcription import transcribe_audio

def load_environment_variables():
    """
    Load environment variables from a .env file and return the Cohere API key.

    Returns:
        str: The Cohere API key.
    """
    load_dotenv()
    cohere_key = os.getenv("COHERE_API_KEY")
    return cohere_key

def setup_cohere_client(api_key):
    """
    Set up and return a Cohere API client.

    Args:
        api_key (str): The Cohere API key.

    Returns:
        cohere.Client: The Cohere API client.
    """
    return cohere.Client(api_key)

def read_message_file(file_path):
    """
    Read the content of a message file and return it as a string.

    Args:
        file_path (str): The path to the message file.

    Returns:
        str: The content of the message file.
    """
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    return ""

def transcribe_uploaded_audio(uploaded_audio):
    """
    Transcribe the uploaded audio file and return the transcription.

    Args:
        uploaded_audio (UploadedFile): The uploaded audio file.

    Returns:
        str: The transcription of the audio file.
    """
    if uploaded_audio is not None:
        return transcribe_audio(uploaded_audio)
    return ""

def generate_insights(co, conversation_text, person_name, relationship_type):
    """
    Generate insights from the conversation text using the Cohere API.

    Args:
        co (cohere.Client): The Cohere API client.
        conversation_text (str): The conversation text.
        person_name (str): The name of the person in the conversation.
        relationship_type (str): The type of relationship.

    Returns:
        str: The generated insights in JSON format.
    """
    response = co.generate(
        model="command-r-plus",
        prompt=f"""
        Analyze the following conversation and provide insights.

        Conversation:
        {conversation_text}

        Relationship Type: {relationship_type}

        Provide:
        1. **Conversation Health Summary** (One sentence with a percentage score).
        2. **Attachment Style** of {person_name} (Fearful-Avoidant, Dismissive-Avoidant, etc.) with 3-4 explanatory sentences.
        3. **Communication Patterns** (Passive Aggressive, Assertive, etc.), with 3-4 sentences on identified traits.
        4. **Communication Insights** (Dominant speaker, interruptions, and a sentiment trend graph).
        5. **Red Flags** (e.g., gaslighting, stonewalling) with examples. Form as list.
        6. **Green Flags** (e.g., positive affirmations) with examples. Form as list.

        Output should be structured JSON format with no trailing whitespaces or newlines:
        {{
            "conversation_health": "...",
            "attachment_style": "...",
            "communication_patterns": "...",
            "communication_insights": "...",
            "red_flags": "...",
            "green_flags": "..."
        }}
        """,
        max_tokens=700,
        temperature=0.7
    )
    return response.generations[0].text

def display_results(insights):
    """
    Display the generated insights in the Streamlit app.

    Args:
        insights (dict): The generated insights.
    """
    st.subheader("Conversation Health Summary")
    st.write(insights["conversation_health"])

    st.subheader("Attachment Style")
    st.write(insights["attachment_style"])

    st.subheader("Communication Patterns")
    st.write(insights["communication_patterns"])

    st.subheader("Communication Insights")
    st.write(insights["communication_insights"])

    st.subheader("Red Flags 🚩")
    for red_flag in insights["red_flags"]:
        st.write(f"- {red_flag}")

    st.subheader("Green Flags ✅")
    for green_flag in insights["green_flags"]:
        st.write(f"- {green_flag}")

def main():
    """
    Main function to run the Streamlit app.
    """
    # Load environment variables and set up Cohere API client
    cohere_key = load_environment_variables()
    co = setup_cohere_client(cohere_key)

    # Read the content of message.txt
    message_content = read_message_file("message.txt")

    # Create UI
    st.set_page_config(page_title="Conversation Insights", layout="wide")
    st.title("Delulu Detector Demo")

    # Audio Upload
    uploaded_audio = st.file_uploader("Upload an audio file (MP3, WAV, M4A)", type=["mp3", "wav", "m4a"])

    # User Inputs
    conversation_text = st.text_area("Conversation transcript", value=message_content, height=200)
    person_name = st.text_input("Person's Name")
    relationship_type = st.selectbox("Relationship Type", ["Situationship", "Partner", "Friend", "Parent"])

    if st.button("Generate Insights"):
        if not conversation_text and not person_name:
            st.warning("Please enter a conversation and a name.")
        if not conversation_text:
            st.warning("Please enter a conversation.")
        if not person_name:
            st.warning("Please enter a name.")
        else:
            conversation_text = "\n".join([line.strip() for line in conversation_text.split("\n")])
            with st.spinner("Preparing to spill the tea..."):
                response_text = generate_insights(co, conversation_text, person_name, relationship_type)
                try:
                    insights = json.loads(response_text)
                except json.JSONDecodeError as e:
                    st.error("Failed to parse the response. The response might be incomplete or malformed.")
                    st.text_area("Response Text", response_text, height=200)
                    st.stop()

                print(response_text)  # Debugging step
                display_results(insights)


if __name__ == "__main__":
    main()