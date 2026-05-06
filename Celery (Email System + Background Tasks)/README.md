# Celery (Email System + Background Tasks)

An asynchronous task queue system built with FastAPI and Celery for handling email delivery and background job processing with retry logic and monitoring.

## Features

- **Async Email Delivery** - Send emails asynchronously using Celery
- **Task Retry Logic** - Automatic retry mechanism with exponential backoff
- **Email Templates** - HTML email templates with dynamic content
- **Task Monitoring** - Monitor task status and history
- **Background Jobs** - Schedule and execute long-running background tasks
- **Task Scheduling** - Periodic task execution with Celery Beat
- **Error Handling** - Robust error handling with dead letter queues
- **Task Chaining** - Complex task workflows with signatures and chains

## Tech Stack

- **Framework**: FastAPI
- **Task Queue**: Celery 5.x
- **Message Broker**: Redis
- **Task Scheduler**: Celery Beat
- **Email**: Aiosmtplib / SendGrid
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

5. Start Celery worker:
```bash
celery -A tasks worker --loglevel=info
```

6. Start Celery Beat (for scheduled tasks):
```bash
celery -A tasks beat --loglevel=info
```

7. Start FastAPI application:
```bash
uvicorn main:app --reload
```

## API Endpoints

### Email Tasks
- `POST /api/tasks/send-email` - Send email asynchronously
- `GET /api/tasks/{task_id}` - Check task status
- `GET /api/tasks/{task_id}/result` - Get task result
- `POST /api/tasks/{task_id}/cancel` - Cancel a task

### Bulk Operations
- `POST /api/tasks/send-bulk-emails` - Send emails to multiple recipients
- `POST /api/tasks/export-data` - Export data (background task)
- `POST /api/tasks/generate-report` - Generate reports

### Task Management
- `GET /api/tasks` - List all tasks
- `GET /api/tasks/pending` - List pending tasks
- `GET /api/tasks/active` - List active tasks
- `GET /api/tasks/failed` - List failed tasks

## Environment Variables

```
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/1
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SENDER_EMAIL=noreply@example.com
CELERY_TASK_SOFT_TIME_LIMIT=300
CELERY_TASK_HARD_TIME_LIMIT=600
CELERY_TASK_MAX_RETRIES=3
DATABASE_URL=postgresql://user:password@localhost/celery_db
```

## Task Examples

### Send Email
```python
from tasks import send_email

# Async execution
task = send_email.delay(
    to_email="user@example.com",
    subject="Welcome",
    template="welcome.html",
    context={"name": "John"}
)

# Check status
status = task.status
result = task.result
```

### Send Bulk Emails
```python
from tasks import send_bulk_emails

task = send_bulk_emails.delay(
    recipients=["user1@example.com", "user2@example.com"],
    subject="Newsletter",
    template="newsletter.html"
)
```

### Periodic Tasks
```python
# Defined in celery.py
app.conf.beat_schedule = {
    'send-daily-digest': {
        'task': 'tasks.send_daily_digest',
        'schedule': crontab(hour=9, minute=0),
    },
}
```

## Project Structure

```
├── main.py
├── celery_config.py
├── tasks.py
├── requirements.txt
├── models/
│   ├── task.py
│   └── email_log.py
├── schemas/
│   ├── task.py
│   └── email.py
├── routes/
│   └── tasks.py
├── services/
│   ├── email_service.py
│   ├── task_service.py
│   └── notification_service.py
├── templates/
│   ├── welcome.html
│   ├── password_reset.html
│   ├── newsletter.html
│   └── order_confirmation.html
├── utils/
│   ├── email_utils.py
│   └── task_utils.py
├── database/
│   └── database.py
├── tests/
│   ├── test_tasks.py
│   └── test_email_service.py
└── celery_app.py
```

## Task Retry Logic

- **Retry Strategy**: Exponential backoff (2, 4, 8, 16 seconds)
- **Max Retries**: 3 attempts by default
- **Backoff Factor**: 2
- **Dead Letter Queue**: Failed tasks after max retries

## Email Templates

Located in `templates/`:
- `welcome.html` - User registration welcome email
- `password_reset.html` - Password reset instructions
- `newsletter.html` - Newsletter template
- `order_confirmation.html` - Order confirmation email

## Running Tests

```bash
pytest tests/ -v
```

## Monitoring

### Celery Flower (Optional)
```bash
pip install flower
celery -A tasks flower
# Access at http://localhost:5555
```

## Performance Considerations

- Use connection pooling for database
- Configure appropriate worker concurrency
- Monitor task queue lengths
- Set reasonable time limits for tasks
- Use rate limiting for API endpoints

## Troubleshooting

### Tasks Not Running
- Check Redis is running: `redis-cli ping`
- Verify Celery worker is running
- Check Celery logs for errors

### Email Not Sending
- Verify SMTP credentials
- Check email service logs
- Ensure firewall allows SMTP port

## Contributing

Ensure all tasks have proper error handling and logging.
