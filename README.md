# 🚀 Task Manager API

A secure and role-based **Task Management REST API** built with **Django REST Framework**, **JWT Authentication**, and **Role-Based Access Control (RBAC)**.

This project allows users to register, log in using JWT tokens, and manage personal tasks. Admin users can manage all tasks, while normal users can only manage their own tasks.

---

## ✨ Key Features

* 🔐 JWT Authentication (Register, Login, Refresh)
* 👥 Role-Based Access Control (Admin/User)
* 📋 Task CRUD Operations
* ✅ Task Status Management
* 📅 Due Date Support
* 📚 Pagination, Filtering, Search & Ordering
* 🧪 Unit Testing
* 🐳 Docker Support
* ⚙️ Automated Role Setup Command

---

## 🛠️ Tech Stack

* Python 3.11
* Django 5.2
* Django REST Framework
* Simple JWT
* SQLite
* Django Filter
* Docker
* Docker Compose

---

## ⚙️ Local Setup Instructions

### 1. Clone Repository

```bash
git clone https://github.com/Tharun-301/Task_Manager_API.git
cd Task_Manager_API
```

### 2. Create Virtual Environment

```bash
python -m venv env
```

### 3. Activate Virtual Environment

Windows:

```bash
env\Scripts\activate
```

Linux / Mac:

```bash
source env/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run Migrations

```bash
python manage.py migrate
```

### 6. Create Default Roles

```bash
python manage.py setup_roles
```

This command creates the required user roles:

```text
Admin
User
```

### 7. Start Development Server

```bash
python manage.py runserver
```

Server runs at:

```text
http://127.0.0.1:8000/
```

---

# 🐳 Docker Setup

This project includes Docker support for running the application in a consistent environment.

### 1. Build Docker Image

```bash
docker compose build
```

### 2. Start Container

```bash
docker compose up
```

Server runs at:

```text
http://localhost:8000/
```

### 3. Run Migrations Inside Docker

```bash
docker compose exec web python manage.py migrate
```

### 4. Create Roles Inside Docker

```bash
docker compose exec web python manage.py setup_roles
```

### 5. Create Superuser Inside Docker

```bash
docker compose exec web python manage.py createsuperuser
```

### 6. Run Tests Inside Docker

```bash
docker compose exec web python manage.py test
```

### 7. View Docker Logs

```bash
docker compose logs -f
```

### 8. Stop Containers

```bash
docker compose down
```

---

# 🔐 Authentication APIs

## 1. Register User

```http
POST /api/auth/register/
```

### Request Body

```json
{
  "username": "user1",
  "email": "user1@gmail.com",
  "password": "User@123"
}
```

### Success Response

```json
{
  "id": 1,
  "username": "user1",
  "email": "user1@gmail.com"
}
```

---

## 2. Login User

```http
POST /api/auth/login/
```

### Request Body

```json
{
  "username": "user1",
  "password": "User@123"
}
```

### Success Response

```json
{
  "refresh": "your_refresh_token",
  "access": "your_access_token"
}
```

The `access` token is used to access protected APIs.
The `refresh` token is used to generate a new access token.

---

## 3. Refresh Access Token

```http
POST /api/auth/refresh/
```

### Request Body

```json
{
  "refresh": "your_refresh_token"
}
```

### Success Response

```json
{
  "access": "new_access_token"
}
```

---

# 🔑 JWT Usage

All task APIs are protected. Send the access token in the request header:

```http
Authorization: Bearer your_access_token
```

Example:

```bash
curl -X GET http://localhost:8000/api/tasks/ \
-H "Authorization: Bearer your_access_token"
```

## ➕ Create Task

```http
POST /api/tasks/
```

### Request Body

```json
{
  "title": "Learn Django REST Framework",
  "description": "Build and test Task Manager API",
  "status": false,
  "due_date": "2026-06-30"
}
```

### Success Response

```json
{
  "id": 1,
  "title": "Learn Django REST Framework",
  "description": "Build and test Task Manager API",
  "status": false,
  "due_date": "2026-06-30",
  "owner": 1,
  "created_at": "2026-06-11T12:00:00Z",
  "updated_at": "2026-06-11T12:00:00Z"
}
```

---

## 📖 List Tasks

```http
GET /api/tasks/
```

### Behavior

* Admin users can view all users' tasks.
* Normal users can view only their own tasks.

---

## ✏️ Update Task

```http
PATCH /api/tasks/1/
```

### Request Body

```json
{
  "status": true
}
```

This can be used to mark a task as complete.

---

## ❌ Delete Task

```http
DELETE /api/tasks/1/
```

### Success Response

```text
204 No Content
```

---

# 👥 Roles and Permissions

## 🛡️ Admin Role

Admin users can:

* View all users' tasks
* Create tasks
* Update any task
* Delete any task
* Filter tasks by owner

## 👤 User Role

Normal users can:

* Create their own tasks
* View only their own tasks
* Update only their own tasks
* Delete only their own tasks

Users cannot access or modify tasks created by other users.

---

# ⚙️ Assign Admin Role

### 1. Run Role Setup Command

```bash
python manage.py setup_roles
```

For Docker:

```bash
docker compose exec web python manage.py setup_roles
```

### 2. Open Django Shell

```bash
python manage.py shell
```

For Docker:

```bash
docker compose exec web python manage.py shell
```

### 3. Assign Admin Group

```python
from django.contrib.auth.models import User, Group

user = User.objects.get(username="djangoadmin")
admin_group = Group.objects.get(name="Admin")
user.groups.add(admin_group)
```

---

# 📚 Pagination

```http
GET /api/tasks/?page=1
```

### Example Response

```json
{
  "count": 12,
  "next": "http://localhost:8000/api/tasks/?page=2",
  "previous": null,
  "results": []
}
```

---

# 🔎 Filtering

## Filter Completed Tasks

```http
GET /api/tasks/?status=true
```

## Filter Incomplete Tasks

```http
GET /api/tasks/?status=false
```

## Filter by Owner

Admin only:

```http
GET /api/tasks/?owner=1
```

Normal users should not use owner filtering to access other users' tasks.

---

# 🔍 Search

Search tasks by title or description:

```http
GET /api/tasks/?search=django
```

Example:

```http
GET /api/tasks/?search=api
```

---

# ↕️ Ordering

## Order by Due Date

```http
GET /api/tasks/?ordering=due_date
```

## Order by Latest Created

```http
GET /api/tasks/?ordering=-created_at
```

## Order by Oldest Created

```http
GET /api/tasks/?ordering=created_at
```
---

# 🧪 Running Tests

## Local Test Command

```bash
python manage.py test
```

## Docker Test Command

```bash
docker compose exec web python manage.py test
```

# 📌 API Testing Tools

You can test the API using:

* Postman
* Thunder Client
* Insomnia
* DRF Browsable API
* PowerShell Invoke-RestMethod

---

# ✅ Final Verification

Before submitting, verify:

```bash
python manage.py check
python manage.py test
```

For Docker:

```bash
docker compose exec web python manage.py check
docker compose exec web python manage.py test
```

Expected result:

```text
System check identified no issues
Ran all tests successfully
OK
```

---

# 📦 Submission

GitHub Repository:

```text
https://github.com/Tharun-301/Task_Manager_API
```

---

# 👨‍💻 Author

**Tharun Sathunuru**
Aspiring Python Backend Developer
