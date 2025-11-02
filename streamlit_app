import streamlit as st
import google.generativeai as genai
import speech_recognition as sr
from gtts import gTTS
import tempfile
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="Amica AI", page_icon="🧠", layout="centered")

# --- CUSTOM CSS ---
st.markdown("""
<style>
/* Background color is white */
[data-testid="stAppViewContainer"] {
    background-color: #ffffff; /* Solid White */
    background-image: none;
}
.stChatMessage {
    border-radius: 20px;
    padding: 1rem 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    border: 1px solid rgba(0,0,0,0.1); 
}
[data-testid="stChatMessageContent"] {
    background-color: light pink;
    color: indigo;
}
[data-testid="stChatMessageContent"]:has(.avatar-bot) {
    background-color: #2563eb;
    color: #ffffff;
}
.stChatMessage > div:first-child {
    display: flex;
    flex-direction: column;
    align-items: center;
}
[data-testid="stChatMessageContent"] .avatar-bot {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background-color: #991b1b;
    display: flex;
    justify-content: center;
    align-items: center;
    color: white;
    font-weight: bold;
    font-size: 24px;
    margin-bottom: 0.5rem;
}
/* Title content colour changed to a visible blue */
h1 { color: #3b82f6; text-align: center; } 

/* Disclaimer background changed to visible light yellow/orange */
[data-testid="stWarning"] {
    background-color: #fff3cd; 
    border-radius: 15px;
    border-color: #ffc107; 
    color: #664d03; 
}

/* --- STYLES FOR USER INPUT BOX (to match the image) --- */

/* Targets the inner form container holding the input and button */
/* Removed fixed positioning to simplify layout */
[data-testid="stChatInput"] {
    max-width: 600px; /* Set a max width similar to the image */
    width: 90%; /* Responsive width */
    margin: 10px auto; /* Center the entire component */
    padding: 10px 0;
    background-color: #ffffff; 
    
    /* Apply styles directly to the input field itself */
    border-radius: 50px !important; 
    border: 1px solid #ced4da; /* Light grey border */
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); /* Soft, noticeable shadow */
}

/* Targets the actual input element wrapper to apply border radius */
[data-testid="textInput"] > div:first-child > div:first-child {
    border-radius: 50px !important;
}

/* Targets the inner input element to apply styling */
[data-testid="stChatInput"] input {
    padding: 15px 20px !important; /* More vertical padding */
    border-radius: 50px !important;
    border: none !important; /* Remove internal border */
    background-color: #f8f9fa !important; /* Very light gray background for input area */
}

/* Targets the entire input area wrapper to prevent it from spanning the full width */
.stChatInputContainer {
    display: flex;
    justify-content: center; /* Center the chat input */
    padding: 0;
}
</style>
""", unsafe_allow_html=True)

# --- API CONFIG ---
API_KEY = "AIzaSyDbdGmOXYtyddLjWhi_eOMr7JVjRg-J9ds"

try:
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error(f"API configuration error: {e}")
    st.stop()

# --- SYSTEM PROMPT ---
SYSTEM_PROMPT = """
You are Amica, a highly empathetic and caring AI assistant focused on mental well-being.
You are a supportive and non-judgmental listener.
Always acknowledge the user's feelings and respond warmly.
If a user expresses suicidal thoughts, say:
"I'm very sorry to hear you're feeling this way, but please seek immediate help by contacting this helpline: 9152987821. You are not alone."
Never diagnose or prescribe. Always stay comforting and safe.
"""

# --- HEADER ---
st.markdown('<div style="text-align: center;"><h1>Amica - Your Mental Health Assistant 💬</h1></div>', unsafe_allow_html=True)
st.warning("**Disclaimer:** I am not a substitute for professional therapy. If you are in crisis, please contact a local helpline immediately.")
st.markdown("---")

# --- MODEL INIT ---
model = genai.GenerativeModel("gemini-2.5-pro", system_instruction=SYSTEM_PROMPT)
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# --- DISPLAY HISTORY ---
def show_chat_history():
    for msg in st.session_state.chat.history:
        is_user = msg.role == "user"
        with st.chat_message("You" if is_user else "Amica"):
            if not is_user:
                # Removed avatar circle 'A'
                pass
            st.markdown(msg.parts[0].text)
show_chat_history()

# --- SPEECH TO TEXT ---
def listen_to_mic():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening... Speak now.")
        audio = recognizer.listen(source, phrase_time_limit=6)
        try:
            text = recognizer.recognize_google(audio)
            st.success(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            st.warning("Sorry, I didn’t catch that. Please try again.")
        except sr.RequestError:
            st.error("Speech recognition service unavailable.")
    return ""

# --- TEXT TO SPEECH ---
def speak_text(text):
    tts = gTTS(text)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tts.save(tmp.name)
        st.audio(tmp.name, format="audio/mp3")
        os.remove(tmp.name)

# --- CHAT LOGIC ---
col1, col2 = st.columns([1, 1])
with col1:
    # Changed to use st.chat_input without the columns wrapper for easier styling/centering
    user_prompt = st.chat_input("Type how you feel") 

if user_prompt:
    with st.chat_message("You"):
        st.markdown(user_prompt)

    suicide_keywords = ["kill myself", "want to die", "commit suicide", "end my life", "suicidal"]
    if any(k in user_prompt.lower() for k in suicide_keywords):
        safety_response = "I'm very sorry to hear you're feeling this way... Please seek help immediately by contacting this helpline: 9152987821."
        with st.chat_message("Amica"):
            # Removed avatar circle 'A'
            pass
            st.markdown(safety_response)
            speak_text(safety_response)
        st.session_state.chat.history.append({'role': 'user', 'parts': [{'text': user_prompt}]})
        st.session_state.chat.history.append({'role': 'model', 'parts': [{'text': safety_response}]})
    else:
        response = st.session_state.chat.send_message(user_prompt)
        with st.chat_message("Amica"):
            # Removed avatar circle 'A'
            pass
            st.markdown(response.text)
            speak_text(response.text)
