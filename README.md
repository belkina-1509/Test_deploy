# User Database CLI

Simple SQLite-based CLI to manage users (add, search, delete, list).

## Requirements

- Python 3.9+

No external dependencies are required.

## Setup

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run

```powershell
python utils.py
```

## Configuration

- `APP_DATABASE` - path to SQLite database file (default: `test.db`)
- `APP_LOG_LEVEL` - logging level (default: `INFO`)

Example:

```powershell
$env:APP_DATABASE="data\app.db"
$env:APP_LOG_LEVEL="DEBUG"
python utils.py
```
