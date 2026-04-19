# Lab 3 - JWT Authentication

This lab implements a JWT-based authentication system using Flask and PostgreSQL, containerized with Docker.

Users can register, log in, access protected routes, and refresh their access tokens. Role-based access control is demonstrated through a student/teacher/admin role field stored in the database.

## Architecture

| Component | Technology |
|---|---|
| Web framework | Flask |
| Database | PostgreSQL 16 |
| Auth mechanism | JWT (flask-jwt-extended) |
| Password hashing | bcrypt |
| Runtime | Docker + Docker Compose |

## API Endpoints

| Method | Path | Auth required | Description |
|---|---|---|---|
| GET | `/` | No | Login page |
| GET | `/register` | No | Register page |
| GET | `/dashboard` | No | Dashboard page |
| POST | `/api/register` | No | Create a new user account |
| POST | `/api/login` | No | Authenticate and receive tokens |
| GET | `/api/me` | Access token | Get the current user's profile |
| GET | `/api/admin` | Access token (admin role) | Admin-only endpoint |
| POST | `/api/refresh` | Refresh token | Issue a new access token |
| POST | `/api/logout` | Access token | Log out |

## How to Start

1. Copy the environment file and fill in your values:

   ```bash
   cp .env.example .env
   ```

2. Start the containers:

   ```bash
   docker-compose up -d --build
   ```

3. Open your browser and navigate to **http://localhost:5000**

## How to Stop

```bash
docker-compose down
```

To also delete the database volume:

```bash
docker-compose down -v
```
