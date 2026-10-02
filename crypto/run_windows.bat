@echo off
cd /d %~dp0
if not exist .venv python -m venv .venv
call .venv\Scriptsctivate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run dashboardpp.py
pause
