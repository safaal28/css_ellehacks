from textblob import TextBlob
import re

def analyze_conversation(convo, name, partner_name, relationship):
    # Sentiment Analysis
    sentiment_score = TextBlob(convo).sentiment.polarity  # Between -1 and 1
    positive = max(0, sentiment_score) * 100
    negative = abs(min(0, sentiment_score)) * 100
    neutral = 100 - (positive + negative)

    # Detect Issues
    issues = {
        "Gaslighting": len(re.findall(r"you're overreacting|that never happened", convo, re.I)),
        "Passive Aggression": len(re.findall(r"fine, whatever|I guess you're right", convo, re.I)),
        "Stonewalling": len(re.findall(r"silent treatment|I don't want to talk about it", convo, re.I)),
        "Defensive Behavior": len(re.findall(r"not my fault|you're the problem", convo, re.I))
    }

    # Conversation Health Score
    health_score = 50 + (positive - negative) * 10 - (sum(issues.values()) * 5)
    health_score = max(0, min(100, health_score))  # Keep score between 0-100

    # Communication Style Detection (Basic NLP Rule-Based)
    if positive > 60 and issues["Defensive Behavior"] == 0:
        style = "Collaborative"
    elif negative > 40:
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
        "sentiment": {"Positive": positive, "Neutral": neutral, "Negative": negative},
        "issues_detected": issues,
        "communication_style": style,
        "therapist_recommendations": therapist_recs
    }