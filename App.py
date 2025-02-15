import streamlit as st
from analysis import analyze_conversation
from report import display_report

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
# openai_key = os.getenv("OPENAI_API_KEY")
# print("open ai key", openai_key)

google_key = os.getenv("GOOGLE_CLOUD_API_KEY")
# print("google cloud key", openai_key)
anthropic_key = os.getenv("ANTHROPIC_API_KEY")
# print("anthropic key", openai_key)

# if not openai_key:
#     raise ValueError("Error: OpenAI API key is missing!")

if not google_key:
    raise ValueError("Error: Google Cloud API key is missing!")

if not anthropic_key:
    raise ValueError("Error: Anthropic API key is missing!")

st.title("Relationship Insights Analyzer")

# User Inputs
name = st.text_input("Your Name")
partner_name = st.text_input("Partner's Name")
relationship_type = st.selectbox("Relationship Type", ["Romantic", "Family", "Friend", "Colleague"])
conversation = st.text_area("Paste your conversation here")


if st.button("Analyze Conversation"):
    results = analyze_conversation(conversation, name, partner_name, relationship_type)

    # Display Report
    st.subheader("Conversation Analysis Report")
    st.metric("Overall Conversation Health Score", f"{results['health_score']}%")
    st.write("### Sentiment Breakdown")
    st.json(results["sentiment"])
    st.write("### Detected Issues")
    st.json(results["issues_detected"])
    st.write(f"### Communication Style: {results['communication_style']}")
    st.write("### Therapist Recommendations")
    for rec in results["therapist_recommendations"]:
        st.write(f"- {rec}")
