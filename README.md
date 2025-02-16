# Delulu Detector

# 🫖 Your AI-Powered Relationship Health Indicator

Delulu Detector is a **Streamlit-based AI app** that helps individuals analyze their conversations for red flags, unhealthy patterns, and communication styles. It provides insights into **attachment styles, communication patterns**, and **conflicts** to promote healthier relationships among their romantic interests, siblings, parents, and friends. 

<img width="999" alt="Screenshot 2025-02-16 at 2 38 41 AM" src="https://github.com/user-attachments/assets/4ea0e9e3-c01d-49ee-83e8-95e8acdb4459" />

---

## 🚀 Features

✅ **Real-Time Conversation Analysis** – Record a conversation for AI-driven analysis  
✅ **Communication Styles Detection** – Identifies passive, passive-aggressive, aggressive, and assertive patterns  
✅ **Sentiment Scoring** – Evaluates emotional tone throughout the conversation  
✅ **Attachment Style Classification** – Determines secure, anxious, avoidant, or fearful attachment tendencies  
✅ **Issue Detection** – Red flags (gaslighting, manipulation, defensiveness, and stonewalling) and green flags (active listening, positive affirmations)
✅ **PDF Report Export** – Generates a PDF based on key discussion points and identified patterns for relationship counseling or for later review

---

## 🏗️ Tech Stack

- **Frontend:** Streamlit (Python)
- **Backend:** FastAPI (or Flask for quick deployment)
- **AI Models:** OpenAI GPT-4, BERT, or SpaCy for NLP-based sentiment & communication analysis
- **Database:** PostgreSQL / Firebase (optional for saving history)
- **Deployment:** Streamlit Sharing, AWS, or Heroku

---

## 🛠️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/TeaTalk.git
cd TeaTalk
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Run the Streamlit App
```bash
streamlit run app.py
```

---

## 🔬 How the AI Works

1️⃣ **Speech-to-Text**: Converts recorded conversations into text (using Whisper API)  
2️⃣ **Text Preprocessing**: Cleans and tokenizes text using SpaCy  
3️⃣ **Sentiment & Communication Analysis**: Applies NLP models to detect tone, styles, and red flags  
4️⃣ **Attachment Style Mapping**: Matches speech patterns to known attachment behaviors  
5️⃣ **Report Generation**: Summarizes findings with therapy recommendations  

---

## 📊 Sample Report Output
**Example Summary:**  
🟢 **Overall Conversation Health Score:** 72% (Healthy but needs improvement)  
🗣 **Primary Communication Style:** Passive-Aggressive  
💬 **Key Issues Detected:** Gaslighting, Defensiveness  
📌 **Therapist Discussion Suggestions:** Boundaries, Emotional Validation  
📄 **Export as PDF**

---

## 🎯 Roadmap
- [ ] Improve conversation health scoring formula
- [ ] Support multi-language analysis
- [ ] Integrate with therapy platforms


### Contributors
- [Safa Al-Siaudi](linkedin.com/in/safa-al-siaudi)
- [Camillia Amin](linkedin.com/in/camillia-hanaan-amin)
- [Saadia Shahid](linkedin.com/in/saadia-shahid)
