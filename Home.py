import streamlit as st
from anthropic import Anthropic
import os

def stream(messages: list[dict[str, str]]):
    client = Anthropic()
    with client.messages.stream(
        max_tokens=1024,
        messages=messages,
        system="You are a helpful AI assistant.",
        model=os.getenv('MODEL'),
    ) as stream:
        for text in stream.text_stream:
            yield text

st.title("💬 Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

st.chat_message("assistant").write("Hello! How can I help you today?")
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = st.write_stream(stream(messages=st.session_state.messages))
    st.session_state.messages.append({"role": "assistant", "content": response})