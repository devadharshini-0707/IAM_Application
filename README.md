# Enterprise IAM Application

A production-style **Identity and Access Management (IAM)** application built using **FastAPI**, **React**, **TypeScript**, and **PostgreSQL** following **Clean Architecture**, **Repository Pattern**, and enterprise software engineering practices.

This project is being developed as an enterprise-grade IAM platform similar to **Okta**, **Keycloak**, **Azure AD**, and **AWS IAM**.

---

# Features

## Authentication

- User Signup
- User Login
- JWT Authentication
- Password Hashing (bcrypt)
- Protected API Endpoints
- Secure Credential Storage

---

## User Management

- Create User
- View Users
- Search Users
- Edit User
- Enable User
- Disable User
- Soft Delete User
- Pagination
- Current Logged-in User API

---

## Database

Implemented using PostgreSQL.

Current entities include:

- Organization
- Identity
- User
- Credential

Relationships are maintained using foreign keys following enterprise IAM design principles.

---

# Technology Stack

## Backend

- FastAPI
- Python 3
- SQLAlchemy ORM
- Alembic
- PostgreSQL
- JWT Authentication
- bcrypt Password Hashing

---

## Frontend

- React
- TypeScript
- Axios
- React Router

---

## Database

- PostgreSQL
- pgAdmin 4

---

# Project Architecture

```
Client (React)

        │

        ▼

FastAPI Routes

        │

        ▼

Service Layer

        │

        ▼

Repository Layer

        │

        ▼

SQLAlchemy ORM

        │

        ▼

PostgreSQL
```

The project follows:

- Clean Architecture
- Repository Pattern
- Dependency Injection
- Separation of Concerns
- Layered Architecture

---

# Project Structure

```
app/
│
├── config/
├── dependencies/
├── models/
├── repositories/
├── routes/
├── schemas/
├── services/
├── utils/
└── main.py

frontend/
│
├── src/
│   ├── pages/
│   ├── services/
│   ├── components/
│   └── App.tsx
```

---

# Current Progress

| Module | Status |
|---------|--------|
| Project Setup | ✅ Completed |
| PostgreSQL Integration | ✅ Completed |
| Authentication | ✅ Completed |
| JWT Authentication | ✅ Completed |
| Password Hashing | ✅ Completed |
| User Management | ✅ Completed |
| Search | ✅ Completed |
| Edit User | ✅ Completed |
| Enable / Disable User | ✅ Completed |
| Soft Delete | ✅ Completed |
| Pagination | ✅ Completed |
| Frontend Integration | ✅ Completed |

---

# Upcoming Modules

- User Details
- Organization Management
- Role Management
- Permission Management
- Group Management
- User Role Assignment
- User Group Assignment
- Role Based Access Control (RBAC)
- Audit Logs
- Multi-Factor Authentication (MFA)
- Password Policies
- Session Management

---

# Installation

## Clone Repository

```bash
git clone https://github.com/devadharshini-0707/IAM_Application.git

cd IAM_Application
```

---

## Create Virtual Environment

```bash
python -m venv .venv
```

Activate:

### Windows

```bash
.venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment

Create a `.env` file and configure:

```
DATABASE_URL=postgresql://...
SECRET_KEY=your_secret_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

## Run Database Migrations

```bash
alembic upgrade head
```

---

## Start Backend

```bash
uvicorn app.main:app --reload
```

Backend:

```
http://127.0.0.1:8000
```

Swagger:

```
http://127.0.0.1:8000/docs
```

---

## Start Frontend

```bash
npm install

npm run dev
```

---

# API Overview

## Authentication

```
POST /auth/signup

POST /auth/login
```

---

## Users

```
POST   /users/

GET    /users/

GET    /users/{id}

PUT    /users/{id}

PUT    /users/{id}/enable

PUT    /users/{id}/disable

DELETE /users/{id}

GET    /users/search

GET    /users/me
```

---

# Engineering Principles

This project follows:

- Clean Architecture
- SOLID Principles
- Repository Pattern
- Dependency Injection
- Strong Typing
- Layered Design
- Enterprise Coding Standards
- RESTful API Design

---

# Repository

GitHub Repository

https://github.com/devadharshini-0707/IAM_Application

---

# Project Status

**Current Version:** v0.1

Completed:

- Authentication Module
- User Management Module

Currently Working On:

- User Module Enhancements

Next Milestone:

- Role Management
- Permission Management
- Group Management

---

# Author

**Deva Dharshini**

Enterprise Identity and Access Management (IAM) Application using FastAPI, React, and PostgreSQL.