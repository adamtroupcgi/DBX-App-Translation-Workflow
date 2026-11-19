---
name: figma-to-app
description: Translate a Figma mockup and CSS dump into a modular Streamlit Databricks App with a documented local run workflow inside an existing Declarative Automation Bundle. Use when generating, scaffolding, or translating an app from Figma deliverables.
---

# Figma Mockup → Databricks App (Streamlit)

Scaffold a Streamlit app from Figma deliverables inside an existing Declarative Automation Bundle. **Always run the four phases in order: Gather inputs → Dry run → Generate → Validate.** The dry run is mandatory — never skip it, and never write files during it.

The typical source layout (from this repo) is:

```
repo/
├── docs/mockups/
│   ├── <Mockup>.png              # Figma diagram exported as PNG. This could also be a JPEG but will work the same
│   └── CSS_COPY_PASTE.md         # Figma "Copy as code → CSS (all layers)" dump
└── test-app/                    # bundle root (contains databricks.yml)
    ├── resources/                # bundle resource declarations
    └── src/app/                  # Databricks app source and runtime manifest
```

## Phase 1 — Gather inputs

Collect and confirm before anything else:

1. **Mockup PNG** — look in `docs/mockups/` of the current repo by default. Read it to understand layout, sections, components.
    - If there is not a mockup image file in that exact location, get input from the user asking them to provide a path to where it exists.
2. **CSS dump** — typically `docs/mockups/CSS_COPY_PASTE.md`. Read the selectors, class names, colors, typography, and spacing it contains.
    - If there is not a CSS dump in that exact location, ask the user for its path.
3. **Bundle root** — the directory containing `databricks.yml` (confirm it has `include: resources/*.yml`). This skill/process should not occur if a databricks bundle does not already exist. **Never create your own bundle**.
4. **App name and key** — kebab-case name and snake_case resource key. Namespace the name per developer (see Guardrails).
5. **Interactivity** — ask which parts of the mockup are live widgets vs. static content. If unclear, propose a mapping and let the user correct it in the dry run.
6. **Existing Python setup** — inspect the bundle's `.gitignore`, Python manifests/lockfiles, virtual environments, tests, and existing `src/app` structure. Reuse the project's package manager and conventions; do not create a competing package manager or overwrite existing app files.
7. **Local launch preference** — tell the user that a local terminal run path will be included, and ask whether they want the agent to start and verify the app after implementation. Do not start a long-running server unless they explicitly opt in.

If any input is missing or ambiguous, ask — do not guess paths or designs.

## Phase 2 — Dry run (mandatory, read-only)

Produce a concise preview of what the generation will create, then **stop and wait for approval**. Present:

1. **Layout map** — hierarchy of the app derived from the PNG: page sections, rows, columns, which Figma layers become which Streamlit containers (`st.container`, `st.columns`, `st.tabs`).
2. **CSS → Streamlit mapping table** — each significant Figma selector/class → the Streamlit widget or element that will implement it, and how its style (color, font, spacing) will be applied.
3. **Planned file tree** — list generated files with a brief responsibility for each; keep `app.py` as a thin entry point and put views/components/styles/state into focused modules as appropriate.
4. **Bundle configuration** — show full contents only for the small Databricks-specific files, especially `resources/<app_key>.app.yml` and `src/app/app.yaml`. Summarize Python modules; do not paste full Python source files, generated stylesheets, or every file into the chat. Show source snippets only when needed to explain a design choice.
5. **Python setup and local run** — summarize the package manager/dependencies, `.gitignore` additions, README instructions, and exact terminal commands for Windows and POSIX where practical. Include whether the agent will start the app only if the user opted in.
6. **Validation commands** — include the local syntax/test checks and `databricks bundle validate --target dev --output JSON`.

Rules:
- **Do not create, edit, or delete any file during the dry run.** Reading is allowed; writing is not.
- Do not include complete generated app source code in the dry-run response. The files will be written to the workspace after approval; the response should describe their structure and show only bundle-specific configuration.
- Do not deploy. Deploying requires an explicit user request.
- End the dry run by asking for approval or corrections. Iterate on the preview as many times as the user wants — it is cheap; regenerating files is not.

## Phase 3 — Generate (only after approval)

