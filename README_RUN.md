<!-- HEADER_COMMENT_AUTOGEN -->
<!-- FILE: README_RUN.md -->
<!-- PURPOSE: Documentation file. -->

Run Guide — Flask Quiz App
===========================

This document explains how to run this Flask quiz project on a Windows machine (PowerShell). It also shows how to generate a PDF of this guide.

Prerequisites
- Python 3.8+ installed and on PATH
- PowerShell (Windows PowerShell v5.1 is fine)

Quick steps (copy/paste in PowerShell)

1) Open PowerShell and go to the project folder

```powershell
cd 'C:\path\to\flask-quiz-app-main\flask-quiz-app-main'
```

2) Create & activate a virtual environment

```powershell
python -m venv venv
# Activate
.\venv\Scripts\Activate.ps1
```

If activation is blocked, run once in this PowerShell session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

3) Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

4) Create the database and default admin

```powershell
python create_db.py
```

This script creates the `quiz.db` SQLite file, default categories, and an admin user:
- username: `admin`
- password: `admin123`

5) Run the app locally

```powershell
python main.py
```

Open the app in a browser: http://127.0.0.1:5000

Optional: run on LAN (access from other devices)

A) Quick dev command (bind to all interfaces):

```powershell
# using flask CLI
$env:FLASK_APP = 'main.py'
$env:FLASK_ENV = 'development'
flask run --host=0.0.0.0 --port=5000
```

B) Or edit `main.py` and set host to '0.0.0.0'

Firewall: allow incoming connections for port 5000 if you want other machines to connect.

Generate a PDF of this guide (two options)

Option A — Use Pandoc (if available):

1. Install pandoc (https://pandoc.org/installing.html)
2. Run:

```powershell
pandoc README_RUN.md -o run_guide.pdf
```

Option B — Use the provided Python script (requires `reportlab`):

1. Install reportlab inside venv:

```powershell
pip install reportlab
```

2. Run the generator script:

```powershell
python generate_run_guide_pdf.py
```

After running, `run_guide.pdf` will be created in the project root.

Troubleshooting
- "python" not found: install Python and add to PATH.
- Activation blocked: use `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`.
- Port 5000 blocked: choose a different port or allow it in Windows Firewall.
- DB errors: confirm `quiz.db` file created and `create_db.py` ran without errors.

Extras you might like me to add
- `run.ps1` script to activate venv and run the app in one command
- `run_guide.pdf` pre-built in the repo
- Dockerfile for containerized runs

If you want, I can now add the `generate_run_guide_pdf.py` script so you can create the PDF locally. Which option do you prefer (I will add the Python PDF generator now if you say yes)?
