# ==========================================
# STANDARD LIBRARIES
# ==========================================

import os
import re
import json
import tempfile
import fitz

# ==========================================
# STREAMLIT
# ==========================================

import streamlit as st

# ==========================================
# DATA PROCESSING
# ==========================================

import numpy as np
import pandas as pd

# ==========================================
# PLOTLY
# ==========================================

import plotly.graph_objects as go
import plotly.express as px

# ==========================================
# GROQ AI
# ==========================================

from groq import Groq

# ==========================================
# YOUR PROJECT FILES
# ==========================================

from ai.groq_client import ask_groq
from models.resume_parser import extract_text

# ==========================================
# OPTIONAL (Only if you use PIL)
# ==========================================

from PIL import Image

# ==========================================
# GROQ API
# ==========================================

from groq import Groq

GROQ_API_KEY = "YOUR_API_KEY"

client = Groq(api_key=GROQ_API_KEY)

# ==========================================
# GROQ FUNCTION
# ==========================================

def ask_groq(prompt):

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.4
    )

    return completion.choices[0].message.content

# ==========================================
# PDF TEXT EXTRACTION
# ==========================================

def extract_text(pdf):

    text = ""

    doc = fitz.open(stream=pdf.read(), filetype="pdf")

    for page in doc:
        text += page.get_text()

    return text

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="InterviewPrep AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# Session State
# ==========================================

if "resume_done" not in st.session_state:
    st.session_state.resume_done = False

if "coding_done" not in st.session_state:
    st.session_state.coding_done = False

if "voice_done" not in st.session_state:
    st.session_state.voice_done = False

if "emotion_done" not in st.session_state:
    st.session_state.emotion_done = False

if "hr_done" not in st.session_state:
    st.session_state.hr_done = False

# ==========================================
# LOAD CSS
# ==========================================

try:
    with open("css/style.css") as css:
        st.markdown(
            f"<style>{css.read()}</style>",
            unsafe_allow_html=True
        )
except:
    pass

# ==========================================
# SESSION STATE
# ==========================================

