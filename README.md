# 🚀 Task Manager API

A secure Task Management REST API built with Django REST Framework, JWT Authentication, and Role-Based Access Control (RBAC).

## ✨ Features

- 🔐 JWT Authentication (Register, Login, Refresh)
- 👥 Role-Based Access Control (Admin/User)
- 📋 Complete Task CRUD Operations
- 🔎 Search, Filtering & Ordering
- 📚 Pagination Support
- 🧪 Unit Testing
- ⚡ RESTful API Architecture

## 🛠️ Tech Stack

- Python 3.11
- Django 5.2
- Django REST Framework
- Simple JWT
- SQLite
- Django Filter

## 🚀 Quick Start

```bash
git clone https://github.com/Tharun-301/Task_Manager_API.git
cd Task_Manager_API

python -m venv env
env\Scripts\activate

pip install -r requirements.txt

python manage.py migrate
python manage.py setup_roles
python manage.py runserver
```

## 🔑 Authentication

```http
POST /api/auth/register/
POST /api/auth/login/
POST /api/auth/refresh/
```

## 📋 Task APIs

```http
GET    /api/tasks/
POST   /api/tasks/
GET    /api/tasks/<id>/
PATCH  /api/tasks/<id>/
DELETE /api/tasks/<id>/
```

## 🏆 Highlights

✅ JWT Authentication  
✅ RBAC (Admin/User)  
✅ Task CRUD Operations  
✅ Search & Filtering  
✅ Pagination  
✅ Unit Tests  

## 👨‍💻 Author

**Tharun Sathunuru**  
Aspiring Python Backend Developer