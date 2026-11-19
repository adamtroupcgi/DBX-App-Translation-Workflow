---
name: figma-to-app
description: Translate a Figma mockup (PNG export + CSS dump) into a working Streamlit Databricks App inside a Declarative Automation Bundle. Read this skill when the user asks to generate, scaffold, or translate an app from a Figma design, mockup, or CSS deliverables.
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
    └── resources/ and src/app/   # where the app lands
```

## Phase 1 — Gather inputs

Collect and confirm before anything else:

1. **Mockup PNG** — look in `docs/mockups/` of the current repo by default. Read it to understand layout, sections, components.
    - If there is not a mockup image file in that exact location, get input from the user asking them to provide a path to where it exists.
2. **CSS dump** — typically `docs/mockups/CSS_COPY_PASTE.md`. Read the selectors, class names, colors, typography, and spacing it contains.
    - - If there is not a css dump in that exact location, get input from the user asking them to provide a path to where it exists.
3. **Bundle root** — the directory containing `databricks.yml` (confirm it has `include: resources/*.yml`). This skill/process should not occur if a databricks bundle does not already exist. **Never create your own bundle**.
4. **App name and key** — kebab-case name and snake_case resource key. Namespace the name per developer (see Guardrails).
5. **Interactivity** — ask which parts of the mockup are live widgets vs. static content. If unclear, propose a mapping and let the user correct it in the dry run.

If any input is missing or ambiguous, ask — do not guess paths or designs.

## Phase 2 — Dry run (mandatory, read-only)

Produce a preview of everything the generation will create, then **stop and wait for approval**. Present:

1. **Layout map** — hierarchy of the app derived from the PNG: page sections, rows, columns, which Figma layers become which Streamlit containers (`st.container`, `st.columns`, `st.tabs`).
2. **CSS → Streamlit mapping table** — each significant Figma selector/class → the Streamlit widget or element that will implement it, and how its style (color, font, spacing) will be applied.
3. **Full file contents** that will be written — every file shown in full: `resources/<app_key>.app.yml`, `src/app/app.yaml`, `src/app/app.py` (see [templates.md](templates.md)).
4. **Commands that will run** after writing (e.g. `bundle validate --target dev`).

Rules:
- **Do not create, edit, or delete any file during the dry run.** Reading is allowed; writing is not.
- Do not deploy. Deploying requires an explicit user request.
- End the dry run by asking for approval or corrections. Iterate on the preview as many times as the user wants — it is cheap; regenerating files is not.

## Phase 3 — Generate (only after approval)

1. Create each file with `createAsset`, using the **absolute bundle-root path** (e.g. `/Users/<user>/.../test-app/resources/<app_key>.app.yml`). Relative names can land the file in the wrong folder — always pass the absolute path.
2. Write content with `editAsset` immediately after creation (files are created empty).
3. Read existing files before overwriting. If `src/app/` already contains app files, show the user what will be replaced and confirm first.
4. Structure `app.py` around the dry-run layout map: one function per section, a shared `<style>` block built from the CSS dump, layout composition in a `main()`.

## Phase 4 — Validate

Run `bundle validate --target dev --output JSON` from the bundle root and confirm:
- The include picks up the new `resources/<app_key>.app.yml`.
- `resources.apps.<key>.name` resolves to a valid app name (lowercase letters, digits, hyphens; 2–30 chars).
- `source_code_path` resolves to the bundle's `src/app` directory.

Report the resolved app name back to the user. Offer `bundle deploy --target dev` as a follow-up, but never run it unprompted.

## Guardrails (Databricks Apps)

- **App names are workspace-global and unique.** Development mode does NOT prefix apps with the user name like jobs/pipelines. Namespace with `${workspace.current_user.domain_friendly_name}` (DNS-friendly, e.g. `adam-troup`); never use `${workspace.current_user.short_name}` (it produces underscores, which are invalid in app names).
- **Env vars live in `src/app/app.yaml`**, not in `databricks.yml` or the resource file.
- **Command is `['streamlit', 'run', 'app.py']`** — the canonical form. Streamlit is pre-installed in the Databricks Apps default environment; only add a `requirements.txt` when the app needs packages beyond the defaults.
- **Path resolution:** a resource file at `resources/*.yml` references the app with `source_code_path: ../src/app` (one level up to bundle root). `databricks.yml` itself would use `./src/app`.
- **Resource file naming:** `<app_key>.app.yml` (e.g. `test_app.app.yml`).
- **Styling:** Streamlit widgets accept no raw CSS. Apply Figma styles via a single `st.markdown(..., unsafe_allow_html=True)` `<style>` block built from the CSS dump, plus `st.columns`/`st.container` for layout. Map fonts and colors faithfully; prefer layout primitives over style hacks where possible.

## Files

- [templates.md](templates.md) — canonical skeletons for the app resource file, `app.yaml`, and `app.py`. Load it during Phase 2 (dry run) so the preview matches what will actually be written.
