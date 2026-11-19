"""Streamlit entry point for Orbit."""

import os

import streamlit as st

from orbit_app.pages.home import render_home
from orbit_app.pages.plan import render_plan
from orbit_app.sidebar import render_sidebar
from orbit_app.state import initialize_state
from orbit_app.styles import inject_styles

st.set_page_config(
    page_title=os.environ.get("APP_TITLE", "Orbit"),
    layout="wide",
    initial_sidebar_state="expanded",
)


def main() -> None:
    initialize_state()
    inject_styles()
    render_sidebar()
    if st.session_state["screen"] == "plan":
        render_plan()
    else:
        render_home()


main()
