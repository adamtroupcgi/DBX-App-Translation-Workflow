"""Launch-week plan state for the Orbit app."""

import streamlit as st

from orbit_app.content import PLAN_TEXT, WEEK
from orbit_app.state import save_follow_up


def render_plan() -> None:
    conversation, workspace = st.columns([3, 1])

    with conversation:
        st.caption("Plan my launch week                                      Share chat")
        st.caption("Today, 9:41 AM")
        with st.container(border=True):
            st.caption("Weekly priorities.pdf · 24 KB")
        with st.chat_message("user"):
            st.text(st.session_state["current_prompt"])

        with st.container(border=True):
            st.markdown("✓  **Plan ready**")
            st.caption("Reviewed your file · Organized priorities · Built your week")

        st.title("A focused week, with room to breathe.")
        st.write(
            "Let’s make Thursday the milestone, not the whole week. "
            "I’ve kept your mornings open for deep work and left space for the unexpected."
        )

        steps = [
            (
                "01",
                "Prepare, then protect your focus",
                "Monday–Tuesday · Finalize the launch essentials and batch small tasks.",
            ),
            (
                "02",
                "Create a buffer before launch",
                "Wednesday · Review the checklist, test key flows, and resolve blockers.",
            ),
            (
                "03",
                "Launch, learn, and leave room to reset",
                "Thursday–Friday · Ship with confidence, then capture what you learned.",
            ),
        ]
        for number, title, detail in steps:
            st.markdown(f"**{number}  {title}**")
            st.caption(detail)

        with st.container(border=True):
            st.markdown("**Your launch week**")
            st.caption("A five-day plan, built around your priorities.")

        for message in st.session_state["follow_ups"]:
            st.markdown("**You**")
            st.text(message)
        if st.session_state["follow_ups"]:
            st.caption("Follow-ups are shown locally; no AI service is connected.")

        with st.form("follow_up_form"):
            st.text_input(
                "Follow-up",
                placeholder="Ask a follow-up or adjust the plan…",
                key="follow_up_input",
                label_visibility="collapsed",
            )
            st.form_submit_button(
                "Add follow-up",
                on_click=save_follow_up,
            )
        if st.session_state["follow_up_error"]:
            st.warning(st.session_state["follow_up_error"])

    with workspace:
        st.caption("YOUR WORKSPACE")
        st.subheader("Your launch week")
        st.caption("One clear plan. A little more breathing room.")
        st.caption("Ready · 5 workdays")
        st.caption("THE WEEK AT A GLANCE")
        for day, date, title, detail in WEEK:
            with st.container(border=True):
                st.caption(f"{day}     {date}")
                st.markdown(f"**{title}**")
                st.caption(detail)
        st.caption("BASED ON YOUR CONTEXT")
        st.caption("Weekly priorities.pdf")
        st.download_button(
            "Download plan",
            data=PLAN_TEXT,
            file_name="your-launch-week-plan.txt",
            mime="text/plain",
            use_container_width=True,
        )
        st.caption("Saved to this conversation.")
