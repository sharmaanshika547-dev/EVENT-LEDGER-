# EventLedger

EventLedger is a backend service for tracking events and activities.

This project is part of a structured backend learning roadmap covering:

- Flask backend development
- PostgreSQL databases
- Redis background workers
- Docker containerization
- AWS deployment
- Blockchain verification

---

## Features

- Health check API
- Event management API (coming next)
- Modular backend architecture

---

## Project Structure

eventledger/

app/
routes/
models/
services/
__init__.py

run.py
requirements.txt

---

## Setup

1. Create virtual environment

python3 -m venv venv

2. Activate environment

source venv/bin/activate

3. Install dependencies

pip install -r requirements.txt

4. Run server

python run.py

---

## API Endpoints

GET /

Returns basic API status.

GET /health

Returns health status.

---

## Roadmap

- [x] Project initialization
- [x] Flask server setup
- [x] Health endpoint
- [ ] Events API
- [ ] Database integration
- [ ] Redis background jobs
- [ ] Docker deployment
- [ ] AWS deployment
