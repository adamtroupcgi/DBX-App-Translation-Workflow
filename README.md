# DBX-App-Translation-Workflow

Use this repository to translate Figma deliverables into a Streamlit application for Databricks Apps. The workflow uses Python only and requires an existing Declarative Automation Bundle.

## Step 1: Prepare Figma deliverables

Provide a mockup image and a CSS export from Figma:

1. Export the mockup as a PNG and save it under `docs/mockups/`, for example `docs/mockups/Translation Test Mockup.png`.
2. In Figma, select the layers to export. Choose **Copy/Paste as > Copy as code > CSS (all layers)**.
    - You can also use CTRL+A in the editor to select all components of the diagram.
3. Save the copied CSS to `docs/mockups/CSS_COPY_PASTE.md`.

The skill looks in `docs/mockups/` for these files by default. If they are stored elsewhere, provide their paths when prompted.

## Step 2: Prepare the bundle

Open an existing Declarative Automation Bundle, such as `test-app`. Its `databricks.yml` must include the app resource files (for example, `resources/*.yml`). The skill does not create a bundle.

## Step 3: Run the skill

In Copilot Chat, run `/figma-to-app`. The skill will:

1. Read the mockup and CSS, locate the bundle, and ask about app behavior and naming.
2. Present a dry run with the proposed layout, files, dependencies, and local run instructions. Review it and approve it before files are created.
3. Generate a modular Streamlit app and its Databricks bundle resource configuration.
4. Document how to create a local Python environment and run the app from a terminal. The skill uses an isolated `.venv` when no existing environment convention applies and ensures it is ignored by Git.
5. Run local syntax/tests and validate the bundle. The skill starts the local app only if you opt in; deployment always requires a separate explicit request.

## Run locally

From the bundle root, follow the local development commands added to its README. For the default setup, the app entry point is `src/app/app.py`.

## Deploy to Databricks Apps

The app runtime manifest is `{bundle_name}/src/app/app.yaml`, and the bundle resource is `{bundle_name}/resources/<app_key>.app.yml`. After validating the bundle, deploy it using either method:

- In the Databricks Apps UI, create or edit an app and choose **Deploy from source**. Set the source to the directory containing `app.yaml` (for this repository, `test-app/src/app/`).
- From the bundle root, use the Databricks CLI to validate and deploy the configured app resource.