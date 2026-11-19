# DBX-App-Translation-Workflow

This is a test repo to explore a workflow that translates Figma deliverables into a functioning application (or at least front end) in Databricks Apps. Since Python knowledge is most applicable to Databricks engineers, Streamlit will be used for a Python-only solution.

## Step 1: Figma Deliverables

I created a mock Figma diagram using an agent to serve as an example. Once the diagram was complete, I:

1. Exported the Figma diagram as a png and dropped it in the repo: `docs/mockups/Translation Test Mockup.png`
2. Copied the full CSS from the diagram editor:
    - Select the entire Figma diagram using CTRL+A in the editor
    - Right clicked the highlighted selection
    - Clicked Copy/Paste as > Copy as code > CSS (all layers)
    - Dumped the copied CSS into `docs/mockups/CSS_COPY_PASTE.md`

This brought all the needed references into the repo for the agent to utilize in scaffolding the app.

## Step 2: Utilize existing bundle

Since bundles can contain more than just the app itself, I created the bundle first under `test-app`.