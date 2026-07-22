# IAM Application

An enterprise-grade Identity and Access Management (IAM) application built using **FastAPI**, **SQLAlchemy**, **PostgreSQL**, and **Alembic**. This project follows a clean, layered architecture to provide a scalable foundation for user identity, authentication, authorization, and organization management in multi-tenant applications.

---

## 🚀 Tech Stack

- **Language:** Python 3.12+
- **Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy 2.x
- **Database Migration:** Alembic
- **Package Manager:** uv

---

## 📂 Project Structure

```
app/
├── config/          # Database and application configuration
├── models/          # SQLAlchemy ORM models
├── repositories/    # Data access layer
├── services/        # Business logic layer
├── schemas/         # Pydantic request/response models (In Progress)
├── routes/          # FastAPI API endpoints (In Progress)
├── utils/           # Utility functions
├── main.py          # Application entry point
└── __init__.py
```

---

## ✅ Features Implemented

### Database Layer
- PostgreSQL configuration
- SQLAlchemy integration
- Database session management
- Declarative base model setup

### Database Models
- User
- Identity
- User Details
- Organization
- User Organization
- Credential
- Password History
- Authentication Policy
- MFA Factor
- MFA Challenge
- Role
- User Role
- Role Swap
- Group
- User Group
- User Audit Log

### Database Migration
- Alembic configuration
- Initial migration generation
- Schema successfully migrated to PostgreSQL

### Repository Layer
- Generic Base Repository
- User Repository
- Identity Repository
- Organization Repository
- User Details Repository

### Service Layer
- Base Service
- User Service
- Identity Service
- Organization Service
- User Details Service
- Centralized service exceptions

---

## 🚧 Work In Progress

- Pydantic Schemas
- FastAPI API Endpoints
- JWT Authentication
- Password Hashing
- Authorization (RBAC)
- Dependency Injection
- Request Validation
- API Documentation
- Unit & Integration Testing

---

## 🛠️ Getting Started

### Clone the Repository

```bash
git clone https://github.com/devadharshini-0707/IAM_Application.git
cd IAM_Application
```

### Create Virtual Environment

```bash
uv venv
```

### Install Dependencies

```bash
uv sync
```

### Configure Environment Variables

Create a `.env` file and configure your PostgreSQL database connection.

Example:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/iam_db
```

### Apply Database Migrations

```bash
alembic upgrade head
```

### Run the Application

```bash
uv run uvicorn app.main:app --reload
```

---

## 📌 Architecture

The project follows a layered architecture:

```
API Layer (Routes)
        │
        ▼
Service Layer
        │
        ▼
Repository Layer
        │
        ▼
Database (SQLAlchemy + PostgreSQL)
```

This separation keeps business logic, data access, and API handling independent and maintainable.

---

## 📅 Development Status

| Module | Status |
|---------|--------|
| Database Configuration | ✅ Completed |
| SQLAlchemy Models | ✅ Completed |
| Alembic Migration | ✅ Completed |
| Repository Layer | ✅ Completed |
| Service Layer | ✅ Completed |
| Schemas | 🚧 In Progress |
| API Endpoints | 🚧 In Progress |
| Authentication | 🚧 Planned |
| Authorization (RBAC) | 🚧 Planned |
| Testing | 🚧 Planned |

---

## 👩‍💻 Author

**Deva Dharshini V**

GitHub: https://github.com/devadharshini-0707

---

## 📄 License

This project is developed for learning and enterprise IAM architecture practice.