# 🚀 AI-Powered Task & Knowledge Management System

<p align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi)
![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql)
![FAISS](https://img.shields.io/badge/FAISS-Vector%20Search-orange?style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=for-the-badge&logo=docker)

</p>

> **An AI-powered knowledge management platform that enables document storage, semantic search, intelligent task management, and role-based collaboration using FastAPI, React, MySQL, and FAISS.**

---

# ✨ Features

## 🔐 Authentication & Authorization
- JWT Authentication
- Role-Based Access Control (Admin/User)
- Secure Password Hashing (bcrypt)
- Protected API Endpoints

---

## 📄 Document Management

- Upload PDF and TXT files
- Automatic text extraction
- AI-generated vector embeddings
- Local FAISS indexing
- Document metadata storage

---

## 🔍 AI Semantic Search

- Sentence Transformer Embeddings
- FAISS Vector Database
- Natural Language Search
- Relevant Document Retrieval
- High-Speed Similarity Matching

---

## ✅ Task Management

- Create Tasks
- Assign Tasks
- Update Status
- Task Filtering
- Task Tracking
- Due Date Management

---

## 📊 Analytics Dashboard

- User Activity
- Task Statistics
- Upload Statistics
- Search Activity
- System Logs

---

## 📝 Activity Logging

System automatically records:

- User Login
- Document Upload
- Search Queries
- Task Updates
- User Activities

---

# 🏗️ System Architecture

```
                React Frontend
                      │
                REST API (FastAPI)
                      │
      ┌───────────────┼───────────────┐
      │                               │
  MySQL Database                 AI Engine
      │                     Sentence Transformers
      │                               │
      └──────────────► FAISS ◄────────┘
               Semantic Vector Search
```

---

# 📂 Project Structure

```
AI-Powered-Task-Knowledge-Management-System
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── main.py
│   │
│   ├── storage/
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── Dockerfile
│
├── docker-compose.yml
├── README.md
└── .gitignore
```

---

# ⚙️ Tech Stack

## 🚀 Backend

| Technology | Purpose |
|------------|---------|
| FastAPI | REST API Framework |
| SQLAlchemy | ORM |
| MySQL | Relational Database |
| PyMySQL | MySQL Driver |
| JWT | Authentication |
| Passlib (bcrypt) | Password Encryption |
| Pydantic | Validation |
| pdfplumber | PDF Parsing |
| Sentence Transformers | AI Embeddings |
| FAISS | Semantic Search |
| NumPy | Numerical Processing |
| Uvicorn | ASGI Server |

---

## 💻 Frontend

| Technology | Purpose |
|------------|---------|
| React 18 | UI Development |
| Vite | Build Tool |
| React DOM | Rendering |
| Nginx | Production Deployment |

---

## ☁️ DevOps

- Docker
- Docker Compose

---

# 🚀 Getting Started

## Clone Repository

```bash
git clone https://github.com/BharathHU/AI-Powered-Task-Knowledge-Management-System.git

cd AI-Powered-Task-Knowledge-Management-System
```

---

# 🐳 Run with Docker

```bash
docker compose up --build
```

### Application URLs

| Service | URL |
|----------|-----|
| Frontend | http://localhost:5173 |
| Backend | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |

---

# 🖥️ Manual Setup

## Backend

```bash
cd backend

python -m venv .venv

# Windows
.venv\Scripts\activate

pip install -r requirements.txt

copy .env.example .env

uvicorn app.main:app --reload
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

---

# 👤 Default Login

## Admin

```
Email:
      admin@example.com

Password:
admin123
```

---

## User

```
Email:
user@example.com

Password:
user123
```

---

# 📡 API Documentation

Swagger UI

```
http://localhost:8000/docs
```

---

# 📸 Screenshots

> Add screenshots here

```
📷 Login Page

📷 Dashboard

📷 Upload Document

📷 Semantic Search

📷 Task Management

📷 Analytics
```

---

# 🔥 Key Highlights

- JWT Authentication
- Role-Based Authorization
- AI Semantic Search
- FAISS Vector Search
- FastAPI REST APIs
- React Frontend
- MySQL Integration
- Dockerized Deployment
- Activity Logging
- Analytics Dashboard

---

# 🚀 Future Improvements

- OpenAI / Gemini Integration
- OCR Support
- Multi-language Search
- Email Notifications
- Team Collaboration
- Cloud Deployment (AWS/Azure)
- Redis Caching
- Elasticsearch Support

---

# 👨‍💻 Author

## **Bharath H U**

📧 Email: **bharathhubharath@gmail.com**

🔗 GitHub:
https://github.com/BharathHU

---

## ⭐ If you like this project, consider giving it a Star!
