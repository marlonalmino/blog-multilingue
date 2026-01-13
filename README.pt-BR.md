# Blog Multilíngue – Frontend (Next.js) + Backend (Django REST)

Este repositório contém uma plataforma de blog multilíngue construída com:

- Frontend: Next.js, React, TypeScript, Tailwind CSS
- Backend: Django, Django REST Framework, python-decouple, django-filter
- Banco de dados: PostgreSQL

## Imagens de Apresentação
![Prévia em Inglês](image-en.png)
![Prévia em Espanhol](image-es.png)
![Prévia em Português](image-pt.png)

## Stack
- Next.js 16, React 19, TypeScript 5, Tailwind CSS 4
- Django 5.x, Django REST Framework 3.x
- PostgreSQL 14+ com busca full‑text (tsvector)
- JWT para autenticação (access/refresh), CORS configurado para dev local

## Estrutura do Projeto
- frontend: Aplicação Next.js para a interface pública
- backend: Projeto Django expondo API REST em `/api/v1`

## Pré-requisitos
- Node.js 18+ e npm (ou pnpm/yarn)
- Python 3.10+ e pip
- PostgreSQL 14+ e CLI `psql`

## Variáveis de Ambiente

### Backend (.env)
- SECRET_KEY
- DEBUG
- DATABASE_URL
- CORS_ALLOWED_ORIGINS

Exemplo:

```
SECRET_KEY=change-me
DEBUG=True
DATABASE_URL=postgres://blog_user:blog_password@localhost:5432/blog_multilingue
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### Frontend (.env)
- NEXT_PUBLIC_API_BASE_URL

Exemplo:

```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1
```

## Criação do Banco com psql

Abra o psql e crie um usuário e banco dedicados:

```sql
-- Conecte como superusuário postgres
\c postgres

-- Crie o usuário da aplicação
CREATE USER blog_user WITH PASSWORD 'blog_password';

-- Crie o banco de dados com o usuário como proprietário
CREATE DATABASE blog_multilingue OWNER blog_user ENCODING 'UTF8';
```

Defina o `DATABASE_URL` no backend:

```
DATABASE_URL=postgres://blog_user:blog_password@localhost:5432/blog_multilingue
```

## Desenvolvimento Local

### 1) Backend
```bash
cd backend
python -m venv .venv
# PowerShell: .\.venv\Scripts\Activate.ps1
# bash (WSL/Mac/Linux): source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env    # Windows PowerShell
# cp .env.example .env    # bash

# Edite .env: defina SECRET_KEY, DATABASE_URL, DEBUG=True, CORS_ALLOWED_ORIGINS

python manage.py migrate
python manage.py seed --posts 5
python manage.py runserver 0.0.0.0:8000
```
API disponível em `http://localhost:8000/api/v1/`.

Admin padrão criado pelo seed:
- usuário: admin
- senha: admin123

### 2) Frontend
```bash
cd frontend
npm install
copy .env.example .env    # Windows PowerShell
# cp .env.example .env    # bash

# Edite .env: defina NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1
npm run dev
```
Frontend em `http://localhost:3000`.

## Observações
- O CORS por padrão permite `http://localhost:3000` para o frontend. Ajuste `CORS_ALLOWED_ORIGINS` se usar outro host/porta.
- Se o PostgreSQL não estiver instalado, instale e garanta que `psql` esteja no PATH.

