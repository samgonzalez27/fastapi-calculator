# FastAPI Calculator - Module 8

This repository contains a small FastAPI-based calculator application with unit, integration, and end-to-end tests, structured logging, and a GitHub Actions CI workflow.

Files added:
- `app/` - FastAPI application and calculator logic
- `tests/` - pytest test suite (unit, integration, e2e)
- `requirements.txt` - Python dependencies
- `.github/workflows/ci.yml` - CI workflow that runs tests on push/PR

Quick start

1. Create and activate a virtualenv (recommended):

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app locally:

```bash
uvicorn app.main:app --reload
```

4. Run tests:

```bash
pytest -q
```

Notes

- The end-to-end test starts a uvicorn server as a subprocess — it requires `uvicorn` to be installed in the same environment running pytest.
