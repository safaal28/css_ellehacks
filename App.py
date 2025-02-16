import streamlit as st
import cohere
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
cohere_key = os.getenv("COHERE_API_KEY")

# Set up Cohere API
COHERE_API_KEY = cohere_key
co = cohere.Client(COHERE_API_KEY)


# Create UI
st.set_page_config(page_title="Conversation Insights", layout="wide")

st.title("Delulu Detector Demo")

# User Inputs
conversation_text = st.text_area("Paste the conversation here:", height=200)
person_name = st.text_input("Person's Name")
relationship_type = st.selectbox("Relationship Type", ["Situationship", "Partner", "Friend", "Parent"])

if st.button("Generate Insights"):

    if not conversation_text or not person_name:
        st.warning("Please enter a conversation and a name.")
    
    else:
        conversation_text = "\n".join([line.strip() for line in conversation_text.split("\n")])

        with st.spinner("Preparing to spill the tea..."):
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
                5. **Red Flags** (e.g., gaslighting, stonewalling) with examples.
                6. **Green Flags** (e.g., positive affirmations) with examples.

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

            # print("RESPONSE: ", response.generations[0].text)

            # st.write(response.generations[0].text)

            try:
                insights = json.loads(response.generations[0].text)
            except json.JSONDecodeError as e:
                st.error("Failed to parse the response. The response might be incomplete or malformed.")
                st.text_area("Response Text", response_text, height=200)
                st.stop()

            print(response.generations[0].text) # Debugging step

            # Display Results
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


st.button("Print Report", on_click=lambda: st.write("Use your browser's print function (Ctrl+P)."))
