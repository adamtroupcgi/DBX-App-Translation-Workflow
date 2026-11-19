"""Shared CSS for the Orbit mockup."""

import streamlit as st


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            --orbit-green: #244C3D;
            --orbit-ink: #202C27;
            --orbit-muted: #747C75;
            --orbit-paper: #FDFCF9;
            --orbit-sidebar: #F2F3ED;
            --orbit-border: #DFE4D9;
        }
        .stApp { background: var(--orbit-paper); color: var(--orbit-ink); }
        section[data-testid="stSidebar"] {
            background: var(--orbit-sidebar);
            min-width: 240px;
            max-width: 240px;
        }
        .block-container {
            max-width: 1440px;
            padding-top: 1.5rem;
            padding-bottom: 1rem;
        }
        h1, h2, h3, p, label, button, textarea, input, div {
            font-family: Inter, Arial, sans-serif;
        }
        h1, h2, h3 { color: var(--orbit-ink); }
        [data-testid="stVerticalBlockBorderWrapper"] {
            border-color: var(--orbit-border);
            border-radius: 14px;
        }
        .stButton > button,
        [data-testid="stFormSubmitButton"] > button,
        [data-testid="stDownloadButton"] > button {
            border-radius: 10px;
            border-color: var(--orbit-border);
        }
        .stButton > button[kind="primary"],
        [data-testid="stFormSubmitButton"] > button,
        [data-testid="stDownloadButton"] > button {
            background: var(--orbit-green);
            color: white;
        }
        [data-testid="stTextArea"] textarea,
        [data-testid="stTextInput"] input {
            border-color: var(--orbit-border);
            border-radius: 10px;
            background: white;
        }
        @media (max-width: 900px) {
            section[data-testid="stSidebar"] {
                min-width: 0;
                max-width: 100%;
            }
            .block-container { padding: 1rem; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
