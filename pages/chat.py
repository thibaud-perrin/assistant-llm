"""
TODO
"""
import streamlit as st
from typing import List

import asyncio

from lib.ollama_call import call_api

st.set_page_config(page_title="Chat", page_icon="💬", layout="wide")

if "assitants" not in st.session_state:
    st.session_state.assitants = []

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = {}

if "running" not in st.session_state:
    st.session_state.running = False

assistants = st.session_state.assitants
assistants_name: List[str] = [ast["name"] for ast in assistants]

chat_messages = st.session_state.chat_messages


async def model_call(
    model: str, prompt: str, name: str, instructions: str, assistant: str
):
    new_message = dict(role="ai", message="")
    st.session_state.chat_messages[assistant].append(new_message)
    st.session_state.running = True

    full_text = ""
    with st.empty():
        async for result in call_api(model, prompt, name, instructions):
            full_text += result["response"]
            st.session_state.chat_messages[assistant][-1]["message"] = full_text
            msg = st.chat_message("ai")
            msg.write(full_text)
    st.session_state.running = False


def add_message(role, message, assistant):
    if assistant not in chat_messages:
        st.session_state.chat_messages[assistant] = []

    new_message = dict(role=role, message=message)
    st.session_state.chat_messages[assistant].append(new_message)

    msg = st.chat_message(new_message["role"])
    msg.write(new_message["message"])


# Function to redraw the chat messages
def redraw_chat(assistant):
    if assistant not in chat_messages:
        st.session_state.chat_messages[assistant] = []
    # Clear the previous chat messages
    for _ in range(len(st.session_state.chat_messages[assistant])):
        st.empty()

    # Display the updated chat messages
    for message in st.session_state.chat_messages[assistant]:
        msg = st.chat_message(message["role"])
        msg.write(message["message"])


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

    redraw_chat(selected)

    # chat input
    prompt = st.chat_input("Say something", disabled=st.session_state.running)
    if prompt:
        add_message("user", prompt, selected)
        asyncio.run(
            model_call(
                assistants[selected_index]["model"],
                prompt,
                assistants[selected_index]["name"],
                assistants[selected_index]["instructions"],
                selected,
            )
        )

else:
    st.info("Go to `create` page in order to build your first agent", icon="ℹ️")
