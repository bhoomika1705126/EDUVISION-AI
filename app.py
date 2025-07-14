%%writefile app.py
import streamlit as st
import pdfplumber
from deepface import DeepFace
from transformers import pipeline, AutoTokenizer
from optimum.intel.openvino import OVModelForQuestionAnswering
from deep_translator import GoogleTranslator
import numpy as np
from PIL import Image
import torch
import random
import speech_recognition as sr

# -------------------------------
# Load QA Model
# -------------------------------
@st.cache_resource
def load_qa_model():
    tokenizer = AutoTokenizer.from_pretrained("distilbert-base-cased-distilled-squad")
    model = OVModelForQuestionAnswering.from_pretrained("distilbert-base-cased-distilled-squad", export=True)
    qa_pipeline = pipeline("question-answering", model=model, tokenizer=tokenizer)
    return qa_pipeline

qa_pipeline = load_qa_model()

# -------------------------------
# Load Summarizer
# -------------------------------
@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

summarizer = load_summarizer()

# -------------------------------
# Sidebar
# -------------------------------
st.sidebar.title("📂 EduVision Sidebar")

# PDF Upload
pdf_file = st.sidebar.file_uploader("Upload a PDF", type=["pdf"])
pdf_text = ""
if pdf_file:
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                pdf_text += text

# Language Selection
language = st.sidebar.selectbox("🌐 Translate answers to:", ["English", "Hindi", "Kannada", "Telugu", "Tamil"])
lang_code = {"English": "en", "Hindi": "hi", "Kannada": "kn", "Telugu": "te", "Tamil": "ta"}[language]

# PDF QA
st.sidebar.subheader("📄 Ask Question from PDF")
pdf_question = st.sidebar.text_input("Ask a question from PDF:")
if st.sidebar.button("Get PDF Answer"):
    if pdf_text and pdf_question:
        result = qa_pipeline(question=pdf_question, context=pdf_text)
        answer = result["answer"]
        translated = GoogleTranslator(source='auto', target=lang_code).translate(answer)
        st.sidebar.success(f"Answer: {translated}")
    else:
        st.sidebar.warning("Please upload a PDF and enter a question.")

# -------------------------------
# Right Column – Fun Facts
# -------------------------------
with st.sidebar.expander("🎉 Fun Study Facts"):
    facts = [
        "💡 Studying in short bursts (Pomodoro) improves focus!",
        "🧠 Teaching others helps you remember better!",
        "📚 Reading aloud improves memory retention!",
        "🛌 Sleep helps consolidate learning overnight!",
        "🖊️ Writing notes by hand improves recall!",
        "🎶 Classical music may boost concentration!",
        "🏃 Short walks improve brain function!",
        "🍎 Healthy snacks fuel better focus!",
    ]
    st.markdown(f"**{random.choice(facts)}**")

# -------------------------------
# Main Panel
# -------------------------------
st.title("🎓 EduVision AI Assistant")

# --- Context Q&A ---
st.subheader("📘 Ask a Question from Custom Context")
context = st.text_area("Enter the context here:")
question = st.text_input("Enter your question:")

if st.button("Get Answer"):
    if context and question:
        result = qa_pipeline(question=question, context=context)
        answer = result["answer"]
        translated = GoogleTranslator(source='auto', target=lang_code).translate(answer)
        st.success(f"Answer: {translated}")
    else:
        st.warning("Please enter both context and question.")

# --- Audio File Upload for Voice Q&A ---
st.subheader("🎙️ Ask a Question via Audio File")
audio_file = st.file_uploader("Upload a .wav file of your voice question", type=["wav"])
if audio_file:
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        try:
            spoken_question = recognizer.recognize_google(audio_data)
            st.write(f"You asked: **{spoken_question}**")
            if context:
                result = qa_pipeline(question=spoken_question, context=context)
                answer = result["answer"]
                translated = GoogleTranslator(source='auto', target=lang_code).translate(answer)
                st.success(f"Answer: {translated}")
            else:
                st.warning("Please enter context above to answer voice-based question.")
        except Exception as e:
            st.error(f"Could not understand audio: {e}")

# --- Text Summarization ---
st.subheader("📝 Text Summarization")
text_to_summarize = st.text_area("Paste text to summarize:")
if st.button("Summarize"):
    if text_to_summarize:
        summary = summarizer(text_to_summarize, max_length=120, min_length=30, do_sample=False)[0]['summary_text']
        translated = GoogleTranslator(source='auto', target=lang_code).translate(summary)
        st.success(f"Summary: {translated}")
    else:
        st.warning("Please enter text to summarize.")

# --- Emotion Detection ---
st.subheader("😊 Emotion Detection from Image")
image_file = st.file_uploader("Upload a photo (jpg/png)", type=["jpg", "jpeg", "png"])
if image_file:
    image = Image.open(image_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    img_array = np.array(image.convert("RGB"))
    emotion = None
    try:
        result = DeepFace.analyze(img_array, actions=['emotion'], enforce_detection=False)
        emotion = result[0]["dominant_emotion"]
        st.success(f"Detected Emotion: {emotion.capitalize()}")
    except Exception as e:
        st.error("Emotion detection failed. Try another image.")

    # 🎯 Study Tips Based on Emotion
    if emotion:
        tips = {
            "happy": "You're in a great mood! Try solving complex problems or revising key topics.",
            "sad": "Take a short break, listen to calming music, then focus on easy tasks.",
            "angry": "Do breathing exercises, walk a bit, then try some interactive quizzes.",
            "surprise": "Explore something new! Use your curiosity for learning.",
            "fear": "Take it slow. Start with confidence-building material.",
            "disgust": "Change topics or clean your space for a fresh start.",
            "neutral": "Perfect time for routine study or practice problems."
        }
        st.info(f"🎯 Study Tip: {tips.get(emotion, 'Stay focused and believe in yourself!')}")
    else:
        st.warning("No emotion detected.")