1. Use the repository's existing package manager, Python source layout, and test conventions. If there is no Python package setup, use the default described in [templates.md](templates.md).
2. Keep the app maintainable and proportionate to its complexity. Use a thin `src/app/app.py` entry point, separate page/view modules, and shared `components/`, `styles.py`, or state/service modules when they have distinct responsibilities. Avoid placing the entire application in `app.py`; also avoid creating empty or unnecessary layers.
3. Put app modules and Databricks runtime files under `src/app/`, so the configured `source_code_path` includes them. Add or update `README.md` with the local run instructions.
4. Read existing files before overwriting. If `src/app/` already contains app files, identify replacements and get confirmation before overwriting.
5. Preserve existing `.gitignore` entries and ensure local environments and Python caches are ignored. Never add a virtual environment to source control or the deployed app source.
6. Create/update dependency manifests only as previewed and approved. Use an isolated `.venv` at the bundle root when no existing environment convention applies; install dependencies into it from the selected manifest.
7. If the user opted into local startup, run the app using the documented local command and verify it responds. Otherwise, do not start a server; report the commands to run it.

## Phase 4 — Validate

From the bundle root, run the relevant Python syntax/tests and `databricks bundle validate --target dev --output JSON`. Confirm:
- The include picks up the new `resources/<app_key>.app.yml`.
- `resources.apps.<key>.name` resolves to a valid app name (lowercase letters, digits, hyphens; 2–30 chars).
- `source_code_path` resolves to the bundle's `src/app` directory.
- The app can be launched locally using the documented command, or report clearly that local startup was not requested or could not be verified.

Report the resolved app name back to the user. Offer `bundle deploy --target dev` as a follow-up, but never run it unprompted.

## Guardrails (Databricks Apps)

- **App names are workspace-global and unique.** Development mode does NOT prefix apps with the user name like jobs/pipelines. Namespace with `${workspace.current_user.domain_friendly_name}` (DNS-friendly, e.g. `adam-troup`); never use `${workspace.current_user.short_name}` (it produces underscores, which are invalid in app names).
- **Env vars live in `src/app/app.yaml`**, not in `databricks.yml` or the resource file.
- **Command is `['streamlit', 'run', 'app.py']`** — the canonical Databricks form, executed with `src/app/` as the working directory. For local development, provide a separate command from the bundle root that runs `src/app/app.py`.
- **Path resolution:** a resource file at `resources/*.yml` references the app with `source_code_path: ../src/app` (one level up to bundle root). `databricks.yml` itself would use `./src/app`.
- **Resource file naming:** `<app_key>.app.yml` (e.g. `test_app.app.yml`).
- **Python packages and environments:** reuse an existing package manager and lockfile. The deployable dependency manifest must be available under `source_code_path`; if the existing manifest lives above `src/app/`, provide a supported export/sync step or a Databricks-compatible manifest rather than assuming it will be installed. If no setup exists, use `src/app/requirements.txt` for runtime dependencies (including Streamlit for a reproducible local run) and a bundle-root `.venv/` for local installation. Databricks may include Streamlit in its default image, but the explicit dependency supports local setup. Keep the dependency source of truth clear; do not maintain duplicate manifests without a documented need.
- **Ignore local artifacts:** preserve `.gitignore` and add missing entries for `.venv/`, `venv/`, `__pycache__/`, `*.py[cod]`, and relevant test/linter caches. Keep the virtual environment outside `src/app/`.
- **Local run docs:** document environment creation, dependency installation, the exact `streamlit run` command, and how to stop it in the bundle README. Ask before starting a local server; never deploy without an explicit request.
- **App organization:** keep `app.py` as a small entry point. Separate pages, reusable UI, styling, and nontrivial state/data logic into modules according to actual app complexity.
- **Styling:** Streamlit widgets accept no raw CSS. Apply Figma styles via a single `st.markdown(..., unsafe_allow_html=True)` `<style>` block built from the CSS dump, plus `st.columns`/`st.container` for layout. Map fonts and colors faithfully; prefer layout primitives over style hacks where possible.

## Files

- [templates.md](templates.md) — canonical bundle configuration, default Python setup, modular app structure, and local run commands. Load it during Phase 2 (dry run).
