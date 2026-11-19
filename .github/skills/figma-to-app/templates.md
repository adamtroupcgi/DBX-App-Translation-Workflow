# Figma-to-app implementation templates

Use these defaults only when the bundle does not already establish a package manager, Python layout, or local development convention. Preserve and extend existing project conventions instead of creating parallel tooling.

## Recommended app structure

Keep the Databricks source root self-contained. `app.py` should initialize the app and route between views; put each distinct responsibility in a small module. Scale the structure to the design and omit modules that do not add value.

```text
<bundle-root>/
├── .gitignore
├── README.md
├── resources/
│   └── <app_key>.app.yml
└── src/
    └── app/
        ├── app.py                 # Thin Streamlit entry point
        ├── app.yaml               # Databricks Apps runtime configuration
        ├── requirements.txt       # Runtime and local Python dependencies, if needed
        └── <app_package>/
            ├── __init__.py
            ├── pages/             # One module per screen or major view
            ├── components/        # Shared UI components, when reused
            ├── styles.py          # CSS/theme injection
            └── state.py           # Session-state helpers, when needed
```

Add a data or service module only when the app has meaningful logic for it. Do not put the entire UI, CSS, data, and interaction logic in `app.py`.

## `resources/<app_key>.app.yml`

```yaml
resources:
  apps:
    <app_key>:
      name: "<kebab-case-app-name>-${workspace.current_user.domain_friendly_name}"
      description: "<one-line description>"
      source_code_path: ../src/app
```

- `<app_key>` is snake_case; `<kebab-case-app-name>` uses lowercase letters, digits, and hyphens.
- Keep the resolved name between 2 and 30 characters. App names are workspace-global; namespace with `domain_friendly_name`, not `short_name`.
- A resource under `resources/` resolves `source_code_path: ../src/app` from the bundle root.

## `src/app/app.yaml`

```yaml
command:
  - streamlit
  - run
  - app.py

env:
  - name: APP_TITLE
    value: "<app title>"
```

The Databricks command runs relative to the app source root. Keep environment variables here, not in `databricks.yml` or the resource file.

## Python dependencies and local environment

1. Inspect the bundle for a Python manifest/lockfile and use its package manager if present.
2. Ensure the dependency manifest Databricks uses is under `src/app/`. If an existing manifest is outside that directory, use a supported export/sync workflow or add a Databricks-compatible manifest and document the source of truth.
3. If there is no existing Python package setup, create `src/app/requirements.txt` with `streamlit` and only the additional packages the app actually imports. Do not add placeholder dependencies.
4. Use a `.venv/` at the bundle root for the local environment. Keep it outside `src/app/` so it is neither deployed as app source nor synchronized as a bundle file.
5. Preserve the bundle's `.gitignore` and add any missing local-artifact rules:

```gitignore
.venv/
venv/
__pycache__/
*.py[cod]
.pytest_cache/
.mypy_cache/
.ruff_cache/
```

6. Add a **Local development** section to the bundle `README.md`. For the default `requirements.txt` setup, document:

```powershell
# Run from the bundle root on Windows
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r src\app\requirements.txt
.\.venv\Scripts\python.exe -m streamlit run src\app\app.py
```

```sh
# Run from the bundle root on macOS/Linux
python3 -m venv .venv
./.venv/bin/python -m pip install -r src/app/requirements.txt
./.venv/bin/python -m streamlit run src/app/app.py
```

Document that `Ctrl+C` stops the local server. If the project uses another package manager, give the equivalent environment/install/run commands instead. Ask whether the user wants the agent to start and verify the server; do not start a long-running process without an explicit yes.

## Phase 2 dry-run output

Show:

1. The Figma-to-Streamlit layout map and a concise CSS mapping table.
2. A planned file tree with a one-line responsibility per file/module.
3. Full contents of the Databricks-specific resource YAML and `app.yaml`.
4. A concise summary of Python dependencies, package manager, `.gitignore` additions, README local-run instructions, and local launch preference.
5. Local validation and bundle-validation commands.

Do **not** paste full generated Python source, CSS, or every file into the response. The user approves the implementation plan; source is written to the workspace after approval. Include source snippets only when needed to explain a specific decision.
