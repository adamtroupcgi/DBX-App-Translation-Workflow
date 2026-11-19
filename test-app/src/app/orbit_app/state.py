"""Session-state initialization and event handlers."""

import streamlit as st


def initialize_state() -> None:
    defaults = {
        "screen": "home",
        "landing_prompt": "",
        "current_prompt": "Help me plan a calm, focused workweek.",
        "assistant": "General assistant",
        "follow_ups": [],
        "follow_up_input": "",
        "prompt_error": "",
        "follow_up_error": "",
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def start_new_chat() -> None:
    st.session_state["screen"] = "home"
    st.session_state["landing_prompt"] = ""
    st.session_state["follow_ups"] = []
    st.session_state["prompt_error"] = ""
    st.session_state["follow_up_error"] = ""


def choose_starter(prompt: str) -> None:
    st.session_state["landing_prompt"] = prompt
    st.session_state["prompt_error"] = ""


def start_plan() -> None:
    prompt = st.session_state["landing_prompt"].strip()
    if not prompt:
        st.session_state["prompt_error"] = "Enter a prompt or choose a starting point."
        return

    st.session_state["current_prompt"] = prompt
    st.session_state["screen"] = "plan"
    st.session_state["follow_ups"] = []
    st.session_state["prompt_error"] = ""


def open_saved_plan() -> None:
    st.session_state["screen"] = "plan"


def save_follow_up() -> None:
    message = st.session_state["follow_up_input"].strip()
    if not message:
        st.session_state["follow_up_error"] = "Enter a follow-up message."
        return

    st.session_state["follow_ups"].append(message)
    st.session_state["follow_up_input"] = ""
    st.session_state["follow_up_error"] = ""
