# DeepCheck — Deepfake Detection UI

DeepCheck is a neural forensics console built with Streamlit for exploring video authenticity and deepfake credibility.

This repo contains the **frontend + UX layer**:
- Video upload & preview interface  
- “Run Deepfake Analysis” workflow (currently using placeholder model output)
- DeepCheck Assistant: a chat-style AI panel for asking questions about deepfakes / the analysis
- Small demo video set for quick testing

> Backend deepfake detection models (CV / intent / LLM backends) are handled in separate modules by teammates.

---

## 🔧 Features

- 🎥 **Video uploader + preview**  
  Upload MP4 / MOV / AVI / MKV videos and preview them directly in the UI.

- 📊 **Analysis panel (placeholder)**  
  Button-driven analysis flow with a credibility score + status text.  
  Currently wired to a fake score for demo; ready to be connected to a real model.

- 🤖 **DeepCheck Assistant (chatbot)**  
  Chat-style interface that:
  - Keeps conversation history in the session
  - Sends messages to an LLM backend (via Groq API)
  - Can be extended to answer questions about the uploaded clip or model output

- 📂 **Demo video directory**  
  `demo_videos/test_real.mp4` and `demo_videos/test_fake.mp4` included for UI testing.

---

## 📁 Project structure

```text
deepcheck/
├─ app.py              # Main Streamlit app (UI + chatbot + analysis flow)
├─ requirements.txt    # Python dependencies
└─ demo_videos/
   ├─ test_real.mp4    # Sample "real" video for demo
   └─ test_fake.mp4    # Sample "fake" video for demo
