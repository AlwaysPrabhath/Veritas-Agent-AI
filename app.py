import streamlit as st
import time
import os
import joblib

# --- IMPORT YOUR NEW PIPELINE ---
# This connects the frontend to your new Agent files
try:
    from agent_pipeline import run_agent_pipeline
except ImportError:
    st.error("⚠️ Error: Could not import 'agent_pipeline'. Make sure agent_pipeline.py is in the same folder.")
    st.stop()

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Veritas Agent — Deepfake Intelligence Console",
    layout="wide"
)

# --- LOAD INTENT MODEL (THE BRAIN) ---
@st.cache_resource
def load_intent_model():
    try:
        model = joblib.load("intent_classifier.pkl")
        return model
    except FileNotFoundError:
        return None

intent_model = load_intent_model()

# --- HELPER: GET USER INTENT ---
def get_user_intent(text):
    """
    Predicts intent using the local Logistic Regression model.
    """
    if not intent_model:
        return "error", 0.0
    
    try:
        probas = intent_model.predict_proba([text])[0]
        max_index = probas.argmax()
        confidence = probas[max_index]
        predicted_intent = intent_model.classes_[max_index]
        
        # Fallback threshold (adjust as needed)
        if confidence < 0.4: 
            return "fallback", confidence
            
        return predicted_intent, confidence
    except Exception as e:
        print(f"Prediction Error: {e}")
        return "error", 0.0

