# Multilingual Blog – Frontend (Next.js) + Backend (Django REST)

This repository contains a multilingual blog platform built with:

- Frontend: Next.js, React, TypeScript, Tailwind CSS
- Backend: Django, Django REST Framework, python-decouple, django-filter
- Database: PostgreSQL

## Project Preview
### English UI
![English Preview](image-en.png)

### Spanish UI
![Spanish Preview](image-es.png)

### Portuguese UI
![Portuguese Preview](image-pt.png)

## Stack
- Next.js 16, React 19, TypeScript 5, Tailwind CSS 4
- Django 5.x, Django REST Framework 3.x
- PostgreSQL 14+ with full‑text search (tsvector)
- JWT for authentication (access/refresh), CORS configured for local dev

## Project Structure
- frontend: Next.js app for the public UI
- backend: Django project exposing REST API under `/api/v1`

## Prerequisites
- Node.js 18+ and npm (or pnpm/yarn)
- Python 3.10+ and pip
- PostgreSQL 14+ and `psql` CLI

## Environment Variables

### Backend (.env)
- SECRET_KEY
- DEBUG
- DATABASE_URL
- CORS_ALLOWED_ORIGINS

Example:

```
SECRET_KEY=change-me
DEBUG=True
DATABASE_URL=postgres://blog_user:blog_password@localhost:5432/blog_multilingue
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### Frontend (.env)
- NEXT_PUBLIC_API_BASE_URL

Example:

```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1
```

## Database Setup with psql

Open psql and create a dedicated user and database:

```sql
-- Connect as the postgres superuser
\c postgres

-- Create app user
CREATE USER blog_user WITH PASSWORD 'blog_password';

-- Create database owned by the app user
CREATE DATABASE blog_multilingue OWNER blog_user ENCODING 'UTF8';
```

Set the backend `DATABASE_URL` accordingly:

```
DATABASE_URL=postgres://blog_user:blog_password@localhost:5432/blog_multilingue
```

## Local Development

### 1) Backend
```bash
cd backend
python -m venv .venv
# PowerShell: .\.venv\Scripts\Activate.ps1
# bash (WSL/Mac/Linux): source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env    # Windows PowerShell
# cp .env.example .env    # bash

# Edit .env: set SECRET_KEY, DATABASE_URL, DEBUG=True, CORS_ALLOWED_ORIGINS

python manage.py migrate
python manage.py seed --posts 5
python manage.py runserver 0.0.0.0:8000
```
API is available at `http://localhost:8000/api/v1/`.

Default admin created by seed:
- username: admin
- password: admin123

### 2) Frontend
```bash
cd frontend
npm install
copy .env.example .env    # Windows PowerShell
# cp .env.example .env    # bash

# Edit .env: set NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1
npm run dev
```
Frontend runs at `http://localhost:3000`.

## Notes
- CORS defaults allow `http://localhost:3000` for the frontend. Adjust `CORS_ALLOWED_ORIGINS` if you use a different host/port.
- If PostgreSQL is not installed, install it and ensure `psql` is in your PATH.

