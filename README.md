# 🎓 EduVision AI Assistant

EduVision is an intelligent learning assistant designed to help students interactively understand study materials. It supports **multilingual question answering**, **PDF-based learning**, **voice queries**, **emotion detection**, and **AI-generated summaries and quizzes**.

---

## 🚀 Features

- 📄 **PDF Upload** – Upload textbooks or notes and ask questions from the content.
- 🔍 **Multilingual QA** – Ask questions in your preferred language (Kannada, Hindi, Tamil, etc.)
- 🎧 **Voice Input** – Speak your question instead of typing.
- 📷 **Emotion Detection** – Uses webcam to check engagement level.
- 📘 **Summary Generator** – Summarizes content using AI.
- 🧪 **Quiz Generator** – Generates 3 simple MCQs from the topic.

---

## 🛠️ Installation Instructions

> Ensure you have Python 3.10 installed on your system.

### 1. Clone the repository:

```bash
git clone https://github.com/bhoomika1705126/EDUVISION-AI.git
cd EDUVISION-AI                         2.*Create Virtual Environment*
python -m venv venv
3.Activate the environment:
.\venv\Scripts\activate
4.Install dependencies:
pip install -r requirements.txt
5.Run the Application
streamlit run app.py
#Supported Languages
English
Hindi
Kannada
Tamil
Telugu
French
Spanish
German
#Tech Stack
Python
Streamlit
DeepFace
Transformers
OpenVINO
Torch
Deep Translator
PDFPlumber
OpenCV

🤖 AI Models Used
🤖 Question Answering: distilbert-base-cased-distilled-squad (OpenVINO optimized)

🧠 Summarization: sshleifer/distilbart-cnn-12-6

📚 Quiz Generation: GPT-2

😃 Emotion Detection: DeepFace + OpenCV

🧑‍💻 Developed by
Team ML Crew




