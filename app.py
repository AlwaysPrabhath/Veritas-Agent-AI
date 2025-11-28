import streamlit as st
import time
from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def deepcheck_chat_reply(messages, score: float | None = None) -> str:
    """Uses free Groq Llama model for real responses."""
    
    system_prompt = (
        "You are Veritas Agent, a cold and analytical forensic intelligence system. "
        "Your tone is factual, concise, and objective. "
        "You analyze deepfake credibility and explain forensic indicators clearly."
    )

    if score is not None:
        system_prompt += f" The current detected deepfake probability score is {score}%."

    formatted_messages = [{"role": "system", "content": system_prompt}] + messages

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=formatted_messages,
        temperature=0.25,
    )

    return response.choices[0].message.content


st.set_page_config(
    page_title="Veritas Agent — Deepfake Intelligence Console",
    layout="wide"
)

# Google fonts
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500&family=Orbitron:wght@600;800&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# =========================
# CYBERPUNK THEME CSS
# =========================
hud_css = """
<style>

:root {
  --bg1: #050516;
  --bg2: #120624;
  --bg3: #31125d;
  --bg4: #5c1ba1;
  --accent: #00f7ff;
  --accent-soft: #7ef7ff;
  --accent-purple: #c03bff;
}

/* 🔮 Background Gradient + Slow Motion */
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > .main {
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

/* Sidebar – dark glass with cyan accent */
[data-testid="stSidebar"] {
    background: rgba(5, 5, 22, 0.92) !important;
    backdrop-filter: blur(14px);
    border-right: 1px solid rgba(0, 247, 255, 0.35);
    color: #e9efff !important;
}
[data-testid="stSidebar"] > div {
    padding-top: 1.5rem;
}

/* Header area transparent */
[data-testid="stHeader"] {
    background: rgba(0,0,0,0) !important;
}

/* Main container like HUD panel */
.block-container {
    background: linear-gradient(135deg, rgba(9, 9, 30, 0.94), rgba(19, 7, 45, 0.96));
    border-radius: 22px;
    padding: 30px;
    border: 1px solid rgba(0, 247, 255, 0.28);
    box-shadow:
        0 0 40px rgba(0, 0, 0, 0.8),
        0 0 60px rgba(0, 247, 255, 0.12);
}

/* Neon outline for columns separation */
.css-ocqkz7, .css-1y4p8pa {
    border-color: rgba(0, 247, 255, 0.2) !important;
}

/* ⚡ Neon HUD buttons */
.stButton>button {
    background: linear-gradient(90deg, #c03bff, #00f7ff) !important;
    border: 1px solid rgba(0, 247, 255, 0.6) !important;
    color: #050516 !important;
    border-radius: 999px !important;
    padding: 0.6rem 1.9rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    box-shadow:
        0 0 0px rgba(0,0,0,0),
        0 0 20px rgba(0, 247, 255, 0.9),
        0 0 40px rgba(192, 59, 255, 0.8);
    transition: all 0.22s ease;
}
.stButton>button:hover {
    transform: translateY(-1px) scale(1.03);
    box-shadow:
        0 0 0px rgba(0,0,0,0),
        0 0 28px rgba(0, 247, 255, 1),
        0 0 60px rgba(192, 59, 255, 1);
}

/* File uploader glass HUD style */
[data-testid="stFileUploader"] > div {
    background: transparent;
    border: none;
}
[data-testid="stFileUploaderDropzone"] {
    background: radial-gradient(circle at 0 0, rgba(192,59,255,0.28), rgba(5,5,22,0.95));
    backdrop-filter: blur(12px);
    border-radius: 18px !important;
    border: 1px solid rgba(0, 247, 255, 0.5) !important;
    box-shadow:
        0 0 25px rgba(0,0,0,0.9),
        0 0 34px rgba(0, 247, 255, 0.4);
    transition: 0.25s ease;
}
[data-testid="stFileUploaderDropzone"]:hover {
    border-color: #00f7ff !important;
    box-shadow:
        0 0 12px rgba(0, 247, 255, 0.9),
        0 0 30px rgba(192, 59, 255, 0.7);
}

/* Text input HUD style */
[data-testid="stTextInput"] input {
    background: transparent !important;
    border: none !important;
    color: #e9efff !important;
    font-family: "Montserrat", sans-serif;
}
[data-testid="stTextInput"] > div {
    background: linear-gradient(90deg, rgba(5,5,22,0.95), rgba(23, 7, 55, 0.95)) !important;
    backdrop-filter: blur(10px);
    border-radius: 16px !important;
    border: 1px solid rgba(0, 247, 255, 0.45) !important;
    padding: 6px !important;
    box-shadow: 0 0 18px rgba(0,0,0,0.7);
}
[data-testid="stTextInput"] > div:hover {
    border: 1px solid rgba(0, 247, 255, 0.8) !important;
}

/* Floating minimal stars (keep it subtle) */
.star {
    position: fixed;
    font-size: 16px;
    opacity: 0.45;
    pointer-events: none;
    animation: twinkle 5s infinite ease-in-out;
    color: #7ef7ff;
}
@keyframes twinkle {
    0% { opacity: 0.15; transform: scale(1); }
    50% { opacity: 0.9; transform: scale(1.35); }
    100% { opacity: 0.15; transform: scale(1); }
}

/* HUD-style shooting scan line is optional – keeping only shooting star */
.shooting-star {
    position: fixed;
    top: 10%;
    left: -10%;
    width: 4px;
    height: 4px;
    background: #00f7ff;
    border-radius: 50%;
    animation: shooting 7s infinite;
    filter: blur(1px);
}
@keyframes shooting {
    0% { transform: translateX(0) translateY(0); opacity: 0; }
    10% { opacity: 1; }
    50% { transform: translateX(120vw) translateY(10vh); opacity: .9; }
    100% { opacity: 0; }
}

/* Status pills under logo */
.status-pill {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 999px;
    font-size: 11px;
    font-family: 'Montserrat', sans-serif;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin: 0 4px;
}
.status-ok {
    background: rgba(0, 247, 132, 0.12);
    border: 1px solid rgba(0, 247, 132, 0.85);
    color: #a7ffda;
}
.status-mode {
    background: rgba(0, 247, 255, 0.1);
    border: 1px solid rgba(0, 247, 255, 0.7);
    color: #c1fbff;
}

/* AI engine running micro animation */
.ai-running {
    font-family: 'Montserrat', sans-serif;
    font-size: 12px;
    color: #cdefff;
    margin-top: 8px;
    opacity: 0.9;
}
.ai-dots span {
    animation: dotPulse 1.2s infinite ease-in-out;
    display: inline-block;
}
.ai-dots span:nth-child(2) { animation-delay: 0.2s; }
.ai-dots span:nth-child(3) { animation-delay: 0.4s; }
@keyframes dotPulse {
    0% { opacity: 0.2; transform: translateY(0px); }
    50% { opacity: 1; transform: translateY(-2px); }
    100% { opacity: 0.2; transform: translateY(0px); }
}

/* Circular scanner – now cyan/purple HUD ring */
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
    box-shadow:
        0 0 25px rgba(0, 247, 255, 0.5),
        0 0 50px rgba(192, 59, 255, 0.4);
}
.scanner-core {
    width: 64px;
    height: 64px;
    border-radius: 50%;
    border: 2px solid rgba(0, 247, 255, 0.9);
    box-shadow: 0 0 22px rgba(0, 247, 255, 0.9);
    position: relative;
    overflow: hidden;
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
.scanner-label {
    margin-top: 8px;
    font-size: 11px;
    font-family: 'Montserrat', sans-serif;
    color: #9df4ff;
    text-transform: uppercase;
    letter-spacing: 1px;
}

</style>

<!-- Subtle HUD stars -->
<div class="star" style="top: 9%; left: 22%;">✦</div>
<div class="star" style="top: 26%; left: 78%;">✧</div>
<div class="star" style="top: 60%; left: 14%;">✶</div>
<div class="star" style="top: 82%; left: 67%;">✦</div>

<div class="shooting-star"></div>
"""
st.markdown(hud_css, unsafe_allow_html=True)

