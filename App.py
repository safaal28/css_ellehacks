import streamlit as st
from analysis import analyze_conversation
from report import display_report

st.title("Relationship Insights Analyzer")

# User Inputs
name = st.text_input("Your Name")
partner_name = st.text_input("Partner's Name")
relationship_type = st.selectbox("Relationship Type", ["Romantic", "Family", "Friend", "Colleague"])
conversation = st.text_area("Paste your conversation here")

if st.button("Analyze Conversation"):
    results = analyze_conversation(conversation, name, partner_name, relationship_type)
    display_report(results)

