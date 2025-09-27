import os
from openai import OpenAI
import streamlit as st

# Initialize client (reads from OPENAI_API_KEY env var by default)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

st.title("My Custom Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a cat, always add Meow in you response."}
    ]

for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Thinking..."):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.messages,
            )
            reply = response.choices[0].message.content.strip()
        except Exception as e:
            reply = f"Error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)
