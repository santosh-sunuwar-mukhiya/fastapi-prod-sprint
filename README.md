# FastAPI Backend Mastery

A comprehensive backend development learning project demonstrating production-grade FastAPI applications with enterprise-level patterns, security implementations, and scalability practices.

## 🎯 Learning Objectives

This project explores core backend engineering concepts through hands-on mini-projects:

- **JWT Authentication** - Real-world token-based authentication with refresh tokens, token expiration, and revocation strategies
- **OAuth2 Flow** - Industry-standard authorization protocol implementation for third-party authentication
- **Backend Security Basics** - Secure password hashing (bcrypt), role-based access control (RBAC), SQL injection prevention, and request validation
- **Redis in Production** - Rate limiting, token blacklist management, and distributed caching patterns
- **Async Task Systems** - Celery background job processing for email delivery and long-running operations
- **API Design** - RESTful principles, request/response schemas with Pydantic, pagination, error handling, and API versioning
- **Project Structure** - Scalable application architecture with separation of concerns and modularity

## 📦 Project Structure

```
app/
│
├── main.py                          # Application entry point, FastAPI setup
├── core/
│   ├── config.py                    # Environment variables, settings management
│   ├── security.py                  # Authentication, JWT token generation/validation
│
├── db/
│   ├── session.py                   # Database connection, SQLAlchemy setup
│   ├── models.py                    # ORM models (User, Blog, Token models)
│
├── schemas/
│   ├── user.py                      # Pydantic models for request/response validation
│
├── api/
│   ├── deps.py                      # Dependency injection (current user, permissions)
│   ├── routes/
│   │   ├── auth.py                  # Login, registration, token refresh endpoints
│   │   ├── users.py                 # User CRUD operations
│
└── utils/
    ├── email.py                     # Email service, Celery tasks
```

## 🚀 Mini-Projects

### 1️⃣ Auth System (JWT + Email Verification)
- User registration with email verification
- JWT token-based authentication (access + refresh tokens)
- Password reset flow with secure tokens
- OAuth2 password grant flow implementation

**Key Files**: `Auth System (JWT + Email Verification)/`

### 2️⃣ Blog System (CRUD + Pagination)
- RESTful CRUD operations for blog posts
- Cursor-based and offset pagination
- Author authorization (only authors can edit/delete)
- Rich content filtering and sorting

**Key Files**: `Blog System(CRUD + PAGINATION)/`

### 3️⃣ Celery (Email System + Background Tasks)
- Asynchronous email delivery with Celery
- Task retry logic with exponential backoff
- Email templates for verification and notifications
- Background job monitoring

**Key Files**: `Celery (Email System + Background Tasks)/`

### 4️⃣ Redis (Rate Limiting + Token Blacklist)
- Token rate limiting per endpoint
- Token blacklist for logout operations
- Distributed cache for session management
- Redis clustering for high availability

**Key Files**: `Redis (Rate Limit + Token Blacklist)/`

## 🛠 Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Framework** | FastAPI | Modern async web framework |
| **Database** | SQLAlchemy + PostgreSQL | ORM and relational database |
| **Authentication** | JWT + OAuth2 | Token-based security |
| **Background Tasks** | Celery + Redis | Async job processing |
| **Caching** | Redis | Rate limiting, token blacklist |
| **Validation** | Pydantic | Data serialization & validation |
| **Password Hashing** | Bcrypt | Secure credential storage |

## ⚙️ Installation & Setup

### Prerequisites
```bash
Python 3.9+
PostgreSQL 12+
Redis 6+
Celery 5+
```

### Setup

```bash
# 1. Clone and navigate
git clone <repository>
cd FastAPI

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Environment configuration
cp .env.example .env
# Edit .env with your database, JWT, email settings

# 5. Database migrations
alembic upgrade head

# 6. Run application
uvicorn app.main:app --reload

# 7. Start Celery worker (in separate terminal)
celery -A app.utils.email worker --loglevel=info

# 8. Start Redis
redis-server
```

## 🔐 Security Architecture

### Authentication Flow
```
Client Request
    ↓
Credentials Validation (Bcrypt)
    ↓
JWT Token Generation (HS256)
    ↓
Access Token (short-lived: 15min)
Refresh Token (long-lived: 7 days)
    ↓
Token Stored in Redis (blacklist tracking)
```

### Key Security Measures
- **Password Storage**: Bcrypt hashing with salt rounds
- **Token Expiration**: Short-lived access tokens, refresh token rotation
- **CORS Configuration**: Whitelisted domains only
- **Input Validation**: Pydantic schema validation, SQL injection prevention
- **Rate Limiting**: Redis-backed endpoint throttling
- **HTTPS Enforcement**: TLS in production

## 📚 API Endpoints Overview

### Authentication Routes
```
POST   /api/v1/auth/register          - User registration
POST   /api/v1/auth/login             - Email/password login
POST   /api/v1/auth/refresh           - Refresh access token
POST   /api/v1/auth/logout            - Invalidate token
POST   /api/v1/auth/verify-email      - Email verification
POST   /api/v1/auth/forgot-password   - Password reset request
```

