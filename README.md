# 🚀 Task Manager API

A secure Task Management REST API built with **Django REST Framework**, **JWT Authentication**, and **Role-Based Access Control (RBAC)**.

---

## ✨ Features

- 🔐 User Registration, Login & JWT Refresh
- 👥 Role-Based Access Control: Admin / User
- 📋 Task CRUD Operations
- ✅ Mark Task Complete / Incomplete
- 📚 Pagination
- 🔎 Filtering, Search & Ordering
- 🧪 Unit Tests
- ⚙️ Role Setup Management Command

---

## 🛠️ Tech Stack

- Python 3.11
- Django 5.2
- Django REST Framework
- Simple JWT
- SQLite
- Django Filter

---

## ⚙️ Setup Instructions

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

```bash
env\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run Migrations

```bash
python manage.py migrate
```

### 6. Create Roles

```bash
python manage.py setup_roles
```

### 7. Start Development Server

```bash
python manage.py runserver
```

Server runs at:

```text
http://127.0.0.1:8000/
```

🐳 Docker Setup
### Build Containers
docker compose build

### Start Containers
docker compose up

### Run Migrations
docker compose exec web python manage.py migrate

### Create Superuser
docker compose exec web python manage.py createsuperuser

### View Logs
docker compose logs -f

### Server:

http://localhost:8000

 -----

## 🔐 Authentication APIs

### Register User

```http
POST /api/auth/register/
```

Request:

```json
{
    "username": "user1",
    "email": "user1@gmail.com",
    "password": "User@123"
}
```

### Login and Get JWT Tokens

```http
POST /api/auth/login/
```

Request:

```json
{
    "username": "user1",
    "password": "User@123"
}
```

Response:

```json
{
    "refresh": "<refresh_token>",
    "access": "<access_token>"
}
```


### Refresh Access Token

```http
POST /api/auth/refresh/
```

Request:

```json
{
    "refresh": "<refresh_token>"
}
```


## 🔑 Using JWT Token

For all protected task APIs, pass the access token in headers:

```http
Authorization: Bearer <access_token>
```


## 📋 Task APIs

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/tasks/` | List tasks |
| POST | `/api/tasks/` | Create task |
| GET | `/api/tasks/<id>/` | Retrieve task |
| PUT | `/api/tasks/<id>/` | Full update task |
| PATCH | `/api/tasks/<id>/` | Partial update task |
| DELETE | `/api/tasks/<id>/` | Delete task |

---

## ➕ Create Task Example

```http
POST /api/tasks/
```

Request:

```json
{
    "title": "Learn DRF",
    "description": "Complete Task Manager API",
    "status": false,
    "due_date": "2026-06-30"
}
```


## 👥 Roles and Permissions

### 🛡️ Admin

- Can view all users' tasks
- Can create tasks
- Can update any task
- Can delete any task

### 👤 User

- Can create own tasks
- Can view only own tasks
- Can update only own tasks
- Can delete only own tasks


## ⚙️ Assign Admin Role

Create groups:

```bash
python manage.py setup_roles
```

Assign Admin role manually:

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User, Group

user = User.objects.get(username="djangoadmin")
admin_group = Group.objects.get(name="Admin")
user.groups.add(admin_group)
```

## 📚 Pagination

```http
GET /api/tasks/?page=1
```

Example response:

```json
{
    "count": 12,
    "next": "http://127.0.0.1:8000/api/tasks/?page=2",
    "previous": null,
    "results": []
}
```


## 🔎 Filtering

Filter by status:

```http
GET /api/tasks/?status=true
```

```http
GET /api/tasks/?status=false
```

Filter by owner, Admin only:

```http
GET /api/tasks/?owner=1
```


## 🔍 Search

Search tasks by title or description:

```http
GET /api/tasks/?search=django
```


## ↕️ Ordering

Order by due date:

```http
GET /api/tasks/?ordering=due_date
```

Order by newest created:

```http
GET /api/tasks/?ordering=-created_at
```


## 🧪 Run Tests

```bash
python manage.py test
```

Test coverage includes:

- Authentication APIs
- JWT login and refresh
- Task model
- Task CRUD operations
- RBAC permissions

---

## 📌 API Testing Tools

You can test this API using:

- Postman
- Thunder Client
- Insomnia
- DRF Browsable API

---

## 👨‍💻 Author

**Tharun Sathunuru**  
Aspiring Python Backend Developer

---