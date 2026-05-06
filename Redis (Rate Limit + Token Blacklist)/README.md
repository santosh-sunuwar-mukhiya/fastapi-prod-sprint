# Redis (Rate Limit + Token Blacklist)

A caching and rate limiting solution built with FastAPI and Redis for managing token blacklists and implementing distributed rate limiting.

## Features

- **Token Blacklist** - Blacklist JWT tokens on logout with TTL
- **Rate Limiting** - Sliding window rate limiting per user/IP
- **Distributed Cache** - Redis-based distributed caching
- **Session Management** - User session tracking and management
- **Token Expiry** - Automatic token expiry with Redis TTL
- **Throttling** - API endpoint throttling
- **Cache Invalidation** - Smart cache invalidation strategies
- **Redis Clustering** - Support for Redis Sentinel and cluster mode

## Tech Stack

- **Framework**: FastAPI
- **Cache/Queue**: Redis
- **Authentication**: JWT
- **Rate Limiting**: slowapi (Redis backend)
- **Database**: SQLAlchemy + PostgreSQL
- **Validation**: Pydantic

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

4. Start Redis:
```bash
redis-server
```

5. Start the application:
```bash
uvicorn main:app --reload
```

## API Endpoints

### Token Management
- `POST /api/tokens/blacklist` - Blacklist a token on logout
- `GET /api/tokens/is-blacklisted/{token}` - Check if token is blacklisted
- `GET /api/tokens/stats` - Token statistics

### Rate Limiting
- `GET /api/rate-limit/status` - Check current rate limit status
- `POST /api/rate-limit/reset` - Reset rate limit for user

### Cache Management
- `POST /api/cache/set` - Set cache value
- `GET /api/cache/{key}` - Get cache value
- `DELETE /api/cache/{key}` - Delete cache value
- `POST /api/cache/invalidate` - Invalidate cache patterns

### Session Management
- `GET /api/sessions` - List user sessions
- `DELETE /api/sessions/{session_id}` - Revoke session
- `POST /api/sessions/invalidate-all` - Invalidate all sessions

## Environment Variables

```
REDIS_URL=redis://localhost:6379
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_PERIOD=3600
TOKEN_BLACKLIST_TTL=86400
SESSION_TIMEOUT=3600
CACHE_TTL=300
REDIS_POOL_SIZE=10
REDIS_CONNECTION_TIMEOUT=5
```

## Rate Limiting Configuration

### Default Rate Limits
- **API Endpoints**: 100 requests per hour per IP
- **Auth Endpoints**: 5 requests per minute per IP
- **Search Endpoints**: 30 requests per minute per user

### Implementation
```python
@app.get("/api/data")
@limiter.limit("100/hour")
async def get_data(request: Request):
    return {"data": "example"}
```

## Token Blacklist

### On Logout
```python
@app.post("/api/auth/logout")
async def logout(token: str, redis_client: Redis):
    # Token is blacklisted with TTL
    await blacklist_token(token, redis_client)
    return {"message": "Logged out successfully"}
```

### Checking Blacklist
```python
async def verify_token_not_blacklisted(token: str, redis_client: Redis):
    is_blacklisted = await redis_client.exists(f"blacklist:{token}")
    if is_blacklisted:
        raise HTTPException(status_code=401, detail="Token is blacklisted")
```

## Caching Strategy

### Cache Patterns
- **User Data**: Cache with 5-minute TTL
- **Configuration**: Cache with 1-hour TTL
- **Session Data**: Cache with session timeout TTL
- **API Responses**: Conditional caching based on headers

### Cache Key Naming
```
user:{user_id}
post:{post_id}
feed:{user_id}:page:{page}
config:{key}
session:{session_id}
```

## Project Structure

```
├── main.py
├── config.py
├── requirements.txt
├── redis_client.py
├── models/
│   ├── token.py
│   ├── session.py
│   └── rate_limit.py
├── schemas/
│   ├── token.py
│   ├── session.py
│   └── cache.py
├── routes/
│   ├── tokens.py
│   ├── rate_limit.py
│   ├── cache.py
│   └── sessions.py
├── services/
│   ├── redis_service.py
│   ├── token_service.py
│   ├── rate_limit_service.py
│   ├── cache_service.py
│   └── session_service.py
├── utils/
│   ├── cache_utils.py
│   ├── rate_limit_utils.py
│   └── token_utils.py
├── database/
│   └── database.py
├── tests/
│   ├── test_token_blacklist.py
│   ├── test_rate_limit.py
│   ├── test_cache.py
│   └── test_sessions.py
└── middleware/
    ├── rate_limit.py
    └── cache.py
```

## Redis Client Setup

```python
from redis import Redis
from redis.asyncio import Redis as AsyncRedis

# Synchronous client
redis_sync = Redis.from_url(REDIS_URL)

# Asynchronous client
redis_async = AsyncRedis.from_url(REDIS_URL)
```

## Running Tests

```bash
pytest tests/ -v
```

## Monitoring Redis

### Redis CLI
```bash
redis-cli
> INFO
> DBSIZE
> KEYS *
> FLUSHDB
```

### Monitor Commands
```bash
redis-cli MONITOR
redis-cli SLOWLOG GET 10
```

## Performance Optimization

- Use Redis connection pooling
- Implement pipeline operations for batch commands
- Use Lua scripts for atomic operations
- Monitor Redis memory usage
- Implement appropriate eviction policies

## High Availability

### Redis Sentinel
```
sentinel.conf:
port 26379
sentinel monitor mymaster 127.0.0.1 6379 1
```

### Redis Cluster
Requires 6+ nodes in production.

## Troubleshooting

### Connection Issues
- Verify Redis is running: `redis-cli ping`
- Check connection URL configuration
- Verify firewall rules

### Performance Issues
- Monitor Redis memory: `redis-cli INFO memory`
- Check key eviction: `redis-cli INFO stats`
- Review command latency: `redis-cli SLOWLOG GET`

### Token Expiration
- Verify TTL is set correctly
- Check blacklist key format
- Monitor Redis memory for expired keys

## Contributing

Ensure all Redis operations have proper error handling and connection management.