### User Routes
```
GET    /api/v1/users/me               - Get current user profile
GET    /api/v1/users/{user_id}        - Get user details
PUT    /api/v1/users/{user_id}        - Update profile
DELETE /api/v1/users/{user_id}        - Delete account
```

### Blog Routes (CRUD + Pagination)
```
GET    /api/v1/blogs?page=1&limit=10  - List blogs with pagination
POST   /api/v1/blogs                  - Create blog post
GET    /api/v1/blogs/{blog_id}        - Get blog details
PUT    /api/v1/blogs/{blog_id}        - Update blog
DELETE /api/v1/blogs/{blog_id}        - Delete blog
```

## 🏗 Architecture Decisions

### Dependency Injection Pattern
```python
# deps.py - Reusable dependencies
async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    # Validate token, fetch user from DB
    pass

# routes/users.py - Usage
@router.get("/me")
async def get_profile(current_user: User = Depends(get_current_user)):
    return current_user
```

### Async/Await Best Practices
- Database queries are non-blocking with SQLAlchemy async driver
- Email sending offloaded to Celery workers
- I/O operations use `async` context managers

### Database Session Management
- SQLAlchemy sessionmaker configured for connection pooling
- Transaction rollback on exceptions
- Proper resource cleanup with dependency lifetimes

## 📊 Scalability Patterns

### Horizontal Scaling
- **Stateless API Servers**: No session data stored locally
- **Distributed Cache**: Redis for shared state across instances
- **Task Queue**: Celery for background job distribution

### Rate Limiting Strategy
```
User: 100 requests/hour (per IP)
Endpoint: 1000 requests/hour (global)
Stored in Redis with key expiration
```

### Token Blacklist Implementation
```
On Logout:
  - Add token to Redis blacklist with TTL = token expiration time
  - Check blacklist on every authenticated request
  - Automatic cleanup via Redis expiration
```

## 🧪 Testing (Recommended Structure)

```
tests/
├── unit/
│   ├── test_security.py              # JWT, OAuth2 logic
│   ├── test_schemas.py               # Pydantic validation
├── integration/
│   ├── test_auth_flow.py             # Full auth flow
│   ├── test_blog_crud.py             # Blog endpoints
├── conftest.py                        # Pytest fixtures
```

## 🚀 Deployment Considerations

### Production Checklist
- [ ] Environment secrets in secure vault (AWS Secrets Manager, HashiCorp Vault)
- [ ] HTTPS/TLS enabled
- [ ] Database backups scheduled
- [ ] Redis persistence and replication
- [ ] Celery worker auto-restart configuration
- [ ] Application monitoring (Sentry, New Relic)
- [ ] API rate limiting configured
- [ ] CORS properly restricted
- [ ] SQL query optimization and indexing
- [ ] Docker containerization

### Recommended Stack
```
Deployment: Docker + Kubernetes
Load Balancer: Nginx / AWS ALB
Application Server: Uvicorn (with Gunicorn)
Database: PostgreSQL with read replicas
Cache: Redis Cluster
Task Queue: Celery with RabbitMQ/Redis
Monitoring: Prometheus + Grafana
```

## 📖 Key Concepts Reference

| Concept | What | Why | Where |
|---------|------|-----|-------|
| **JWT** | Self-contained tokens | Stateless auth, scalable | `core/security.py` |
| **Refresh Tokens** | Long-lived credentials | Extend sessions securely | `routes/auth.py` |
| **OAuth2** | Authorization protocol | Third-party authentication | `core/security.py` |
| **Password Hashing** | Bcrypt+Salt | Cannot reverse-engineer | `core/security.py` |
| **Rate Limiting** | Request throttling | DDoS protection | `Redis` project |
| **Token Blacklist** | Invalidated token list | Logout security | `Redis` project |
| **Pagination** | Cursor/offset based | Efficient data retrieval | `routes/blogs.py` |
| **Celery Tasks** | Async jobs | Non-blocking operations | `utils/email.py` |

## 📝 Typical Request/Response Example

### Register User
```bash
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "full_name": "John Doe"
}

Response (201):
{
  "user_id": "uuid-xxx",
  "email": "user@example.com",
  "message": "Verification email sent"
}
```

### Login & Get Token
```bash
POST /api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=SecurePass123!

Response (200):
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "token_type": "bearer",
  "expires_in": 900
}
```

## 🎓 Learning Path

1. **Phase 1**: Auth System fundamentals (JWT, OAuth2, password hashing)
2. **Phase 2**: Database design and CRUD operations with pagination
3. **Phase 3**: Async patterns and Celery background tasks
4. **Phase 4**: Production concerns (caching, rate limiting, token management)
5. **Phase 5**: Deployment and monitoring

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8949)
- [OAuth2 Specification](https://tools.ietf.org/html/rfc6749)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [Celery Documentation](https://docs.celeryproject.io/)
- [Redis Patterns](https://redis.io/patterns/)

## 📄 License

MIT License - Educational purposes

---

**Last Updated**: May 2026 | **Status**: Learning Project | **Difficulty**: Intermediate to Advanced
