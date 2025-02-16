from transformers import pipeline
from google.cloud import language_v1
import os
import streamlit as st
import cohere

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
cohere_key= os.getenv("COHERE_API_KEY")
print("cohere key", cohere_key)



# Hugging Face Sentiment Analysis
def analyze_sentiment_hf(convo):
    # have not supplied a mdel name, so it will use the default model
    print("inside hugging face function")
    sentiment_pipeline = pipeline("sentiment-analysis")
    results = sentiment_pipeline(convo[:512])  # Hugging Face models have token limits
    sentiment = results[0]["label"]
    score = results[0]["score"]
    print("score: ", score)

    print("analyzing sentiment via hugging face")
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

# Cohere api for Issue Detection
def analyze_issues_cohere(convo):
    co = cohere.Client(cohere_key)
    
    try:
        response = co.generate(
            model="command-r-plus", 
            prompt=f"Analyze this conversation for relationship issues such as Gaslighting, Passive Aggression, Stonewalling, and Defensiveness. Only return counts of each issue in JSON format:\n\n{convo}. Use exact key names.",
            max_tokens=500
        )

        if not response.generations or not response.generations[0].text:
            raise ValueError("Empty response from Cohere API")

        issue_analysis = response.generations[0].text.strip()  # Ensure no leading/trailing whitespace
        print("Issue analysis text: \n", issue_analysis)  # Add this line for debugging

        # Attempt to parse the JSON response
        import json
        issues = json.loads(issue_analysis)
        print("Parsed issues: ", issues)
        return issues

    except json.JSONDecodeError as e:
        print("JSONDecodeError: ", e)  # Add this line for debugging
        return {"Gaslighting": 0, "Passive Aggression": 0, "Stonewalling": 0, "Defensiveness": 0}
    except Exception as e:
        print("Exception: ", e)  # Add this line for debugging
        return {"Gaslighting": 0, "Passive Aggression": 0, "Stonewalling": 0, "Defensiveness": 0}
    

# Main Analysis Function
def analyze_conversation(convo, name, partner_name, relationship):
    # Sentiment Analysis (Choose Hugging Face or Google Cloud)
    sentiment = analyze_sentiment_hf(convo)

    # Issue Detection (Choose cohere or Claude)
    issue_analysis = analyze_issues_cohere(convo)
    print("Raw issue analysis response: \n", issue_analysis)  # Add this line for debugging

    # Parse issue analysis output (assuming JSON-like structure from cohere/Claude)
    import json
    try:
        issues = json.loads(issue_analysis)
        print("Parsed issues: ", issues)
        
    except json.JSONDecodeError as e:
        print("JSONDecodeError: ", e)  # Add this line for debugging
        issues = {"Gaslighting": 0, "Passive Aggression": 0, "Stonewalling": 0, "Defensiveness": 0}
    except Exception as e:
        print("Exception: ", e)  # Add this line for debugging
        issues = {"Gaslighting": 0, "Passive Aggression": 0, "Stonewalling": 0, "Defensiveness": 0}
        
    print("Issues: ", issues)
    # Compute Conversation Health Score
    health_score = 50 + (sentiment["Positive"] - sentiment["Negative"]) * 10 - (sum(issues.values()) * 5)
    print("Health score: ", health_score)
    print("Sum of values: ", sum(issues.values()) * 5)
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
    if issues["Defensiveness"] > 0:
        therapist_recs.append("Work on accepting constructive criticism without defensiveness.")

    return {
        "health_score": health_score,
        "sentiment": sentiment,
        "issues_detected": issues,
        "communication_style": style,
        "therapist_recommendations": therapist_recs
    }
