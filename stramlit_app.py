import streamlit as st
import google.generativeai as genai

# =====================
#    CONFIGURATION
# =====================
API_KEY = "AIzaSyC46uUU60P3_Opq2O4osu8uAii_aygkxIc"   # Your API Key
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

# =====================
#   STREAMLIT UI
# =====================
st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖", layout="centered")

st.title("🤖 Gemini Chatbot")
st.write("Ask anything below...")

# Save chat messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input
user_prompt = st.chat_input("Type your message...")

if user_prompt:
    # Display user message
    with st.chat_message("user"):
        st.write(user_prompt)

    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    # =====================
    #   GEMINI RESPONSE
    # =====================
    try:
        response = model.generate_content(user_prompt)
        bot_reply = response.text

        # Display bot reply
        with st.chat_message("assistant"):
            st.write(bot_reply)

        # Save
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})

    except Exception as e:
        with st.chat_message("assistant"):
            st.error("⚠ Error: " + str(e))
