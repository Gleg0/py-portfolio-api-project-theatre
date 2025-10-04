# 🎭 py-portfolio-api-project-theatre

A Django REST Framework (DRF) project built as part of a portfolio.  
It provides a backend API for a theatre system: users, movies, cinema halls, and movie sessions.  
The project is containerized with Docker and follows best practices for CI/CD and code style.

---

## 📌 Features

- Custom **User model** (based on `AbstractUser`)
- **Movies**, **Cinema Halls**, and **Movie Sessions** management
- **CRUD** operations for all main entities
- **JWT authentication** for users
- **Filtering & pagination** for API endpoints
- **Permissions** (admin vs regular users)
- Database migrations with Django ORM
- **Dockerized setup** with `docker-compose`
- Code quality checks with **flake8**
- Unit tests with **pytest / Django test runner**

---

## 🛠 Tech Stack

- Python 3.12+
- Django 5.x
- Django REST Framework
- PostgreSQL
- Docker & Docker Compose
- flake8 (linting)
- pytest (testing)

---

## ⚡ Installation

Clone the repository:

```bash
git clone https://github.com/Gleg0/py-portfolio-api-project-theatre.git
cd py-portfolio-api-project-theatre
```

## 🛠 Run test:
```bash
pytest --ds=config.settings.test --cov=theatre --cov=user --cov-report=term-missing
```
