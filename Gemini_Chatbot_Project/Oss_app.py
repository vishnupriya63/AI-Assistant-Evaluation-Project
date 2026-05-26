import streamlit as st
from transformers import pipeline

# Page config
st.set_page_config(
    page_title="OSS AI Assistant",
    page_icon="🟢"
)

st.title("🟢 Open Source AI Assistant")

# Load model
chatbot = pipeline(
    "text-generation",
    model="Qwen/Qwen2.5-0.5B-Instruct"
)

# Strong system prompt
SYSTEM_PROMPT = """
You are a helpful AI assistant.

Rules:
- Always reply in English only.
- Give short and clear answers.
- Do not repeat old conversations.
- Do not generate hashtags.
- Do not generate random text.
- Avoid harmful or unsafe content.
"""

# Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show old messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input
user_input = st.chat_input("Ask something...")

if user_input:

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Build prompt
    prompt = SYSTEM_PROMPT + "\n\n"

    for msg in st.session_state.messages[-4:]:
        prompt += f"{msg['role']}: {msg['content']}\n"

    prompt += "assistant:"

    # Generate response
    result = chatbot(
        prompt,
        max_new_tokens=80,
        temperature=0.5,
        do_sample=True,
        truncation=True
    )

    output = result[0]["generated_text"]

    # Clean response
    reply = output.split("assistant:")[-1].strip()

    # Save assistant reply
    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })

    # Display reply
    with st.chat_message("assistant"):
        st.write(reply)