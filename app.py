# EduVision AI Assistant – Full Integrated Version
# Includes: QA (PDF/Text), Voice QA, Emotion Detection, Summary, Fun Facts, Study Tips

import streamlit as st
import numpy as np
import pdfplumber
from deepface import DeepFace
from transformers import pipeline as hf_pipeline, AutoTokenizer
from optimum.intel.openvino import OVModelForQuestionAnswering
from deep_translator import GoogleTranslator
import speech_recognition as sr
from pydub import AudioSegment
import tempfile
from PIL import Image
import os
import random

# -------------------- Language Setup --------------------
langs = {
    "English": "en", "Hindi": "hi", "Kannada": "kn", "Tamil": "ta",
    "Telugu": "te", "French": "fr", "Spanish": "es", "German": "de"
}
st.set_page_config(page_title="EduVision AI", layout="wide")
st.title("\U0001F4DA EduVision AI – Smart Classroom Assistant")

st.sidebar.title("\U0001F310 Language & Uploads")
selected_lang = st.sidebar.selectbox("Select Language", list(langs.keys()))
lang_code = langs[selected_lang]

# Study tips based on emotion
study_tips = {
    "Happy": "You're in a great mood! Tackle difficult topics now.",
    "Sad": "Take a short break with music, then revise simple concepts.",
    "Angry": "Take deep breaths. Try reviewing flashcards calmly.",
    "Surprise": "Explore a new topic you're curious about!",
    "Fear": "You're stressed — summarize what you've learned so far.",
    "Disgust": "Clean your desk and refresh with a short break.",
    "Neutral": "Great time to revise or self-test calmly."
}

# Fun facts
fun_facts = [
    "Did you know? The human brain has about 86 billion neurons!",
    "Fun fact: Honey never spoils. You could eat 3000-year-old honey!",
    "Fun fact: Light from the Sun takes 8 minutes to reach Earth.",
    "Did you know? Water can boil and freeze at the same time in a vacuum!",
    "Fun fact: A day on Venus is longer than a year on Venus.",
    "Fun fact: Lightning is 5x hotter than the sun’s surface.",
    "Fun fact: Sea otters hold hands when they sleep.",
    "Fun fact: Your DNA could stretch from the sun to Pluto and back 17 times!",
    "Fun fact: Some turtles can breathe through their butts!",
    "Fun fact: Bananas are berries, but strawberries aren’t!"
] * 6  # Repeat to simulate 60 entries

def translate(text, to_lang):
    return GoogleTranslator(source='auto', target=to_lang).translate(text)

# -------------------- PDF Upload --------------------
uploaded_pdf = st.sidebar.file_uploader("\U0001F4C4 Upload PDF", type="pdf")
context = ""
if uploaded_pdf is not None:
    with pdfplumber.open(uploaded_pdf) as pdf:
        for page in pdf.pages:
            context += page.extract_text() + "\n"
    st.success("\u2705 PDF uploaded and text extracted.")
else:
    context = st.text_area("\U0001F4D8 Or paste context manually:",
        "Photosynthesis is the process by which green plants use sunlight to synthesize foods from carbon dioxide and water.")

# -------------------- Load Models --------------------
model_id = "helenai/distilbert-base-cased-distilled-squad-ov"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = OVModelForQuestionAnswering.from_pretrained(model_id)
qa_pipeline = hf_pipeline("question-answering", model=model, tokenizer=tokenizer)
summarizer = hf_pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
quiz_gen = hf_pipeline("text-generation", model="gpt2")

# -------------------- Helper Functions --------------------
def get_answer(question, context, lang_code):
    question_en = translate(question, "en") if lang_code != "en" else question
    context_en = translate(context, "en") if lang_code != "en" else context
    result = qa_pipeline(question=question_en, context=context_en)
    answer_en = result["answer"]
    return translate(answer_en, lang_code) if lang_code != "en" else answer_en

