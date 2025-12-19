<p align="center">
  <img src="docs/images/screenshot.png" alt="IntegrateX admin screenshot" width="auto">
</p>

---

# IntegrateX

IntegrateX is a **production-grade Django backend system** designed to demonstrate advanced Python & Django expertise, real-world backend architecture, and complex third-party API integrations.

The project follows patterns commonly used in **scalable, multi-tenant backend platforms**, with a strong focus on security, maintainability, and deployment readiness.

---

## Key Features

### ✔ Authentication & Authorization
- JWT-based authentication (access & refresh tokens)
- Role-based access control:
  - Admin
  - Manager
  - User
- Permission enforcement at API and service layers
- Secure password handling and token expiration

### ✔ Multi-Tenant Architecture
- Organization-based data isolation
- Users can belong to one or more organizations
- Organization-scoped queries to prevent data leakage
- Organization-level API key support

### ✔ REST API (Django REST Framework)
- Versioned API (`/api/v1/`)
- Pagination, filtering, and searching
- Consistent response and error formats
- OpenAPI / Swagger documentation

### ✔ Third-Party Integrations
- Payment gateway integration (Stripe-style workflow)
- Notification services (email / SMS)
- Secure webhook ingestion with signature verification
- Idempotent webhook processing and event replay support

### ✔ Background Processing
- Celery with Redis as message broker
- Background jobs for:
  - Webhook processing
  - Notification delivery
  - External API synchronization
- Retry logic with exponential backoff

### ✔ Audit Logging & Observability
- User action and request tracking
- Persistent audit logs
- Change history with timestamps
- Designed for compliance and debugging

### ✔ Security Best Practices
- CSRF and CORS protection
- API rate limiting
- Input validation and sanitization
- Secure secret and environment handling

### ✔ Deployment Readiness
- Gunicorn-compatible WSGI setup
- Dockerized application stack
- PostgreSQL-ready configuration
- Automated migration and static file handling
- Celery worker and beat services

---

## Tech Stack

- Python 3.10+
- Django
- Django REST Framework
- PostgreSQL
- Celery + Redis
- JWT Authentication
- Docker & Docker Compose
- Gunicorn

---

## Project Structure (High-Level)

```
IntegrateX/
│
├── apps/                  # Django apps (users, organizations, integrations, etc.)
├── config/                # Project settings, URLs, WSGI, Celery config
├── docker/                # Dockerfile, docker-compose, entrypoint
├── docs/
│   └── images/            # README screenshots and documentation assets
├── staticfiles/           # Collected static files (Docker / production)
├── manage.py
├── requirements.txt
├── .env.example
└── README.md
```

---

## Local Development (Without Docker)

### 1. Clone the repository
```bash
git clone https://github.com/damir-bubanovic/IntegrateX.git
cd IntegrateX
```

### 2. Create and activate a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
cp .env.example .env
```

### 5. Run migrations
```bash
python manage.py migrate
```

### 6. Start the development server
```bash
python manage.py runserver
```

---

## Running with Docker (Recommended)

### 1. Build and start the stack
```bash
cd docker
docker compose up --build
```

Services started:
- Django (Gunicorn)
- PostgreSQL
- Redis
- Celery worker
- Celery beat

### 2. Create an admin user
```bash
docker compose exec web python manage.py createsuperuser
```

### 3. Access the admin interface
```
http://127.0.0.1:8000/admin/
```

---

## Purpose of This Project

IntegrateX is a **portfolio and demonstration project** created to showcase:

- Senior-level Django architecture
- Multi-tenant backend design
- Real-world third-party API integration patterns
- Secure webhook processing
- Asynchronous task orchestration
- Production-ready deployment workflows

This project is intentionally backend-focused and does not include a frontend UI.

---

## Author

**Damir Bubanović**

- Website: https://damirbubanovic.com  
- GitHub: https://github.com/damir-bubanovic  
- YouTube: https://www.youtube.com/@damirbubanovic6608  

---

## License

MIT License
