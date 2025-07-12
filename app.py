import streamlit as st
import torch
import numpy as np
import cv2
import time
import speech_recognition as sr
from deepface import DeepFace  # ✅ Using DeepFace for emotion detection
from transformers import pipeline as hf_pipeline, AutoTokenizer
from optimum.intel.openvino import OVModelForQuestionAnswering
import pdfplumber
from deep_translator import GoogleTranslator

# -------------------- Language & Translation Setup --------------------
langs = {
    "English": "en", "Hindi": "hi", "Kannada": "kn", "Tamil": "ta",
    "Telugu": "te", "French": "fr", "Spanish": "es", "German": "de"
}
st.sidebar.title("🌐 Language & Uploader")
selected_lang = st.sidebar.selectbox("Select Language", list(langs.keys()))
lang_code = langs[selected_lang]

def translate(text, to_lang):
    return GoogleTranslator(source='auto', target=to_lang).translate(text)

# -------------------- Study Tip on Sidebar --------------------
st.sidebar.markdown("### 💡 Study Tip")
st.sidebar.info("📘 Tip: Stay focused, take short breaks, and review summaries regularly!")

# -------------------- PDF Upload --------------------
uploaded_pdf = st.sidebar.file_uploader("📄 Upload PDF", type="pdf")
context = ""

if uploaded_pdf is not None:
    with pdfplumber.open(uploaded_pdf) as pdf:
        for page in pdf.pages:
            context += page.extract_text() + "\n"
    st.success("✅ PDF uploaded and text extracted.")
else:
    context = st.text_area("📙 Context", 
        "Photosynthesis is the process by which green plants use sunlight to synthesize foods from carbon dioxide and water.")

# -------------------- Load OpenVINO QA Model --------------------
model_id = "helenai/distilbert-base-cased-distilled-squad-ov"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = OVModelForQuestionAnswering.from_pretrained(model_id)
qa_pipeline = hf_pipeline("question-answering", model=model, tokenizer=tokenizer)

# -------------------- Load Summarizer and Quiz Model --------------------
summarizer = hf_pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
quiz_gen = hf_pipeline("text-generation", model="gpt2")

# -------------------- Functions --------------------
def get_answer(question, context, lang_code):
    question_en = translate(question, "en") if lang_code != "en" else question
    context_en = translate(context, "en") if lang_code != "en" else context
    result = qa_pipeline(question=question_en, context=context_en)
    answer_en = result["answer"]
    return translate(answer_en, lang_code) if lang_code != "en" else answer_en

def give_study_tip(emotion, speed):
    if emotion in ["sad", "angry"] or speed < 1.5:
        return "🌱 Take a short break, hydrate, and revisit with fresh energy."
    elif emotion == "happy" and speed > 2.5:
        return "🚀 You're doing great! Keep up the momentum!"
    else:
        return "📘 Try reviewing summaries or flashcards for better retention."

def generate_summary(text, target_lang_code="en"):
    if not text.strip():
        return "No content provided."
    if len(text.split()) < 30:
        return "Text too short to summarize."
    try:
        raw_summary = summarizer(text[:1024], max_length=130, min_length=30, do_sample=False)[0]['summary_text']
        return translate(raw_summary, target_lang_code) if target_lang_code != "en" else raw_summary
    except Exception as e:
        return f"⚠️ Could not summarize: {e}"

def generate_quiz_from_summary(summary_text, lang_code="en"):
    if not summary_text or summary_text.startswith("⚠️"):
        return ["⚠️ No valid summary to generate questions."]

    prompt = (
        "Generate 3 simple quiz questions (with answers) based on this summary:\n\n"
        f"{summary_text}\n\n"
        "Format:\nQ1: ...?\nA1: ...\nQ2: ...?\nA2: ...\nQ3: ...?\nA3: ..."
    )
    try:
        output = quiz_gen(prompt, max_length=200, num_return_sequences=1)[0]["generated_text"]
        questions = []
        lines = output.split("\n")
        for line in lines:
            if line.strip().startswith("Q") or line.strip().startswith("A"):
                questions.append(line.strip())
        return questions
    except Exception as e:
        return [f"⚠️ Could not generate quiz: {e}"]

# -------------------- Streamlit UI --------------------
st.set_page_config(page_title="EduVision", page_icon="🧠")
st.title("🎓 EduVision AI Assistant")
st.markdown("Ask your question via **text or voice**, and I’ll help you out!")

# -------------------- Text QA --------------------
question = st.text_input("📄 Enter your question here:")
if st.button("🔍 Get Answer"):
    if question.strip():
        answer = get_answer(question, context, lang_code)
        st.success(f"🧠 Answer: {answer}")
    else:
        st.warning("Please enter a valid question!")

# -------------------- Voice QA --------------------
st.markdown("🎤 Or record your question:")
if st.button("🎧 Start Recording"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎧 Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=15)
            voice_question = recognizer.recognize_google(audio)
            st.success(f"✅ You said: {voice_question}")
            answer = get_answer(voice_question, context, lang_code)
            st.success(f"🧠 Answer: {answer}")
        except Exception as e:
            st.error(f"❌ Voice Recognition Failed: {e}")

# -------------------- Emotion Detection via DeepFace --------------------
# Emotion Detection via DeepFace
if st.button("📷 Check Engagement"):
    st.info("⏳ Capturing emotion from webcam...")
    cap = cv2.VideoCapture(0)
    time.sleep(10)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        st.error("❌ Failed to capture image.")
    else:
        st.image(frame, caption="Captured Frame", channels="BGR")
        cv2.imwrite("temp.jpg", frame)

        try:
            result = DeepFace.analyze("temp.jpg", actions=["emotion"], enforce_detection=False)
            dominant = result[0]['dominant_emotion']
            st.success(f"😃 Dominant Emotion: {dominant}")

            st.markdown("### 🔍 Top Emotions:")
            sorted_emotions = sorted(result[0]['emotion'].items(), key=lambda x: x[1], reverse=True)
            for emo, score in sorted_emotions[:3]:
                st.info(f"**{emo.capitalize()}**: {score:.2f}%")
        except Exception as e:
            st.error(f"Emotion Detection Error: {e}")


# -------------------- Summary --------------------
st.markdown("### 📔 Summary of the Provided Context")
summary = generate_summary(context, lang_code)
st.info(summary)

# -------------------- Quiz Generator --------------------
if st.button("🧪 Generate Quiz from Summary"):
    with st.spinner("Generating quiz..."):
        quiz = generate_quiz_from_summary(summary, lang_code)
        st.markdown("### 📘 AI-Generated Quiz")
        for item in quiz:
            st.info(item)