# =========================
# Header + logo / status strip
# =========================
header_html = """
<div style='text-align:center; margin-top: -10px; margin-bottom: 5px;'>
    <h1 style="
        font-family: 'Orbitron', sans-serif;
        font-size: 46px;
        font-weight: 700;
        color: #e9efff;
        letter-spacing: 4px;
        text-shadow: 0px 0px 18px rgba(0,247,255,0.9);
    ">
        VERITAS AGENT
    </h1>
    <p style="
        font-family: 'Montserrat', sans-serif;
        font-size: 14px;
        color: #b6c8ff;
        margin-top: -6px;
        letter-spacing: 0.6px;
    ">
        Neural forensics console for video authenticity & deepfake credibility assessment
    </p>
    <div style="margin-top: 6px;">
        <span class="status-pill status-ok">SYSTEM ONLINE</span>
        <span class="status-pill status-mode">DEEPFAKE ANALYSIS MODE</span>
    </div>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

st.markdown("""
<hr style="border: none; height: 1px; background: linear-gradient(90deg, transparent, rgba(0,247,255,0.9), transparent); margin-top:6px; margin-bottom:22px;">
""", unsafe_allow_html=True)

# =========================
# Sidebar
# =========================
st.sidebar.markdown("""
<div style="font-family:Montserrat; font-size:14px; line-height:1.7; color:#e9efff;">
<span style="font-size:16px; font-weight:600; color:#7ef7ff;"> Veritas Agent HUD</span><br><br>
1️⃣ <b>Upload</b> a short video (mp4 / mov / avi).<br>
2️⃣ <b>(Optional)</b> enter a question about the clip.<br>
3️⃣ Hit <b>Run Deepfake Analysis</b> to start the engine.<br>
4️⃣ Review the <b>credibility score</b> and summary on the right.<br>
</div>
""", unsafe_allow_html=True)

# =========================
# Main layout
# =========================
col1, col2 = st.columns([2, 3])

# Left: upload & preview
with col1:
    st.markdown("<h3 style='font-family:Montserrat; color:#e9efff; text-transform:uppercase; letter-spacing:1px;'>Upload Module</h3>", unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload a video", type=["mp4", "mov", "avi", "mkv"])

    if uploaded is not None:
        st.success("Video received! (Backend connection will happen later)")
        st.write("Video preview:")
        st.video(uploaded)


# Right: analysis & results
with col2:
    st.markdown("<h3 style='font-family:Montserrat; color:#e9efff; text-transform:uppercase; letter-spacing:1px;'>Analysis Engine</h3>", unsafe_allow_html=True)

    question = st.text_input("Ask something about this video (optional):")

    analyze_btn = st.button("Run Deepfake Analysis")

    if analyze_btn:
        if uploaded is None:
            st.warning("Please upload a video before analyzing.")
        else:
        # --- scanner HTML ---
            scanner_html = """
            <div class="scanner-wrapper">
                <div class="scanner-ring">
                    <div class="scanner-core">
                        <div class="scanner-sweep"></div>
                    </div>
                </div>
                <div class="scanner-label">SCANNING VIDEO FRAMES</div>
                <div class="ai-running">
                    AI engine running
                    <span class="ai-dots">
                        <span>.</span><span>.</span><span>.</span>
                    </span>
                </div>
            </div>
            """

            # 🔹 create a temporary placeholder for the scanner
            scanner_placeholder = st.empty()

            with st.spinner("Analyzing video..."):
                # render scanner only inside this placeholder
                with scanner_placeholder.container():
                    st.markdown(scanner_html, unsafe_allow_html=True)

                # TODO: replace this with real model call
                time.sleep(4)

            # 🔹 remove the scanner once analysis is done
            scanner_placeholder.empty()

            # now show final results
            fake_score = 12.5  # placeholder score
            st.success("Analysis complete!")

            result_box = st.container()
            with result_box:
                st.markdown("#### 📊 Credibility Report")
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("Deepfake score (0–100%)", f"{fake_score:.1f}%")
                with col_b:
                    st.write("**Status:** Low likelihood of manipulation.")

                st.write(
                    "This is placeholder output. Once the detection model is wired in, "
                    "this block will show real reasoning and evidence traces."
                )

                if question:
                    st.markdown("---")
                    st.markdown("**Operator query:**")
                    st.write(question)
                    st.caption("Later, the agent's answer to this query will appear here.")

# =========================
# Chatbot – Veritas Agent Assistant
# =========================
st.markdown("## 💬 Veritas Agent Assistant")

# Init chat history once
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Pretty chat bubbles in main view ---
for msg in st.session_state.chat_history:
    role = msg["role"]
    content = msg["content"]

    if role == "user":
        bubble_color = "rgba(0,0,0,0.35)"
        align = "flex-start"
        label = "Operator"
    else:
        bubble_color = "rgba(255,255,255,0.10)"
        align = "flex-end"
        label = "Veritas Agent"

    st.markdown(
        f"""
        <div style="display:flex; justify-content:{align}; margin-bottom:6px;">
          <div style="
              background:{bubble_color};
              padding:8px 12px;
              border-radius:12px;
              max-width:70%;
              font-size:14px;
              border:1px solid rgba(255,255,255,0.15);
          ">
            <div style="font-size:11px; opacity:0.7; margin-bottom:2px;"><b>{label}</b></div>
            <div>{content}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# --- Input row (ask question here) ---
