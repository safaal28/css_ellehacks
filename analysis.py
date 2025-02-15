from transformers import pipeline
from google.cloud import language_v1
from openai import OpenAI
import os
import anthropic
import streamlit as st

openai_key = os.getenv("OPENAI_API_KEY")
# print("openai key",openai_key)

google_key = os.getenv("GOOGLE_CLOUD_API_KEY")
anthropic_key = os.getenv("ANTHROPIC_API_KEY")

# if not openai_key:
#     raise ValueError("Error: OpenAI API key is missing!")

# if not google_key:
#     raise ValueError("Error: Google Cloud API key is missing!")

# if not anthropic_key:
#     raise ValueError("Error: Anthropic API key is missing!")

client = OpenAI(api_key=openai_key)
# Hugging Face Sentiment Analysis
def analyze_sentiment_hf(convo):
    sentiment_pipeline = pipeline("sentiment-analysis")
    results = sentiment_pipeline(convo[:512])  # Hugging Face models have token limits
    sentiment = results[0]["label"]
    score = results[0]["score"]

    if sentiment == "POSITIVE":
        return {"Positive": score * 100, "Neutral": 100 - score * 100, "Negative": 0}
    elif sentiment == "NEGATIVE":
        return {"Positive": 0, "Neutral": 100 - score * 100, "Negative": score * 100}
    else:
        return {"Positive": 0, "Neutral": 100, "Negative": 0}

# Google Cloud Sentiment Analysis
def analyze_sentiment_google(convo):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=convo, type_=language_v1.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(request={"document": document}).document_sentiment
    score = sentiment.score  # Ranges from -1 (negative) to 1 (positive)

    positive = max(0, score) * 100
    negative = abs(min(0, score)) * 100
    neutral = 100 - (positive + negative)

    return {"Positive": positive, "Neutral": neutral, "Negative": negative}

# OpenAI GPT-4-turbo for Issue Detection
def analyze_issues_gpt(convo):
    response = client.chat.completions.create(model="gpt-4-turbo",
    messages=[
        {"role": "system", "content": "Analyze this conversation for relationship issues such as gaslighting, passive aggression, stonewalling, and defensiveness. Return counts of each issue."},
        {"role": "user", "content": convo}
    ])
    return response.choices[0].message.content

# Anthropic Claude for Issue Detection
def analyze_issues_claude(convo):
    client = anthropic.Anthropic(api_key=anthropic_key)
    response = client.messages.create(
        model="claude-3",
        max_tokens=500,
        messages=[{"role": "user", "content": f"Analyze this conversation for relationship issues: {convo}"}]
    )
    return response.content

# Main Analysis Function
def analyze_conversation(convo, name, partner_name, relationship, use_google_nlp=False, use_claude=False):
    # Sentiment Analysis (Choose Hugging Face or Google Cloud)
    sentiment = analyze_sentiment_google(convo) if use_google_nlp else analyze_sentiment_hf(convo)

    # Issue Detection (Choose GPT-4-turbo or Claude)
    issue_analysis = analyze_issues_claude(convo) if use_claude else analyze_issues_gpt(convo)

    # Parse issue analysis output (assuming JSON-like structure from GPT/Claude)
    import json
    try:
        issues = json.loads(issue_analysis)
    except:
        issues = {"Gaslighting": 0, "Passive Aggression": 0, "Stonewalling": 0, "Defensive Behavior": 0}

    # Compute Conversation Health Score
    health_score = 50 + (sentiment["Positive"] - sentiment["Negative"]) * 10 - (sum(issues.values()) * 5)
    health_score = max(0, min(100, health_score))

    # Communication Style Classification
    if sentiment["Positive"] > 60 and issues["Defensive Behavior"] == 0:
        style = "Collaborative"
    elif sentiment["Negative"] > 40:
        style = "Conflict-Prone"
    elif issues["Gaslighting"] > 0:
        style = "Manipulative"
    else:
        style = "Neutral"

    # Therapist Recommendations
    therapist_recs = []
    if issues["Gaslighting"] > 0:
        therapist_recs.append("Address gaslighting tendencies and work on open validation.")
    if issues["Passive Aggression"] > 0:
        therapist_recs.append("Learn direct communication to replace passive-aggressive remarks.")
    if issues["Stonewalling"] > 0:
        therapist_recs.append("Discuss healthy ways to express frustration instead of shutting down.")
    if issues["Defensive Behavior"] > 0:
        therapist_recs.append("Work on accepting constructive criticism without defensiveness.")

    return {
        "health_score": health_score,
        "sentiment": sentiment,
        "issues_detected": issues,
        "communication_style": style,
        "therapist_recommendations": therapist_recs
    }
