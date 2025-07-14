# 🎓 EduVision AI Assistant

**EduVision** is an intelligent, AI-powered classroom assistant built using Streamlit, OpenVINO, and other state-of-the-art tools. It enables students to interact with educational content via context-based question answering, PDF Q&A, voice queries, text summarization, emotion detection from images, and study tips based on mood — all with multilingual support.

---

## 🚀 Features

### 🧠 Main Panel
- **📘 Manual Q&A**: Type context and ask questions with accurate answers using OpenVINO QA model.
- **🎙️ Voice Q&A**: Upload `.wav` audio files and get answers via speech recognition.
- **📝 Text Summarization**: Summarize large blocks of text into concise notes.
- **😊 Emotion Detection**: Upload an image and detect your current mood using DeepFace.
- **🎯 Study Tips**: Get motivation or productivity tips based on your detected emotion.

### 🗂️ Sidebar Panel
- **📄 PDF Upload & Q&A**: Upload a study PDF and ask questions from its content.
- **🌐 Multilingual Support**: Translate all answers into Hindi, Kannada, Tamil, Telugu, or English.
- **🎉 Fun Facts**: Stay engaged with random, interesting study-related facts.

---

## 🧪 Technologies Used

| Function              | Technology                    |
|-----------------------|-------------------------------|
| UI                    | Streamlit                     |
| QA Model              | DistilBERT + OpenVINO         |
| Summarization         | DistilBART                    |
| Emotion Detection     | DeepFace + OpenCV             |
| Translation           | Deep Translator (Google API)  |
| PDF Handling          | pdfplumber                    |
| Voice Recognition     | SpeechRecognition (WAV input) |

---

## 📦 Installation

### 🔹 Install All Requirements

Use the `requirements.txt` file:

```bash
pip install -r requirements.txt
