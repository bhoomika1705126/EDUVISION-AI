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
-----
 ## Images
Q&A with translation
IN English:<img width="1920" height="1080" alt="Screenshot (34)" src="https://github.com/user-attachments/assets/164c1ff7-ea5f-416f-addd-c203236d6236" />
IN Kannada:<img width="1920" height="1080" alt="Screenshot (35)" src="https://github.com/user-attachments/assets/ece1ddda-48e5-4b2e-b9ab-5a9894811bf5" />
------
## Emotion

<img width="1920" height="1080" alt="Screenshot (37)" src="https://github.com/user-attachments/assets/2ace97c1-1267-4293-ae20-5436c1409356" />

----
## Summary

<img width="1920" height="1080" alt="Screenshot (36)" src="https://github.com/user-attachments/assets/89a6a231-51f7-48fa-9072-39d7aea9511d" />

---

## 📦 Installation

### 🔹 Install All Requirements

Use the `requirements.txt` file:
 
```bash
pip install -r requirements.txt

▶️ Run the App Locally
streamlit run app.py

🌍 Run in Google Colab (via Ngrok)
Colab doesn’t allow direct browser access to Streamlit apps, so we use ngrok:

🔸 Step-by-step:

# Install requirements
!pip install -r requirements.txt
!pip install pyngrok

🔸 Run Streamlit via Ngrok
from pyngrok import ngrok
import subprocess, time
# Kill previous tunnels
ngrok.kill()
# Start the app
process = subprocess.Popen(["streamlit", "run", "app.py"])
time.sleep(5)
# Create public URL
print("🌍 Public URL:", ngrok.connect(8501))
----

