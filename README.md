BillBot

BillBot is a full-stack app built with FastAPI (Python backend) and React + Vite (frontend).
It allows users to upload grocery bills, extract text using OCR, and display it in a sleek dark-themed dashboard.

python -m venv venv ---- for starting virtual environment


// for backend
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload 

python train.py


// for frontend
npm start                     
 