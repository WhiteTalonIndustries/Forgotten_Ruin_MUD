# Setup Guide

Complete guide to setting up the Forgotten Ruin MUD development environment.

## Prerequisites

### Required Software

- **Python 3.10+**: [Download Python](https://www.python.org/downloads/)
- **Node.js 16+**: [Download Node.js](https://nodejs.org/)
- **PostgreSQL 13+**: [Download PostgreSQL](https://www.postgresql.org/download/)
- **Redis 6+**: [Download Redis](https://redis.io/download)
- **Git**: [Download Git](https://git-scm.com/downloads)

## Backend Setup

### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

```bash
# Copy example environment file
cp ../.env.example ../.env

# Edit .env with your configuration
# Update these values:
# - DJANGO_SECRET_KEY (generate new for production)
# - DB_PASSWORD (your PostgreSQL password)
# - DEBUG (False for production)
```

### 4. Set Up Database

```bash
# Create PostgreSQL database
createdb forgotten_ruin

# Or using psql:
psql -U postgres
CREATE DATABASE forgotten_ruin;
\q

# Run migrations
python manage.py migrate
```

### 5. Create Superuser

```bash
python manage.py createsuperuser
# Follow prompts to create admin account
```

### 6. Create Initial Game Data (Optional)

```bash
# Load sample zones, rooms, etc.
python manage.py loaddata initial_data.json
```

### 7. Run Development Server

#### Option A: Django Development Server (HTTP only)
```bash
python manage.py runserver
```

#### Option B: Daphne (ASGI server with WebSocket support)
```bash
daphne -b 0.0.0.0 -p 8000 server.asgi:application
```

### 8. Start Redis

```bash
# macOS (with Homebrew)
brew services start redis

# Linux
sudo systemctl start redis

# Or run directly
redis-server
```

### 9. Start Celery (Optional, for background tasks)

```bash
# In a new terminal
celery -A server worker -l info
```

## Frontend Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment

```bash
# Create .env file
echo "REACT_APP_API_URL=http://localhost:8000" > .env
echo "REACT_APP_WS_URL=ws://localhost:8000" >> .env
```

### 3. Run Development Server

```bash
npm start
```

The application will open at http://localhost:3000

## Verification

### 1. Check Backend

- Visit http://localhost:8000/admin/
- Login with superuser credentials
- You should see the Django admin interface

### 2. Check API

- Visit http://localhost:8000/api/v1/
- You should see the DRF browsable API

### 3. Check Frontend

- Visit http://localhost:3000
- You should see the game homepage
- Try registering a new account and logging in

### 4. Check WebSocket

- After logging in, go to the game page
- Open browser console
- You should see "WebSocket connected" message

## Common Issues

### Database Connection Error

**Error**: `django.db.utils.OperationalError: FATAL: database "forgotten_ruin" does not exist`

**Solution**: Create the database:
```bash
createdb forgotten_ruin
```

### Redis Connection Error

**Error**: `Error connecting to Redis`

**Solution**: Start Redis:
```bash
redis-server
```

### Module Not Found

**Error**: `ModuleNotFoundError: No module named 'channels'`

**Solution**: Install dependencies:
```bash
pip install -r requirements.txt
```

### Port Already in Use

**Error**: `Error: That port is already in use`

**Solution**: Change port or kill existing process:
```bash
# Django (use different port)
python manage.py runserver 8001

# Or find and kill process
lsof -ti:8000 | xargs kill -9
```

### CORS Issues

**Error**: Browser console shows CORS errors

**Solution**: Check CORS_ALLOWED_ORIGINS in .env:
```
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080
```

## Production Deployment

See [docs/DEPLOYMENT.md](./DEPLOYMENT.md) for production deployment instructions.

## Next Steps

- Read [project.md](../project.md) for project requirements
- Check [research/](../research/) for implementation guidelines
- Review [docs/architecture/](./architecture/) for system design

## Need Help?

- Check existing issues on GitHub
- Join our Discord community
- Read the documentation in [docs/](./)