# Blog System (CRUD + Pagination)

A RESTful API for a blogging platform built with FastAPI, featuring complete CRUD operations, pagination, and author-based authorization.

## Features

- **Create Posts** - Create new blog posts with title, content, and tags
- **Read Posts** - Retrieve posts with advanced filtering and search
- **Update Posts** - Edit existing blog posts (author-only)
- **Delete Posts** - Remove blog posts (author-only)
- **Pagination** - Support for both offset-based and cursor-based pagination
- **Authorization** - Author-based access control for post modifications
- **Filtering & Search** - Filter by author, tags, date range
- **Comments** - Add comments to blog posts
- **Tags** - Categorize posts with tags

## Tech Stack

- **Framework**: FastAPI
- **Database**: SQLAlchemy + PostgreSQL
- **Authentication**: JWT (from Auth System)
- **Pagination**: Cursor-based and offset-based
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

### Blog Posts
- `GET /api/posts` - List all posts with pagination
- `POST /api/posts` - Create a new post (authenticated)
- `GET /api/posts/{post_id}` - Get post details
- `PUT /api/posts/{post_id}` - Update post (author-only)
- `DELETE /api/posts/{post_id}` - Delete post (author-only)

### Comments
- `GET /api/posts/{post_id}/comments` - List comments for a post
- `POST /api/posts/{post_id}/comments` - Add comment (authenticated)
- `DELETE /api/posts/{post_id}/comments/{comment_id}` - Delete comment (author-only)

### Tags
- `GET /api/tags` - List all tags
- `GET /api/posts/tag/{tag_name}` - Get posts by tag

### Search & Filtering
- `GET /api/posts?search=query` - Search posts
- `GET /api/posts?author_id=123` - Filter by author
- `GET /api/posts?tags=python,fastapi` - Filter by tags

## Pagination

### Offset-based Pagination
```
GET /api/posts?skip=0&limit=10
```

### Cursor-based Pagination
```
GET /api/posts?cursor=abc123&limit=10
```

## Environment Variables

```
DATABASE_URL=postgresql://user:password@localhost/blog_db
JWT_SECRET_KEY=your-secret-key-here
POSTS_PER_PAGE=10
MAX_PAGE_SIZE=100
```

## Database Schema

- **posts** - Blog post data
- **comments** - Post comments
- **tags** - Tag definitions
- **post_tags** - Many-to-many relationship between posts and tags
- **users** - User accounts (from Auth System)

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
│   ├── post.py
│   ├── comment.py
│   ├── tag.py
│   └── user.py
├── schemas/
│   ├── post.py
│   ├── comment.py
│   └── tag.py
├── routes/
│   ├── posts.py
│   ├── comments.py
│   └── tags.py
├── services/
│   ├── post_service.py
│   └── pagination_service.py
├── utils/
│   ├── filters.py
│   └── pagination.py
├── database/
│   └── database.py
├── tests/
│   ├── test_posts.py
│   └── test_pagination.py
└── alembic/
    └── versions/
```

## Pagination Implementation

### Offset Pagination
Suitable for small to medium-sized datasets. Returns total count and pages.

### Cursor Pagination
Recommended for large datasets. Uses encoded cursors for efficient navigation.

## Authorization

- Only post authors can update or delete their posts
- Comments inherit author permissions
- Admins can manage all content

## Contributing

Follow FastAPI best practices and ensure comprehensive test coverage.
