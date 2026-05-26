import streamlit as st
import time
from google import genai

client = genai.Client(api_key="AIzaSyAJAZJ_PH8gErbwZIyJ6GFIFllZxxu_VfI")
MODEL = "models/gemini-2.5-flash"

st.set_page_config(page_title="Frontier AI Assistant", page_icon="🤖")

st.title("🤖 Frontier AI Assistant (Gemini)")

# System prompt (VERY IMPORTANT for evaluation project)
SYSTEM_PROMPT = """
You are a helpful AI assistant.
You answer clearly, safely, and concisely for students.
Avoid harmful, biased, or unsafe content.
"""

# memory
if "chat" not in st.session_state:
    st.session_state.chat = []

def build_context():
    context = SYSTEM_PROMPT + "\n\n"
    for role, msg in st.session_state.chat:
        context += f"{role}: {msg}\n"
    return context

def get_response(prompt):
    for i in range(3):
        try:
            full_prompt = build_context() + f"\nUser: {prompt}\nAssistant:"
            
            response = client.models.generate_content(
                model=MODEL,
                contents=full_prompt
            )
            return response.text

        except Exception:
            time.sleep(2)

    return "⚠️ Server busy. Try again later."

# input
user_input = st.chat_input("Ask something...")

if user_input:

    st.session_state.chat.append(("User", user_input))

    reply = get_response(user_input)

    st.session_state.chat.append(("Assistant", reply))

# display chat
for role, msg in st.session_state.chat:
    with st.chat_message(role):
        st.write(msg)