"""Sidebar navigation and static workspace details."""

import streamlit as st

from orbit_app.state import open_saved_plan, start_new_chat


def render_sidebar() -> None:
    with st.sidebar:
        st.markdown(
            "<div style='color:#244C3D;font-size:32px;font-weight:600'>orbit</div>",
            unsafe_allow_html=True,
        )
        st.button(
            "New chat",
            type="primary",
            use_container_width=True,
            on_click=start_new_chat,
        )
        st.caption("Search chats")
        st.caption("Explore agents")
        st.caption("My library")
        st.divider()
        st.caption("RECENT CHATS")
        st.button(
            "Plan my launch week",
            use_container_width=True,
            on_click=open_saved_plan,
        )
        st.caption("Website copy ideas")
        st.caption("Customer interview insights")
        st.caption("A better morning routine")
        st.divider()
        st.caption("YESTERDAY")
        st.caption("Q4 research notes")
        st.caption("Reading list for November")
        st.divider()
        with st.container(border=True):
            st.markdown("**Room for bigger ideas**")
            st.caption("More agents. More possibilities.")
            st.caption("Explore Pro")
        st.caption("Personal workspace")
        st.caption("Free plan")
