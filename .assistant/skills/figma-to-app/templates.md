# File templates for figma-to-app

Canonical skeletons for the three files the skill writes. Replace every `<placeholder>`; keep the structure. Show these in the Phase 2 dry run so the preview matches what Phase 3 writes.

## `resources/<app_key>.app.yml`

```yaml
# Databricks App resource: https://docs.databricks.com/en/dev-tools/bundles/resources.html#apps
resources:
  apps:
    <app_key>:
      # App names are workspace-global; dev mode does NOT prefix them per user.
      # domain_friendly_name is DNS-friendly (e.g. adam-troup) — never short_name (underscores).
      name: <app-name>-${workspace.current_user.domain_friendly_name}
      description: <one-line description of what the app does>
      source_code_path: ../src/app
```

- `<app_key>`: snake_case (e.g. `translation_test`). `<app-name>`: kebab-case, 2–30 chars, lowercase letters/digits/hyphens only.
- For a stable production name, the `prod` target may override `name` without the developer suffix.

## `src/app/app.yaml`

```yaml
# Databricks Apps runtime configuration
# https://docs.databricks.com/en/dev-tools/databricks-apps/app-manifest.html
command:
  - streamlit
  - run
  - app.py

env:
  - name: APP_TITLE
    value: '<title shown in the app>'
```

- Env vars belong here, not in `databricks.yml`.
- Streamlit is pre-installed; only add `requirements.txt` when extra packages are needed.

## `src/app/app.py`

```python
"""<App name>: translated from a Figma mockup."""

import os

import streamlit as st

st.set_page_config(page_title="<title>", layout="<centered|wide>")


def inject_styles() -> None:
    """Figma styles from CSS_COPY_PASTE.md, condensed into one style block."""
    st.markdown(
        """
        <style>
        /* Map selectors from the Figma CSS dump here, e.g.:
        section[data-testid="stSidebar"] { background: <color>; }
        .figma-<class-name> { color: <color>; font-family: <font>; }
        */
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_<section_a>() -> None:
    """One function per section from the layout map."""
    ...


def render_<section_b>() -> None:
    """One function per section from the layout map."""
    ...


def main() -> None:
    st.title(os.environ.get("APP_TITLE", "<fallback title>"))
    render_<section_a>()
    render_<section_b>()


main()
```

## Dry-run output format

Structure the Phase 2 preview exactly as:

1. **Layout map** — indented tree of sections → containers → widgets, each node annotated with the Figma layer name it came from.
2. **CSS → Streamlit mapping** — GFM table: `Figma layer / class` | `Streamlit element` | `How style is applied`.
3. **Files to create** — full contents of each file, headed by its absolute path.
4. **Post-write commands** — `bundle validate --target dev --output JSON` (bundle root as working directory).