# =========================
# CYBERPUNK THEME CSS
# =========================
hud_css = """
<style>
:root {
  --bg1: #050516;
  --bg2: #120624;
  --accent: #00f7ff;
  --accent-purple: #c03bff;
}
[data-testid="stAppViewContainer"], [data-testid="stAppViewContainer"] > .main {
    background: radial-gradient(circle at 10% 0%, #34175f 0, #050516 50%, #050516 100%);
    background-size: 240% 240%;
    animation: bgMove 28s ease-in-out infinite;
    color: #f5f5ff !important;
}
@keyframes bgMove {
    0% { background-position: 0% 0%; }
    50% { background-position: 80% 80%; }
    100% { background-position: 0% 0%; }
}
[data-testid="stSidebar"] {
    background: rgba(5, 5, 22, 0.92) !important;
    border-right: 1px solid rgba(0, 247, 255, 0.35);
}
.stButton>button {
    background: linear-gradient(90deg, #c03bff, #00f7ff) !important;
    border: 1px solid rgba(0, 247, 255, 0.6) !important;
    color: #050516 !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    transition: all 0.22s ease;
}
.stButton>button:hover {
    transform: translateY(-1px) scale(1.03);
    box-shadow: 0 0 28px rgba(0, 247, 255, 1);
}

/* --- FIX FOR INVISIBLE TEXT INPUTS --- */
[data-testid="stTextInput"] input {
    background: transparent !important;
    border: none !important;
    color: #e9efff !important;
    -webkit-text-fill-color: #e9efff !important; /* Force text color on Chrome/Safari */
    caret-color: #00f7ff !important; /* Neon cyan cursor */
    font-family: "Montserrat", sans-serif;
}
[data-testid="stTextInput"] > div {
    background: linear-gradient(90deg, rgba(5,5,22,0.95), rgba(23, 7, 55, 0.95)) !important;
    border: 1px solid rgba(0, 247, 255, 0.45) !important;
}

.scanner-wrapper {
    margin-top: 10px;
    display: flex;
    flex-direction: column;
    align-items: center;
}
.scanner-ring {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    border: 1px solid rgba(0, 247, 255, 0.7);
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    box-shadow: 0 0 25px rgba(0, 247, 255, 0.5);
}
.scanner-sweep {
    position: absolute;
    width: 100%;
    height: 100%;
    background: conic-gradient(from 0deg, rgba(0,247,255,0.95), transparent 40%);
    animation: sweepRotate 1.6s linear infinite;
}
@keyframes sweepRotate {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}
</style>
"""
st.markdown(hud_css, unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.markdown("""
<div style='text-align:center;'>
    <h1 style="font-family: 'Orbitron', sans-serif; color: #e9efff; text-shadow: 0px 0px 18px rgba(0,247,255,0.9);">
        VERITAS AGENT
    </h1>
    <p style="color: #b6c8ff;">Neural forensics console for video authenticity analysis</p>
    <div>
        <span style="background:rgba(0, 247, 132, 0.12); color:#a7ffda; padding:3px 12px; border-radius:999px; font-size:11px; border:1px solid rgba(0, 247, 132, 0.85);">SYSTEM ONLINE</span>
    </div>
</div>
<hr style="border: none; height: 1px; background: linear-gradient(90deg, transparent, rgba(0,247,255,0.9), transparent); margin-top:15px; margin-bottom:25px;">
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================
st.sidebar.markdown("""
<div style="color:#e9efff;">
<span style="font-size:16px; font-weight:600; color:#7ef7ff;"> Veritas Agent HUD</span><br><br>
1️⃣ <b>Upload</b> a video.<br>
2️⃣ Hit <b>Run Analysis</b>.<br>
3️⃣ Review the <b>Forensic Report</b>.<br>
</div>
""", unsafe_allow_html=True)

# =========================
# MAIN LAYOUT
# =========================
col1, col2 = st.columns([2, 3])

# --- LEFT COLUMN: UPLOAD ---
with col1:
    st.markdown("### UPLOAD MODULE")
    uploaded = st.file_uploader("Upload a video", type=["mp4", "mov", "avi"])

    if uploaded is not None:
        st.success("Video received.")
        st.video(uploaded)

# --- RIGHT COLUMN: ANALYSIS ENGINE ---
with col2:
    st.markdown("### ANALYSIS ENGINE")
    question = st.text_input("Add specific query (optional):", placeholder="e.g., Is the lip movement natural?")
    analyze_btn = st.button("RUN DEEPFAKE ANALYSIS")

    if analyze_btn:
        if uploaded is None:
            st.warning("⚠️ Access Denied: No video evidence found. Please upload a file.")
        else:
            # 1. Scanner Animation
            scanner_html = """
            <div class="scanner-wrapper">
                <div class="scanner-ring"><div class="scanner-core"><div class="scanner-sweep"></div></div></div>
                <div style="color:#9df4ff; font-size:12px; margin-top:10px; letter-spacing:1px;">ANALYZING FRAMES...</div>
            </div>
            """
            placeholder = st.empty()
            with placeholder.container():
                st.markdown(scanner_html, unsafe_allow_html=True)
                time.sleep(3) # Simulate processing time
            placeholder.empty()

            # 2. DEFINE EVIDENCE (SIMULATED FOR NOW)
            # In Phase 3, your Deepfake Model (MesoNet) will populate this!
            fake_score = 88.5 
            evidence_package = {
                "score": fake_score, 
                "anomalies": ["Lip Sync Failure", "Unnatural Blinking Patterns", "Mouth Artifacts"],
                "metadata": f"Filename: {uploaded.name} | Size: {uploaded.size/1024:.1f}KB"
            }

            st.success("Analysis Complete.")

            # 3. DISPLAY METRICS
            result_box = st.container()
            with result_box:
                st.markdown("#### 📊 Credibility Report")
                c1, c2 = st.columns(2)
                with c1:
                    st.metric("Deepfake Probability", f"{fake_score}%")
                with c2:
                    status = "CRITICAL" if fake_score > 70 else "SAFE"
                    st.write(f"**Status:** {status}")

                # 4. GENERATE REPORT VIA PIPELINE
                user_command = question if question else "Generate Forensic Report"
                
                with st.spinner("Consulting Veritas Intelligence..."):
                    # Call the agent pipeline with the 'report' intent and evidence
                    report = run_agent_pipeline(
                        intent="report", 
                        user_text=user_command, 
                        chat_history=[], 
                        evidence=evidence_package
                    )
                
                st.info(report)
                
                # Add to chat history automatically
                if "chat_history" not in st.session_state:
                    st.session_state.chat_history = []
                st.session_state.chat_history.append({"role": "assistant", "content": report})

# =========================
# CHATBOT INTERFACE
# =========================
st.markdown("---")
st.markdown("## 💬 Veritas Agent Assistant")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display Chat History
for msg in st.session_state.chat_history:
    role = msg["role"]
    content = msg["content"]
    align = "flex-end" if role == "assistant" else "flex-start"
    color = "rgba(255,255,255,0.10)" if role == "assistant" else "rgba(0,0,0,0.35)"
    label = "Veritas" if role == "assistant" else "Operator"
    
    st.markdown(f"""
    <div style="display:flex; justify-content:{align}; margin-bottom:10px;">
        <div style="background:{color}; padding:10px 15px; border-radius:10px; max-width:70%; border:1px solid rgba(255,255,255,0.1);">
            <div style="font-size:10px; opacity:0.7; margin-bottom:4px;"><b>{label}</b></div>
            {content}
        </div>
    </div>
    """, unsafe_allow_html=True)

# Chat Input
user_msg = st.text_input("Input command / query:", key="chat_input")
col_send, col_clear = st.columns([1, 6])
send_clicked = col_send.button("Send")

if col_clear.button("Clear Log"):
    st.session_state.chat_history = []
    st.rerun()

# ---- CHAT LOGIC (UPDATED WITH PIPELINE) ----
if send_clicked and user_msg.strip():
    
    # 1. Store User Message
    st.session_state.chat_history.append({"role": "user", "content": user_msg})

    # 2. IDENTIFY INTENT (Local Brain)
    intent, confidence = get_user_intent(user_msg)
    
    # 3. EXECUTE PIPELINE
    # Prepare history for context
    history_for_api = [{"role": m["role"], "content": m["content"]} for m in st.session_state.chat_history]
    
    # Run the pipeline (evidence=None because this is just a chat message)
    response_text = run_agent_pipeline(intent, user_msg, history_for_api, evidence=None)

    # 4. FALLBACKS (If pipeline returns None, use static responses)
    if not response_text:
        if intent == "greeting":
            response_text = "Greetings. I am Veritas. Ready to analyze video evidence."
        elif intent == "analyze_video":
            response_text = "Please use the 'Upload Module' on the left sidebar to submit evidence."
        elif intent == "goodbye":
            response_text = "Session ending. Stay vigilant."
        elif intent == "help":
            response_text = "GUIDE: 1. Upload Video. 2. Click Analyze. 3. Read Report."
        else:
            response_text = "I received your query but require more context."

    # 5. Show Response
    st.session_state.chat_history.append({"role": "assistant", "content": response_text})
    st.rerun()
