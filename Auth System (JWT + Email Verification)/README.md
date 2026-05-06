# Auth System (JWT + Email Verification)

A comprehensive authentication system built with FastAPI, featuring JWT token-based authentication with email verification and OAuth2 implementation.

## Features

- **User Registration** - New user registration with email verification
- **Email Verification** - Secure email verification flow with verification tokens
- **JWT Authentication** - Token-based authentication with access and refresh tokens
- **Password Reset** - Secure password reset flow via email
- **OAuth2 Integration** - OAuth2 with password flow support
- **Password Hashing** - Bcrypt-based secure password hashing
- **User Management** - User profile management and account settings

## Tech Stack

- **Framework**: FastAPI
- **Authentication**: JWT (PyJWT)
- **Password Hashing**: Bcrypt
- **Database**: SQLAlchemy + PostgreSQL
- **Email Service**: SMTP/SendGrid
- **Validation**: Pydantic
- **Database Migration**: Alembic

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
```

4. Run database migrations:
```bash
alembic upgrade head
```

5. Start the application:
```bash
uvicorn main:app --reload
```

## API Endpoints

### Registration & Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/verify-email` - Verify email address
- `POST /api/auth/login` - Login user (returns JWT tokens)
- `POST /api/auth/refresh` - Refresh access token
- `POST /api/auth/logout` - Logout user

### Password Management
- `POST /api/auth/forgot-password` - Request password reset
- `POST /api/auth/reset-password` - Reset password with token

### User Profile
- `GET /api/users/me` - Get current user profile
- `PUT /api/users/me` - Update user profile
- `DELETE /api/users/me` - Delete user account

## Environment Variables

```
DATABASE_URL=postgresql://user:password@localhost/auth_db
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
REFRESH_TOKEN_EXPIRATION_DAYS=7
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SENDER_EMAIL=noreply@example.com
```

## Database Schema

- **users** - User account information
- **email_verification_tokens** - Email verification tokens
- **password_reset_tokens** - Password reset tokens
- **refresh_tokens** - Refresh token storage (optional)

## Running Tests

```bash
pytest tests/ -v
```

## Project Structure

```
├── main.py
├── config.py
├── requirements.txt
├── models/
│   └── user.py
├── schemas/
│   ├── user.py
│   └── token.py
├── routes/
│   └── auth.py
├── services/
│   ├── auth_service.py
│   ├── email_service.py
│   └── token_service.py
├── utils/
│   ├── security.py
│   └── validators.py
├── database/
│   └── database.py
├── tests/
│   └── test_auth.py
└── alembic/
    └── versions/
```

## Security Considerations

- Passwords are hashed using bcrypt with salt
- JWT tokens use HS256 algorithm
- Email verification prevents spam registrations
- HTTPS should be enforced in production
- CORS should be configured appropriately
- Rate limiting recommended on auth endpoints

## Contributing

Follow the FastAPI best practices and ensure all tests pass before submitting PRs.
