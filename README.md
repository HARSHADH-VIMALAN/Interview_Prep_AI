# 🚀 InterviewPrep AI – AI-Powered Interview Preparation Platform

## 📌 Project Overview

InterviewPrep AI is an AI-powered interview preparation platform built with **Streamlit** that helps users improve their interview readiness through resume analysis, coding challenges, HR interview practice, voice interview evaluation, emotion analysis, and performance tracking. The application leverages **Groq LLM** to generate personalized feedback and recommendations across every stage of the interview process. :contentReference[oaicite:0]{index=0}

---

## 🎯 Features

- 📄 AI Resume Analyzer
- 💻 AI Coding Interview
- 🎤 AI Voice Interview
- 😊 AI Emotion Analysis
- 💼 AI HR Interview
- 📊 Performance Dashboard
- 📈 Overall Interview Readiness Score
- 📝 Resume-Based Interview Questions
- 🤖 AI Career Recommendations
- 📋 AI Code Review
- 📈 Progress Tracking
- ⭐ Personalized AI Feedback

---

## 🛠️ Technologies Used

- Python
- Streamlit
- Pandas
- NumPy
- Plotly
- PyMuPDF (fitz)
- Pillow
- Groq API
- Whisper Large v3
- JSON

---

## 🤖 AI Modules

### 📄 Resume Analyzer

- Resume text extraction from PDF
- ATS score calculation
- Technical skill extraction
- Resume strengths & weaknesses
- Missing skill identification
- Career recommendations
- Resume-based interview questions

### 💻 Coding Interview

- AI-generated coding questions
- Multiple programming languages
- Difficulty selection
- AI code evaluation
- Optimization suggestions
- Coding score analysis

### 🎤 Voice Interview

- Audio transcription using Whisper
- Communication skills evaluation
- Fluency assessment
- Grammar analysis
- Confidence scoring
- Professional interview feedback

### 😊 Emotion Detection

- Facial expression analysis
- Professional appearance review
- Interview readiness assessment
- AI-generated improvement suggestions

### 💼 HR Interview

- Common HR interview questions
- AI answer evaluation
- Confidence analysis
- Professionalism assessment
- Personalized HR feedback

### 📊 Performance Dashboard

- Overall readiness score
- Module-wise performance tracking
- Weekly progress visualization
- Final AI interview report

---

## 📁 Project Structure

```
InterviewPrep-AI/
│
├── app.py
├── groq_client.py
├── __init__.py      ← Empty file
├── css/
├── resume_parser.py
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/InterviewPrep-AI.git
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

or

```bash
pip install streamlit pandas numpy plotly pymupdf pillow groq
```

---

## 🔑 API Configuration (Required)

This project uses the **Groq API** for AI-powered interview analysis and **Whisper Large v3** for speech transcription.

Before running the application, **replace the placeholder API key with your own Groq API key** in the source code. The project contains a placeholder such as:

```python
GROQ_API_KEY = "YOUR_API_KEY"
```

Replace `"YOUR_API_KEY"` with your personal Groq API key before launching the application. :contentReference[oaicite:1]{index=1}

> **Note:** For security reasons, API keys are **not included** in this repository. Each user must obtain and configure their own API key.

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal (typically `http://localhost:8501`).

---

## 📊 Workflow

1. Launch the application
2. Choose an interview module
3. Upload your resume or voice response (if required)
4. Receive AI-powered analysis and feedback
5. Practice coding and HR interviews
6. Track your interview readiness
7. Review personalized recommendations for improvement

---

## 🚀 Future Enhancements

- Multi-language interview support
- Live webcam emotion detection
- AI mock interview simulation
- Company-specific interview preparation
- Resume version comparison
- Cloud deployment
- User authentication and progress history

---

## 👨‍💻 Author

**Harshadh Vimalan**

---

## ⭐ Support

If you found this project useful, please consider giving it a **⭐ Star** on GitHub!
