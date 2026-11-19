# test-app

## Getting Started

To deploy and manage this bundle, follow these steps:

### 1. Deployment

- Click the **deployment rocket** 🚀 in the left sidebar to open the **Deployments** panel, then click **Deploy**.

### 2. Running Jobs & Pipelines

- To run a deployed job or pipeline, hover over the resource in the **Deployments** panel and click the **Run** button.

### 3. Managing Resources

- Use the **Add** dropdown to add resources to the bundle.
- Click **Schedule** on a notebook within the bundle to create a **job definition** that schedules the notebook.

## Documentation

- For information on using **Declarative Automation Bundles in the workspace**, see: [Declarative Automation Bundles in the workspace](https://docs.databricks.com/aws/en/dev-tools/bundles/workspace-bundles)
- For details on the **Declarative Automation Bundles format** used in this bundle, see: [Declarative Automation Bundles Configuration reference](https://docs.databricks.com/aws/en/dev-tools/bundles/reference)

## Local development

Run these commands from the `test-app` bundle root.

### Windows (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r src\app\requirements.txt
.\.venv\Scripts\python.exe -m streamlit run src\app\app.py
```

### macOS/Linux

```sh
python3 -m venv .venv
./.venv/bin/python -m pip install -r src/app/requirements.txt
./.venv/bin/python -m streamlit run src/app/app.py
```

Press `Ctrl+C` in the terminal to stop the local server. The current mockup uses static sample plan content; it does not connect to an AI service.
