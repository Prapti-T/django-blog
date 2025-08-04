# Django Blog API

A backend API for a blogging platform, built using Django REST Framework. It supports JWT authentication, post creation, categorization, and commenting functionalities — all secured and RESTful.

---

## Features

- User Registration & Login (JWT-based)
- Create, Read, Update, Delete (CRUD) for:
  - Blog Posts
  - Categories
  - Comments
- Authentication Required for : Creating Categories, Creating/Editing/Deleting Posts or Comments
- Author Permissions : Only authors can update/delete their own content
- PostgreSQL Database

---

## API Authentication

Use /signup to register.

Use /login to get a token.

Include the token in Authorization header for protected routes:

```
Authorization: Bearer <your_token>
```

---

## API Endpoints

### Authentication

| Endpoint     | Method | Description       |
| ------------ | ------ | ----------------- |
| `/register/` | POST   | Create a new user |
| `/login/`    | POST   | Get JWT tokens    |

---

### Posts

| Endpoint                  | Method | Auth | Description               |
| ------------------------- | ------ | ---- | ------------------------- |
| `/posts/`                 | GET    | NO   | List all posts            |
| `/posts/create/`          | POST   | Yes  | Create new post           |
| `/posts/<int:pk>/`        | GET    | NO   | Get post detail           |
| `/posts/<int:pk>/update/` | PUT    | Yes  | Update post (author only) |
| `/posts/<int:pk>/delete/` | DELETE | Yes  | Delete post (author only) |
| `/posts/<str:category>/`  | GET    | NO   | List posts by category    |

---

### Categories

| Endpoint            | Method | Auth | Description         |
| ------------------- | ------ | ---- | ------------------- |
| `/category/`        | GET    | NO   | List all categories |
| `/category/create/` | POST   | Yes  | Create new category |

---

### Comments

| Endpoint                                 | Method | Auth | Description                  |
| ---------------------------------------- | ------ | ---- | ---------------------------- |
| `/posts/<post_pk>/comments/`             | GET    | NO   | List all comments on a post  |
| `/posts/<post_pk>/comments/create/`      | POST   | Yes  | Add a comment                |
| `/posts/<post_pk>/comments/<pk>/update/` | PUT    | Yes  | Update comment (author only) |
| `/posts/<post_pk>/comments/<pk>/delete/` | DELETE | Yes  | Delete comment (author only) |
| `/posts/<post_pk>/comments/<pk>/`        | GET    | NO   | Get a specific comment       |

---

## 🛠️ Setup Instructions

1. Clone the Repository

```bash
git clone https://github.com/your-username/d
```

2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

3. Install Requirements

```bash
pip install -r requirements.txt
```

4. Configure PostgreSQL in settings.py

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

6. Run Server

```bash
python manage.py runserver
```
