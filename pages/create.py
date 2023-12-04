"""
TODO
"""
import streamlit as st

st.set_page_config(page_title="Create", page_icon="🏗️")

if "assitants" not in st.session_state:
    st.session_state.assitants = []

if "display_errors" not in st.session_state:
    st.session_state.display_errors = False

display_errors = st.session_state.display_errors

with st.form("configure", clear_on_submit=True):
    # Title
    st.header("Configure")
    # Image
    st.image(
        "https://uxwing.com/wp-content/themes/uxwing/download/"
        + "peoples-avatars/avatar-icon.png",
        width=80,
    )

    # Name
    name = st.text_input(label="Name*", placeholder="Name your assistant")
    if name is None or name == "" and display_errors:
        st.write(":red[Name is required]")

    # Description
    description = st.text_input(
        label="Description*",
        placeholder="Add a short description about what this Assistant does",
    )
    if description is None or description == "" and display_errors:
        st.write(":red[Description is required]")

    # Instruction
    instructions = st.text_area(
        label="Instructions*",
        placeholder="What does this Assistant do? How does it behave? What should it avoid doing?",
    )
    if instructions is None or instructions == "" and display_errors:
        st.write(":red[Instructions is required]")

    model = st.selectbox(
        "Select a model",
        (
            "Mistral-7B",
            "zephyr-7b-beta",
        ),
        index=0,
    )

    # Capabilities
    with st.container():
        st.write(
            "Capabilities",
        )
        sdxlt = st.checkbox("Stabble diffusion XL Turbo")

    submitted = st.form_submit_button("Save")

    if submitted and name and description and instructions:
        assistant = dict(
            name=name,
            description=description,
            instructions=instructions,
            model=model,
            sdxlt=sdxlt,
        )
        st.session_state.assitants.append(assistant)
        st.toast(f"{name} assistant has been created!", icon="🎉")
        st.session_state.display_errors = False
    else:
        st.session_state.display_errors = True