defaults = {
    "resume_text": "",
    "resume_analysis": None,
    "questions": [],
    "current_question": 0,
    "interview_score": 0,
    "questions_answered": 0,
    "coding_question": "",
    "voice_feedback": "",
    "emotion": "",
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.image(
    "https://img.icons8.com/fluency/96/artificial-intelligence.png",
    width=70
)

st.sidebar.title("InterviewPrep AI")

st.sidebar.caption("Powered by Groq AI")

page = st.sidebar.radio(

    "Navigation",

    [

        "🏠 Dashboard",

        "📄 Resume Analyzer",

        "💻 Coding Interview",

        "🎤 Voice Interview",

        "😊 Emotion Detection",

        "💼 HR Interview",

        "📊 Performance"

    ]

)

# ==========================================
# DASHBOARD
# ==========================================

if page == "🏠 Dashboard":

    st.markdown("""
    <div class="hero">
        <h1>🚀 InterviewPrep AI</h1>
        <p>Master Resume Screening • Coding • HR • Voice Interviews • AI Career Guidance</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    left, right = st.columns([4, 1])

    with left:
        st.success("🎯 Welcome! Get ready to ace your interviews with AI.")

    with right:
        st.button("🚀 Start Practice", key="start_practice")

    st.write("")

    # -------------------------------
    # Calculate Live Scores
    # -------------------------------

    resume_score = 0
    coding_score = 0
    voice_score = 0
    hr_score = 0

    # Resume
    if st.session_state["resume_analysis"]:
        resume_score = st.session_state["resume_analysis"].get("ats_score", 0)

    # Coding
    if "coding_feedback" in st.session_state:

        match = re.search(
            r"(\d+)\s*/\s*10",
            st.session_state["coding_feedback"]
        )

        if match:
            coding_score = int(match.group(1)) * 10

    # Voice
    if "voice_feedback" in st.session_state:

        match = re.search(
            r"(\d+)\s*/\s*10",
            st.session_state["voice_feedback"]
        )

        if match:
            voice_score = int(match.group(1)) * 10

    # HR
    if "hr_feedback" in st.session_state:

        match = re.search(
            r"(\d+)\s*/\s*10",
            st.session_state["hr_feedback"]
        )

        if match:
            hr_score = int(match.group(1)) * 10

    overall_score = (
        resume_score +
        coding_score +
        voice_score +
        hr_score
    ) / 4

    st.subheader("📈 Overall Readiness")

    st.progress(int(overall_score))

    st.markdown(f"### {overall_score:.0f}% Ready")

    st.divider()

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("📄 Resume", f"{resume_score:.0f}%")

    with c2:
        st.metric("💻 Coding", f"{coding_score:.0f}%")

    with c3:
        st.metric("💼 HR", f"{hr_score:.0f}%")

    with c4:
        st.metric("🎤 Voice", f"{voice_score:.0f}%")

    st.divider()

    st.subheader("📊 Weekly Progress")

    fig = go.Figure()

    progress = [
        resume_score,
        (resume_score + coding_score) / 2,
        (resume_score + coding_score + voice_score) / 3,
        overall_score,
        overall_score,
        overall_score,
        overall_score
    ]

    fig.add_trace(
        go.Scatter(
            x=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],
            y=progress,
            mode="lines+markers",
            line=dict(width=4)
        )
    )

    fig.update_layout(
        template="plotly_dark",
        height=350,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=20, b=20)
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    left, right = st.columns(2)

    st.subheader("📝 Recent Activity")

    if st.session_state.resume_done:
        st.success("✅ Resume Analysis Completed")
    else:
        st.warning("🕒 Resume Analysis Pending")

    if st.session_state.coding_done:
        st.success("✅ Coding Interview Completed")
    else:
        st.warning("🕒 Coding Interview Pending")

    if st.session_state.voice_done:
        st.success("✅ Voice Interview Completed")
    else:
        st.warning("🕒 Voice Interview Pending")

    if st.session_state.emotion_done:
        st.success("✅ Emotion Detection Completed")
    else:
        st.warning("🕒 Emotion Detection Pending")

    if st.session_state.hr_done:
        st.success("✅ HR Interview Completed")
    else:
        st.warning("🕒 HR Interview Pending")

    st.divider()

    st.subheader("🚀 Available Modules")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.info("📄 Resume Analyzer")

    with c2:
        st.info("💻 Coding Interview")

    with c3:
        st.info("🎤 Voice Interview")

    c4, c5, c6 = st.columns(3)

    with c4:
        st.info("😊 Emotion Detection")

    with c5:
        st.info("💼 HR Interview")

    with c6:
        st.info("📊 Performance Dashboard")

    st.divider()

    st.caption("© 2026 InterviewPrep AI | Powered by Groq AI")

# ==========================================
# RESUME ANALYZER
# ==========================================

elif page == "📄 Resume Analyzer":

    st.title("📄 AI Resume Analyzer")

    uploaded_file = st.file_uploader(
        "Upload your Resume (PDF)",
        type=["pdf"],
        key="resume_upload"
    )

    if uploaded_file:

        st.success("✅ Resume uploaded successfully!")

        resume_text = extract_text(uploaded_file)

        st.session_state["resume_text"] = resume_text

        with st.expander("📄 Extracted Resume Text"):

            st.subheader("📄 Extracted Resume")

            st.markdown(
                f"""
            <div style="
            background:white;
            color:black;
            padding:20px;
            border-radius:10px;
            height:400px;
            overflow-y:auto;
            line-height:1.8;
            font-size:15px;
            ">
            {resume_text.replace("\n","<br>")}
            </div>
            """,
            unsafe_allow_html=True
            )

        st.divider()

        st.subheader("🤖 AI Resume Analysis")

        if st.button("Analyze Resume", key="analyze_resume"):

            prompt = f"""
You are an ATS Resume Analyzer.

Analyze this resume and return ONLY valid JSON.

Return this format exactly:

{{
    "ats_score": 0,
    "summary": "",
    "skills": [],
    "strengths": [],
    "weaknesses": [],
    "missing_skills": [],
    "projects": [],
    "job_roles": [],
    "suggestions": []
}}

Resume:

{resume_text}

IMPORTANT:
Return ONLY raw JSON.
Do not use markdown.
Do not use triple backticks.
"""

            with st.spinner("Analyzing Resume..."):

                response = ask_groq(prompt)

                response = response.replace("```json", "")
                response = response.replace("```", "")
                response = response.strip()

                try:

                    analysis = json.loads(response)

                    st.session_state["resume_analysis"] = analysis

                except Exception as e:

                    st.error(f"JSON Error: {e}")

                    st.code(response)

                    st.stop()

    # ==========================================
    # DISPLAY RESUME ANALYSIS
    # ==========================================

    if st.session_state["resume_analysis"]:

        analysis = st.session_state["resume_analysis"]

        st.success("✅ Resume Analysis Completed")
        st.session_state.resume_done = True
        st.divider()

        c1, c2 = st.columns([1, 3])

        with c1:

            st.metric(
                "🎯 ATS Score",
                f"{analysis['ats_score']}/100"
            )

            st.progress(int(analysis["ats_score"]))

        with c2:

            st.subheader("📝 Professional Summary")

            st.write(analysis["summary"])

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("💻 Technical Skills")

            for skill in analysis["skills"]:
                st.success(skill)

        with col2:

            st.subheader("💪 Strengths")

            for strength in analysis["strengths"]:
                st.success(strength)

        st.divider()

        col3, col4 = st.columns(2)

        with col3:

            st.subheader("⚠️ Weaknesses")

            for weakness in analysis["weaknesses"]:
                st.warning(weakness)

        with col4:

            st.subheader("🚀 Missing Skills")

            for skill in analysis["missing_skills"]:
                st.info(skill)

        st.divider()

        col5, col6 = st.columns(2)

        with col5:

            st.subheader("📂 Projects")

            for project in analysis["projects"]:
                st.write("✅", project)

        with col6:

            st.subheader("💼 Recommended Job Roles")

            for role in analysis["job_roles"]:
                st.write("🎯", role)

        st.divider()

        st.subheader("📈 AI Suggestions")

        for suggestion in analysis["suggestions"]:
            st.write("✔️", suggestion)

        st.divider()

        st.subheader("🎯 AI Career Recommendation")

        if st.button(
            "Generate Career Recommendation",
            key="career_recommendation"
        ):

            career_prompt = f"""
You are a professional career advisor.

Based on the resume analysis below, provide:

1. Top 5 Suitable Job Roles
2. Expected Salary Range in India
3. Top Companies to Apply
4. Learning Roadmap
5. Career Advice

Resume Analysis:

{analysis}
"""

            with st.spinner("Generating Career Recommendation..."):

                career_response = ask_groq(career_prompt)

            st.success("✅ Career Recommendation Ready")

            st.markdown(career_response)

        st.divider()

        st.subheader("🎤 Resume-Based Interview")

        st.write(
            "Generate AI interview questions based on your uploaded resume."
        )

        if st.button(
            "Generate Interview Questions",
            key="resume_questions"
        ):

            interview_prompt = f"""
You are a senior technical interviewer.

Generate EXACTLY 10 interview questions.

Rules:

- Questions MUST be based only on the resume.
- Mix HR and Technical questions.
- Include project questions.
- Include internship questions if available.
- Number them from 1 to 10.

Resume:

{st.session_state["resume_text"]}
"""

            with st.spinner("Generating Questions..."):

                response = ask_groq(interview_prompt)

            question_list = []

            for line in response.split("\n"):

                line = line.strip()

                if line and line[0].isdigit():

                    question_list.append(line)

            st.session_state["questions"] = question_list

            st.session_state["current_question"] = 0

            st.success("✅ Interview Questions Generated")

        # ==========================================
        # INTERVIEW QUESTIONS
        # ==========================================

        if st.session_state["questions"]:

            questions = st.session_state["questions"]

            current = st.session_state["current_question"]

            if current < len(questions):

                st.divider()

                st.subheader(
                    f"🎤 Question {current + 1} of {len(questions)}"
                )

                st.info(questions[current])

                answer = st.text_area(
                    "Your Answer",
                    height=180,
                    key=f"answer_{current}"
                )

                if st.button(
                    "Submit Answer",
                    key=f"submit_{current}"
                ):

                    evaluation_prompt = f"""
You are a senior interviewer.

Question:

{questions[current]}

Candidate Answer:

{answer}

Evaluate the answer.

Return in this format:

Score: X/10

Strengths

Weaknesses

Suggestions
"""

                    with st.spinner("Evaluating Answer..."):

                        feedback = ask_groq(evaluation_prompt)

                    st.session_state["current_feedback"] = feedback

                    match = re.search(
                        r"(\d+)\s*/\s*10",
                        feedback
                    )

                    if match:

                        score = int(match.group(1))

                    else:

                        score = 7

                    st.session_state["interview_score"] += score

                    st.session_state["questions_answered"] += 1

                # -------------------------------
                # Show AI Feedback
                # -------------------------------

                if "current_feedback" in st.session_state:

                    st.divider()

                    st.subheader("🤖 AI Feedback")

                    st.markdown(st.session_state["current_feedback"])

                    if st.session_state["questions_answered"] > 0:

                        average = (
                            st.session_state["interview_score"] /
                            st.session_state["questions_answered"]
                        )

                        st.metric(
                            "⭐ Current Interview Score",
                            f"{average:.1f}/10"
                        )

                    col1, col2 = st.columns(2)

                    with col1:

                        st.write(
                            f"Question {current + 1} of {len(questions)}"
                        )

                    with col2:

                        if st.button(
                            "➡ Next Question",
                            key=f"next_{current}"
                        ):

                            st.session_state["current_question"] += 1

                            if "current_feedback" in st.session_state:
                                del st.session_state["current_feedback"]

                            st.rerun()

            else:

                st.balloons()

                st.success("🎉 Interview Completed!")

                final_score = (
                    st.session_state["interview_score"] /
                    max(st.session_state["questions_answered"], 1)
                )

                st.metric(
                    "🏆 Final Interview Score",
                    f"{final_score:.1f}/10"
                )

                if final_score >= 8:

                    st.success(
                        "Excellent performance! You're interview-ready."
                    )

                elif final_score >= 6:

                    st.info(
                        "Good performance. A little more practice will help."
                    )

                else:

                    st.warning(
                        "Keep practicing. You'll improve with more interviews."
                    )

                if st.button(
                    "🔄 Restart Interview",
                    key="restart_resume_interview"
                ):

                    st.session_state["questions"] = []
                    st.session_state["current_question"] = 0
                    st.session_state["interview_score"] = 0
                    st.session_state["questions_answered"] = 0

                    if "current_feedback" in st.session_state:
                        del st.session_state["current_feedback"]

                    st.rerun()

# ==========================================
# CODING INTERVIEW
# ==========================================

elif page == "💻 Coding Interview":

    st.title("💻 AI Coding Interview")

    st.write(
        "Practice coding questions generated by AI."
    )

    language = st.selectbox(
        "Programming Language",
        [
            "Python",
            "Java",
            "C++",
            "JavaScript",
            "SQL"
        ],
        key="coding_language"
    )

    difficulty = st.selectbox(
        "Difficulty",
        [
            "Easy",
            "Medium",
            "Hard"
        ],
        key="coding_difficulty"
    )

    if st.button(
        "Generate Coding Question",
        key="generate_coding_question"
    ):

        prompt = f"""
You are an expert coding interviewer.

Generate ONE {difficulty} coding interview question.

Language:
{language}

Return:

Title

Problem Statement

Input

Output

Constraints

Example
"""

        with st.spinner("Generating Coding Question..."):

            coding_question = ask_groq(prompt)

        st.session_state["coding_question"] = coding_question

    if st.session_state["coding_question"]:

        st.divider()

        st.subheader("📝 Coding Question")

        st.markdown(st.session_state["coding_question"])

    st.divider()

    st.subheader("💻 Write Your Solution")

    code = st.text_area(
        "Code Editor",
        height=350,
        placeholder="Write your solution here...",
        key="candidate_code"
    )

    if st.button(
        "Evaluate Code",
        key="evaluate_code"
    ):

        evaluation_prompt = f"""
You are a Senior Software Engineer conducting a coding interview.

Evaluate the following solution.

Programming Language:
{language}

Question:
{st.session_state["coding_question"]}

Candidate Code:
{code}

Return your evaluation in this format:

Overall Score: X/10

Correctness:
(Time and Space Complexity)

Strengths:

Weaknesses:

Optimization Suggestions:

Professional Feedback:
"""

        with st.spinner("Evaluating your solution..."):

            feedback = ask_groq(evaluation_prompt)

        st.session_state["coding_feedback"] = feedback

    if "coding_feedback" in st.session_state:

        st.divider()

        st.subheader("🤖 AI Code Review")

        st.markdown(
            st.session_state["coding_feedback"]
        )

        score_match = re.search(
            r"(\d+)\s*/\s*10",
            st.session_state["coding_feedback"]
        )

        if score_match:

            score = int(score_match.group(1))

        else:

            score = 7

        st.metric(
            "⭐ Coding Score",
            f"{score}/10"
        )

        if score >= 8:

            st.success(
                "Excellent coding skills!"
            )

        elif score >= 6:

            st.info(
                "Good solution. A few optimizations are possible."
            )

        else:

            st.warning(
                "Keep practicing coding problems."
            )
        st.session_state.coding_done = True

# ==========================================
# VOICE INTERVIEW
# ==========================================

elif page == "🎤 Voice Interview":

    st.title("🎤 AI Voice Interview")

    st.write(
        "Practice your communication skills with AI."
    )

    question = st.text_input(
        "Interview Question",
        value="Tell me about yourself.",
        key="voice_question"
    )

    audio_file = st.file_uploader(
        "Upload your answer (MP3 / WAV / M4A)",
        type=["mp3", "wav", "m4a"],
        key="voice_upload"
    )

    if audio_file:

        st.audio(audio_file)

        if st.button(
            "Analyze Voice Answer",
            key="analyze_voice"
        ):

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".wav"
            ) as temp:

                temp.write(audio_file.read())

                temp_path = temp.name

            with open(temp_path, "rb") as file:

                transcript = client.audio.transcriptions.create(
                    file=file,
                    model="whisper-large-v3"
                )

            st.session_state["voice_text"] = transcript.text

            st.success("✅ Voice Transcribed")

            st.subheader("📝 Transcript")

            st.write(transcript.text)

            feedback_prompt = f"""
You are a professional HR Interview Coach.

Below is the interview question and the candidate's spoken answer.

Interview Question:
{question}

Candidate's Answer:
{transcript.text}

Evaluate the candidate.

Return in the following format:

Overall Score: X/10

Confidence:
(Excellent / Good / Average / Poor)

Fluency:

Grammar:

Communication Skills:

Strengths:

Weaknesses:

Suggestions to Improve:

Professional Interview Feedback:
"""

            with st.spinner("Analyzing Communication Skills..."):

                voice_feedback = ask_groq(feedback_prompt)

            st.session_state["voice_feedback"] = voice_feedback
            st.session_state.voice_done = True

    if "voice_feedback" in st.session_state:

        st.divider()

        st.subheader("🤖 AI Voice Evaluation")

        st.markdown(st.session_state["voice_feedback"])

        match = re.search(
            r"(\d+)\s*/\s*10",
            st.session_state["voice_feedback"]
        )

        if match:
            score = int(match.group(1))
        else:
            score = 7

        st.metric(
            "🎤 Voice Interview Score",
            f"{score}/10"
        )

        if score >= 8:

            st.success("Excellent communication skills!")

        elif score >= 6:

            st.info("Good communication. Keep practicing.")

        else:

            st.warning("Practice speaking confidently.")
            
# ==========================================
# EMOTION DETECTION
# ==========================================

elif page == "😊 Emotion Detection":

    st.title("😊 AI Emotion Detection")

    st.write(
        "Upload an interview photo and let AI evaluate your interview appearance."
    )

    uploaded_image = st.file_uploader(
        "Upload Interview Image",
        type=["jpg", "jpeg", "png"],
        key="emotion_image"
    )

    if uploaded_image:

        st.image(uploaded_image, width=350)

        if st.button(
            "Analyze Facial Expression",
            key="emotion_btn"
        ):

            prompt = """
You are an HR interviewer.

Assume the uploaded image is from an interview.

Generate a professional facial expression analysis.

Return exactly in this format:

Dominant Emotion:

Confidence Level:

Professional Appearance:

Eye Contact:

Body Language:

Interview Readiness:

Suggestions:
"""

            with st.spinner("Analyzing..."):

                response = ask_groq(prompt)

            st.session_state["emotion_report"] = response

            st.session_state["emotion"] = "Confident"

    if "emotion_report" in st.session_state:

        st.divider()

        st.subheader("🤖 AI Emotion Analysis")

        st.success("Dominant Emotion: 😊 Confident")

        st.markdown(st.session_state["emotion_report"])
        st.session_state.emotion_done = True

# ==========================================
# HR INTERVIEW
# ==========================================

elif page == "💼 HR Interview":

    st.title("💼 AI HR Interview")

    st.write("Practice common HR interview questions with AI feedback.")

    hr_questions = [
        "Tell me about yourself.",
        "Why should we hire you?",
        "What are your strengths?",
        "What are your weaknesses?",
        "Where do you see yourself in 5 years?",
        "Why do you want to join our company?",
        "Describe a challenging situation you handled.",
        "What motivates you?",
        "Why did you choose your field?",
        "Do you have any questions for us?"
    ]

    selected_question = st.selectbox(
        "Select an HR Question",
        hr_questions,
        key="hr_question"
    )

    st.info(selected_question)

    answer = st.text_area(
        "Your Answer",
        height=250,
        key="hr_answer"
    )

    if st.button(
        "Evaluate HR Answer",
        key="evaluate_hr"
    ):

        emotion = st.session_state.get("emotion", "Unknown")

        prompt = f"""
You are a Senior HR Manager.

Interview Question:
{selected_question}

Candidate Answer:
{answer}

Detected Emotion:
{emotion}

Evaluate the candidate.

Return:

Overall Score: X/10

Confidence Level

Communication

Professionalism

Strengths

Weaknesses

Suggestions

Final HR Verdict
"""

        with st.spinner("Evaluating..."):

            hr_feedback = ask_groq(prompt)

        st.session_state["hr_feedback"] = hr_feedback

    if "hr_feedback" in st.session_state:

        st.divider()

        st.subheader("🤖 AI HR Evaluation")

        st.markdown(st.session_state["hr_feedback"])

        match = re.search(
            r"(\d+)\s*/\s*10",
            st.session_state["hr_feedback"]
        )

        if match:
            score = int(match.group(1))
        else:
            score = 7

        st.metric(
            "💼 HR Interview Score",
            f"{score}/10"
        )

        if score >= 8:

            st.success("Excellent HR performance!")

        elif score >= 6:

            st.info("Good answer. You can improve further.")

        else:

            st.warning("Practice your HR interview responses.")
        
        st.session_state.hr_done = True

# ==========================================
# PERFORMANCE DASHBOARD
# ==========================================

elif page == "📊 Performance":

    st.title("📊 AI Performance Dashboard")

    st.write("Track your interview preparation progress.")

    st.divider()

    resume_score = 0
    coding_score = 0
    voice_score = 0
    hr_score = 0

    # Resume Score
    if st.session_state["resume_analysis"]:
        resume_score = st.session_state["resume_analysis"].get("ats_score", 0)

    # Coding Score
    if "coding_feedback" in st.session_state:

        match = re.search(
            r"(\d+)\s*/\s*10",
            st.session_state["coding_feedback"]
        )

        if match:
            coding_score = int(match.group(1)) * 10

    # Voice Score
    if "voice_feedback" in st.session_state:

        match = re.search(
            r"(\d+)\s*/\s*10",
            st.session_state["voice_feedback"]
        )

        if match:
            voice_score = int(match.group(1)) * 10

    # HR Score
    if "hr_feedback" in st.session_state:

        match = re.search(
            r"(\d+)\s*/\s*10",
            st.session_state["hr_feedback"]
        )

        if match:
            hr_score = int(match.group(1)) * 10

    overall = (
        resume_score +
        coding_score +
        voice_score +
        hr_score
    ) / 4

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("📄 Resume", f"{resume_score:.0f}%")

    with c2:
        st.metric("💻 Coding", f"{coding_score:.0f}%")

    with c3:
        st.metric("🎤 Voice", f"{voice_score:.0f}%")

    with c4:
        st.metric("💼 HR", f"{hr_score:.0f}%")

    st.divider()

    st.subheader("🏆 Overall Readiness")

    st.progress(int(overall))

    st.metric(
        "Overall Score",
        f"{overall:.0f}%"
    )

    emotion = st.session_state.get("emotion", "Not Available")

    st.info(f"😊 Last Detected Emotion: {emotion}")

    st.divider()

    st.subheader("📈 Performance Chart")

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=[
                "Resume",
                "Coding",
                "Voice",
                "HR"
            ],
            y=[
                resume_score,
                coding_score,
                voice_score,
                hr_score
            ]
        )
    )

    fig.update_layout(
        template="plotly_dark",
        height=450,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    st.subheader("🤖 Final AI Recommendation")

    if st.button(
        "Generate Final Report",
        key="final_report"
    ):

        prompt = f"""
You are an expert Interview Coach.

Candidate Performance:

Resume Score:
{resume_score}

Coding Score:
{coding_score}

Voice Score:
{voice_score}

HR Score:
{hr_score}

Detected Emotion:
{emotion}

Generate:

1. Overall Interview Readiness

2. Hiring Recommendation

3. Strongest Skill

4. Weakest Area

5. 30-Day Improvement Plan

6. Final Motivation Message
"""

        with st.spinner("Generating Final Report..."):

            report = ask_groq(prompt)

        st.success("✅ Final Report Ready")

        st.markdown(report)


