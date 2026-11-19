"""Landing state for the Orbit app."""

import streamlit as st

from orbit_app.content import STARTERS
from orbit_app.state import choose_starter, start_plan


def render_home() -> None:
    st.caption("YOUR WORKSPACE                                      ALL SYSTEMS READY")
    st.caption("A LITTLE SUPPORT. A LOT OF POSSIBILITY.")
    st.title("What’s on your mind?")
    st.caption("A thinking partner for your plans, questions, and next big idea.")

    st.selectbox(
        "Assistant",
        [
            "General assistant",
            "Writing partner",
            "Research assistant",
            "Project planner",
        ],
        key="assistant",
    )

    with st.container(border=True):
        with st.form("prompt_form"):
            st.text_area(
                "Prompt",
                placeholder="Ask a question, make a plan, or start with an idea…",
                key="landing_prompt",
                label_visibility="collapsed",
                height=100,
            )
            st.form_submit_button(
                "Start planning",
                type="primary",
                use_container_width=True,
                on_click=start_plan,
            )
        if st.session_state["prompt_error"]:
            st.warning(st.session_state["prompt_error"])

    st.subheader("Try a starting point")
    st.caption("Small prompts. Useful possibilities.")
    cards = st.columns(3)
    for index, (title, description, prompt) in enumerate(STARTERS):
        with cards[index]:
            with st.container(border=True):
                st.markdown(f"**{title}**")
                st.caption(description)
                st.button(
                    "Use this prompt",
                    key=f"starter_{index}",
                    use_container_width=True,
                    on_click=choose_starter,
                    args=(prompt,),
                )

    st.divider()
    st.caption("A specialist for every kind of task")
    st.caption("Writing partner · Research assistant · Project planner")
    st.caption("Orbit can make mistakes. Check important information.")
