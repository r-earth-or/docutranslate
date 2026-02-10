# Repository Guidelines

## Project Structure & Module Organization
Core Python code is in `docutranslate/`.
- `docutranslate/workflow/`: file-type workflows (`*_workflow.py`) that orchestrate conversion, translation, and export.
- `docutranslate/converter/`, `docutranslate/translator/`, `docutranslate/exporter/`: pipeline stages.
- `docutranslate/app.py`: FastAPI/Web UI backend entrypoint.
- `docutranslate/cli.py`: CLI entry (`docutranslate` command).
- `docutranslate/static/` and `docutranslate/template/`: bundled frontend/static assets.
- Packaging/build files live at root: `pyproject.toml`, `Dockerfile`, `*.spec`, `.github/workflows/`.

## Build, Test, and Development Commands
- `uv sync`: install project dependencies from `pyproject.toml`/`uv.lock`.
- `uv run docutranslate -i`: start local Web UI + API (default `127.0.0.1:8010`).
- `uv run docutranslate -i -p 8011 --cors`: run on a custom port with CORS enabled.
- `docker run -d -p 8010:8010 xunbu/docutranslate:latest`: run the published container locally.
- `uv pip install pyinstaller && uv run pyinstaller lite.spec --noconfirm --clean -y`: build a lightweight desktop package (see also `full.spec`, `lite_mac.spec`).

## Coding Style & Naming Conventions
- Follow Python 3.11+ conventions and PEP 8: 4-space indentation, clear type-oriented config classes, small focused functions.
- Use `snake_case` for modules/functions/variables and `PascalCase` for classes.
- Keep workflow naming consistent: `xxx_workflow.py`, matching config and workflow class names.
- Prefer explicit, composable configs over hard-coded provider values.

## Testing Guidelines
There is currently no first-party `tests/` suite or enforced coverage gate in this repository.
- For behavior changes, run a manual smoke test: start `docutranslate -i`, open `/docs`, and execute at least one translation path you touched.
- If you add automated tests, place them under `tests/` with `test_*.py` names and keep fixtures small and file-type specific.

## Commit & Pull Request Guidelines
Recent history favors short, imperative commit subjects (Chinese or English), for example: `Fix Gemini provider tag`, `Add regex dependency`, `Add Vietnamese`.
- Keep subject lines concise and action-focused.
- In PRs, include: what changed, why, how you validated it, and UI screenshots when `docutranslate/static/` or interface behavior changes.
- Link related issues and note any new env vars/API provider requirements.

## Security & Configuration Tips
- Never commit real API keys or tokens.
- Keep provider credentials in environment variables or local untracked config.
- For LAN exposure, use `--host 0.0.0.0` intentionally and restrict network access as needed.
