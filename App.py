import streamlit as st
from analysis import analyze_conversation
from report import display_report
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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
