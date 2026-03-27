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


### Delete Event

DELETE /events/<id>

Deletes an event by its ID.

#### Example:

DELETE /events/1

#### Response:

Success:
```json
{
  "message": "Event deleted"
}

### Get Single Event

GET /events/<id>

Returns a specific event.

#### Example:

GET /events/1


# 📌 Event Ledger Backend

A Flask-based backend application that allows users to register, authenticate, and manage their events with proper authorization using JWT and a database.

---

# 🚀 Features

* User Registration & Login
* JWT-based Authentication
* Protected Routes (Middleware)
* Event CRUD (in progress)
* User-specific data filtering
* Database integration using SQLAlchemy

---

# 🧠 Tech Stack

* Python (Flask)
* SQLAlchemy (ORM)
* SQLite (Database)
* JWT (Authentication)

---

# 📁 Project Structure

```
app/
├── __init__.py        # App factory + config
├── extensions.py      # DB instance
├── models/
│   └── event.py       # Event model (table)
├── routes/
│   ├── auth.py        # Auth routes + middleware
│   └── events.py      # Event routes
run.py                 # Entry point
events.db              # SQLite database
```

---

# ⚙️ Setup Instructions

## 1. Create virtual environment

```
python3 -m venv venv
source venv/bin/activate
```

## 2. Install dependencies

```
pip install flask flask-sqlalchemy pyjwt
```

## 3. Run the app

```
python3 run.py
```

---

# 🧠 Core Concepts Learned

## 🔹 ORM (SQLAlchemy)

* `class Event(db.Model)` → table
* Object → row
* `db.Column` → column

---

## 🔹 Database Operations

```
Create → Event(...)
Add → db.session.add()
Save → db.session.commit()
Read → Event.query.all()
Filter → Event.query.filter_by(...)
```

---

## 🔹 Authentication (JWT)

* Token generated at login
* Payload contains user identity
* Token sent via headers

---

## 🔹 Middleware (Decorator)

```
@token_required
```

* Runs before route
* Extracts user_id from JWT
* Attaches to request

---

## 🔹 Authorization

```
Event.query.filter_by(user_id=current_user_id)
```

* Ensures users only access their own data

---

# 🔄 Request Flow

```
Client → JWT → Flask → Middleware → DB → JSON Response
```

---

# 🧪 API Endpoints

## 🔹 Auth

* POST `/auth/register`
* POST `/auth/login`

---

## 🔹 Events

* GET `/events` (Protected)

---

# ⚠️ Important Notes

* Database persists data across runs
* Do NOT insert data in `run.py`
* Always use `commit()` to save changes
* Middleware must attach `request.user_id`

---

# 📈 Future Improvements

* Add POST /events
* Add PUT /events/<id>
* Add DELETE /events/<id>
* Integrate PostgreSQL
* Add proper user table
* Password hashing (bcrypt)

---

# 💙 Learning Highlights

* Transition from in-memory data → database
* Understanding ORM vs raw SQL
* Implementing authentication + authorization
* Building real backend architecture

---

# 🙌 Final Note

This project marks the transition from basic coding to real backend development with proper structure, persistence, and security.