user_msg = st.text_input(
    "Ask Veritas Agent something about deepfakes, this video, or the analysis:",
    key="chat_input",
)

col_chat_send, col_chat_clear = st.columns([1, 1])
send_clicked = col_chat_send.button("Send")
clear_clicked = col_chat_clear.button("Clear Chat")

# Clear history if needed
if clear_clicked:
    st.session_state.chat_history = []
    st.rerun()

# ---- Chat Submit Handler ----
if send_clicked and user_msg.strip():

    # Store user message
    st.session_state.chat_history.append({"role": "user", "content": user_msg})

    # Prepare messages for Groq / LLM
    messages_for_api = []
    for m in st.session_state.chat_history:
        messages_for_api.append({
            "role": m["role"],   # "user" or "assistant"
            "content": m["content"]
        })

    # Use deepfake score if exists
    current_score = fake_score if "fake_score" in locals() else None

    try:
        reply_text = deepcheck_chat_reply(messages_for_api, score=current_score)
    except Exception as e:
        reply_text = f"⚠️ Model Error: {e}"

    # Store the assistant reply
    st.session_state.chat_history.append({"role": "assistant", "content": reply_text})

    # Refresh UI
    st.rerun()

st.markdown("---")

# --- Forensic-style chat history panel (now BELOW input) ---
history_expander = st.expander("Session chat history (forensic log)", expanded=True)
with history_expander:
    if not st.session_state.chat_history:
        st.caption("No messages yet. Conversation log will appear here.")
    else:
        for i, msg in enumerate(st.session_state.chat_history, start=1):
            role_label = "Operator" if msg["role"] == "user" else "Veritas Agent"
            st.markdown(f"**{i}. {role_label}:** {msg['content']}")


# =========================
# Footer / disclaimer
# =========================
st.markdown("---")
st.caption(
    "⚠ Prototype console. Deepfake scores and explanations are placeholders "
    "until the final detection model is integrated."
)
st.caption("Built by Team Veritas")