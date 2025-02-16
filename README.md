
# Delulu Detector ❤️
![3](https://github.com/user-attachments/assets/77cb78f9-f9a0-48b4-8dfc-dda3a0e7c9df)

### The Solulu to Your Delulu
Delulu Detector is a **Streamlit-based AI app** that helps individuals analyze their conversations for red flags, unhealthy patterns, and communication styles. It provides insights into **attachment styles, communication patterns**, and **conflicts** to promote healthier relationships among their romantic interests, siblings, parents, friends, and more.

## Features

![5](https://github.com/user-attachments/assets/e6bdb7db-54d7-4ded-9720-4a0a94ea2bbd)
✅ **Real-Time Conversation Analysis** – Record a conversation for AI-driven analysis  
✅ **Communication Styles Detection** – Identifies passive, passive-aggressive, aggressive, and assertive patterns  
✅ **Sentiment Scoring** – Evaluates emotional tone throughout the conversation  
✅ **Attachment Style Classification** – Determines secure, anxious, avoidant, or fearful attachment tendencies  
✅ **Issue Detection** – Red flags (gaslighting, manipulation, etc.) and green flags (active listening, positive affirmations, etc.)<br>
✅ **PDF Report Export** – Generates a PDF based on key discussion points and identified patterns for relationship counseling or for later review

## How the App Works

1️⃣ **Speech-to-Text**: Converts recorded conversations into text using AssemblyAI and identifies each speaker  
2️⃣ **Text Preprocessing**: Cleans and tokenizes text using SpaCy, redacts PII such as names  
3️⃣ **Relationship Analysis**: Applies Cohere's Command R Plus model to identify attachment style, communication style, red and green flags  
4️⃣ **Results Output**: Exports findings as a PDF to share and disucss with their therapist  
5️⃣ **Observe Long-term Trends**: Compare relationship trends and reoccurring patterns over multiple conversations  

## Tech Stack
- **Frontend:** Streamlit
- **Backend:** Python, AssemblyAI
- **AI Model:** Cohere's Command R Plus

## Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/safaal28/css_ellehacks.git
cd css_ellehacks
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Run the Streamlit App
```bash
streamlit run App.py
```

## Technical Considerations

### Accuracy Testing
We created synthetic data to perform semi-automated, qualitative testing of our results based on 5 types of conversations. Each conversation was tested 5 times. Findings are displayed as follows:
| Input # | # of Trials | Score out of 5 | Conversation Health Summary | Attachment Style | Communication Pattern | Communication Insights | Red Flags | Green Flags |
|---------|--------|---------------|-----------------------------|------------------|----------------------|-----------------------|-----------|------------|
| 1       | 5      | 80%           | This relationship exhibits emotional neglect. Seeking therapy is advised. | Anxious-Preoccupied | Passive-Aggressive | Dominant speaker: Jason, frequent dismissive responses | Gaslighting, stonewalling | Apologies, attempt at clarity |
| 2       | 5      | 100%          | The conversation reflects a significant communication gap. Both parties are defensive, leading to emotional invalidation. | Anxious-Preoccupied	| Deflective, Defensive	| Dominant speaker: Parent, avoidance of deeper issues| Emotional invalidation, guilt-tripping, defensiveness	| Attempts to initiate communication, verbalized feelings of being unheard
| 3       | 5      | 60%           | This conversation demonstrates healthy communication. Both parties are open, receptive, and willing to find solutions. |	Secure |	Open, Collaborative	| Dominant speaker: Mia, empathetic responses, solution-oriented | None	| Active listening, willingness to resolve, setting future intentions

### Secure Use of GenAI


## Future Roadmap
- [ ] GenAI: Fine-tune Cohere's R Command Plus model with synthetic data for more accurate sentiment analysis
- [ ] Testing: Generate a higher volume of synthetic testing data, perform user testing
- [ ] Education: Partner with mental health educative platforms to incentivize user education  

### Contributors
- [Safa Al-Siaudi](linkedin.com/in/safa-al-siaudi)
- [Camillia Amin](linkedin.com/in/camillia-hanaan-amin)
- [Saadia Shahid](linkedin.com/in/saadia-shahid)

![13](https://github.com/user-attachments/assets/9d0095be-02db-4289-9ae9-cd78e7066452)



