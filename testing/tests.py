import csv
import json
import cohere
import markdown
import time

def generate_insights(conversation, co):
    prompt = f"""
    Analyze the following conversation and return structured JSON output with keys: 
    - "conversation_health"
    - "attachment_style"
    - "communication_patterns"
    - "communication_insights"
    - "red_flags"
    - "green_flags"
    
    Respond in valid JSON format only. No additional text.

    Conversation:
    '''{conversation}'''
    """
    
    response = co.generate(
        model="command-r-plus",  # Ensure correct model
        prompt=prompt,
        max_tokens=500,
        temperature=0.7
    )
    
    try:
        insights = json.loads(response.generations[0].text.strip())
    except json.JSONDecodeError:
        insights = {"error": "Invalid JSON received from API"}
    
    return insights

def run_analysis(input_file="synthetic_data.csv", output_file="results.md"):

    co = cohere.Client("COHERE_API_KEY")
    
    with open(input_file, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # Skip headers
        conversations = list(reader)
    
    results = []
    
    for input_num, conversation in conversations:
        for trial in range(1, 4):
            print(f"Processing Input #{input_num}, Trial #{trial}...")
            insights = generate_insights(conversation, co)
            results.append([input_num, trial] + list(insights.values()))
            time.sleep(1)  # Rate limit handling
    
    md_content = """# Conversation Analysis Results

| Input # | Trial # | Overall Score | Conversation Health Summary | Attachment Style | Communication Pattern | Communication Insights | Red Flags | Green Flags |
|---------|--------|--------------|----------------------------|------------------|-------------------|-------------------|-----------|------------|
"""
    
    for row in results:
        md_content += "| " + " | ".join(map(str, row)) + " |\n"
    
    with open(output_file, "w", encoding="utf-8") as md_file:
        md_file.write(md_content)
    
    print(f"Analysis saved to {output_file}")

# Run the pipeline
create_synthetic_data()
run_analysis()