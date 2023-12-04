"""
TODO
"""
import streamlit as st
from typing import List
import time


st.set_page_config(page_title="Chat", page_icon="💬", layout="wide")

if "assitants" not in st.session_state:
    st.session_state.assitants = []

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = {}

if "selected_assistant" not in st.session_state:
    st.session_state.selected_assistant = None

assistants = st.session_state.assitants
assistants_name: List[str] = [ast["name"] for ast in assistants]

chat_messages = st.session_state.chat_messages

selected_assistant = st.session_state.selected_assistant


def chat():
    if selected_assistant not in chat_messages:
        st.session_state.chat_messages[selected_assistant] = []

    for message in chat_messages[selected_assistant]:
        msg = st.chat_message(message["role"])
        msg.write(message["message"])

    # chat input
    prompt = st.chat_input("Say something")
    if prompt:
        new_message = dict(role="user", message=prompt)
        st.session_state.chat_messages[selected_assistant].append(new_message)
        msg = st.chat_message(new_message["role"])
        msg.write(new_message["message"])


st.header("Chat")
if len(assistants_name) > 0:
    selected = st.selectbox(
        "Select your assistant",
        assistants_name,
        index=0,
    )
    selected_index = assistants_name.index(selected)
    st.divider()

    if selected:
        # Presentation
        st.subheader(assistants[selected_index]["name"])
        st.write(f"Description: {assistants[selected_index]['description']}")
        st.write(f"Model: {assistants[selected_index]['model']}")
        st.divider()

        st.session_state.selected_assistant = selected

    chat()

else:
    st.info("Go to `create` page in order to build your first agent", icon="ℹ️")
