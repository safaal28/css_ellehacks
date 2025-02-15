import streamlit as st

def display_report(results):
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