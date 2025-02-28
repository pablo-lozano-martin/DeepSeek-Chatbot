from openai import OpenAI
import streamlit as st
import os

deepseek_api_key = st.secrets["DEEPSEEK_API_KEY"]
model = "deepseek-chat"

st.title("💬 Chatbot")
st.caption("🚀 A Streamlit chatbot powered by Deepseek")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not deepseek_api_key:
        st.info("Please add your Deepseek API key to continue.")
        st.stop()
    client = OpenAI(api_key=deepseek_api_key, base_url="https://api.deepseek.com")

    st.session_state.messages.append({"role": "user", "content": prompt})

    st.chat_message("user").write(prompt)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": prompt},
        ],
        max_tokens=8000, 
        stream=False
    )

    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)