def generate_summary(text, lang_code):
    if not text.strip(): return "No content provided."
    if len(text.split()) < 30: return "Text too short to summarize."
    try:
        summary = summarizer(text[:1024], max_length=130, min_length=30, do_sample=False)[0]['summary_text']
        return translate(summary, lang_code) if lang_code != "en" else summary
    except Exception as e:
        return f"⚠️ Summarization error: {e}"

def generate_quiz_from_summary(summary_text, lang_code="en"):
    if not summary_text or summary_text.startswith("⚠️"):
        return ["⚠️ No valid summary to generate questions."]
    prompt = f"Generate 3 quiz questions with answers based on this summary:\n{summary_text}\nQ1:"
    try:
        output = quiz_gen(prompt, max_length=300, num_return_sequences=1)[0]["generated_text"]
        lines = output.split("\n")
        return [l.strip() for l in lines if l.strip().startswith(('Q', 'A'))][:6]
    except Exception as e:
        return [f"⚠️ Could not generate quiz: {e}"]

# -------------------- Text QA --------------------
question = st.text_input("\U0001F4D6 Enter your question:")
if st.button("\U0001F50D Get Answer"):
    if question.strip():
        answer = get_answer(question, context, lang_code)
        st.success(f"\U0001F9E0 Answer: {answer}")
    else:
        st.warning("❗ Please enter a question.")

# -------------------- Voice Question --------------------
st.markdown("### \U0001F399️ Upload voice question (wav, mp3, mp4)")
uploaded_audio = st.file_uploader("Upload Audio", type=["wav", "mp3", "mp4"])
if uploaded_audio:
    recognizer = sr.Recognizer()
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_audio.name)[1]) as temp_audio:
        temp_audio.write(uploaded_audio.read())
        try:
            audio = AudioSegment.from_file(temp_audio.name)
            wav_path = temp_audio.name + ".wav"
            audio.export(wav_path, format="wav")
            with sr.AudioFile(wav_path) as source:
                audio_data = recognizer.record(source)
                voice_text = recognizer.recognize_google(audio_data)
                st.success(f"✅ You said: {voice_text}")
                answer = get_answer(voice_text, context, lang_code)
                st.success(f"\U0001F9E0 Answer: {answer}")
        except Exception as e:
            st.error(f"❌ Audio processing failed: {e}")

# -------------------- Emotion Detection --------------------
st.markdown("### \U0001F4F8 Upload Your Image for Emotion Detection")
img_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
if img_file:
    image = Image.open(img_file)
    st.image(image, caption="Uploaded Image")
    img_array = np.array(image)
    try:
        result = DeepFace.analyze(img_array, actions=["emotion"], detector_backend="retinaface", enforce_detection=True)
        dominant = result[0]['dominant_emotion'].capitalize()
        st.success(f"\U0001F604 Dominant Emotion: {dominant}")
        st.markdown("### \U0001F50D Top 3 Emotions")
        sorted_emotions = sorted(result[0]['emotion'].items(), key=lambda x: x[1], reverse=True)[:3]
        for emo, score in sorted_emotions:
            st.info(f"**{emo.capitalize()}**: {score:.2f}%")
        st.sidebar.markdown("---")
        st.sidebar.markdown(f"### \U0001F4A1 Study Tip")
        st.sidebar.success(study_tips.get(dominant, "Stay focused and keep going!"))
        st.sidebar.markdown(f"### \U0001F680 Fun Fact")
        st.sidebar.info(random.choice(fun_facts))
    except Exception as e:
        st.error(f"⚠️ Emotion detection failed: {e}")

# -------------------- Summary + Quiz --------------------
st.markdown("### \U0001F4D0 Summary of Context")
summary = generate_summary(context, lang_code)
st.info(summary)

if st.button("\U0001F52E Generate Quiz"):
    with st.spinner("Creating quiz..."):
        quiz = generate_quiz_from_summary(summary, lang_code)
        for q in quiz:
            st.info(q)
