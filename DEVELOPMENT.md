# Development Guide

Quick guide for developers working on Forgotten Ruin MUD.

## Initial Setup

### 1. Install Prerequisites

See [PREREQUISITES.md](PREREQUISITES.md) for detailed instructions.

**Quick Install (macOS with Homebrew):**
```bash
brew install postgresql@13 redis
brew services start postgresql@13
brew services start redis
```

### 2. Run Setup Script

```bash
# From anywhere in the project
./scripts/setup_test_environment.sh
```

This installs all dependencies and sets up test data.

## Development Workflow

### Start Development Servers

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
python manage.py runserver
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

**Terminal 3 - Tests (optional):**
```bash
./test.sh coverage
```

### Running Tests

```bash
# All tests
./test.sh all

# Specific suites
./test.sh accounts
./test.sh chat
./test.sh websocket

# With coverage
./test.sh coverage

# Quick smoke tests
./test.sh quick
```

### Code Changes

**Backend (Python/Django):**
```bash
cd backend
source venv/bin/activate

# Create migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Run tests
pytest

# Check code style
flake8
black .
```

**Frontend (React):**
```bash
cd frontend

# Run tests
npm test

# Build for production
npm run build

# Format code
npm run format  # if configured
```

## Project Structure

```
Forgotten_Ruin_MUD/
├── backend/              # Django backend
│   ├── server/          # Django project settings
│   ├── accounts/        # User authentication
│   ├── game/            # Core game logic
│   ├── websocket/       # WebSocket handlers
│   ├── api/             # REST API
│   └── tests/           # Backend tests
│
├── frontend/            # React frontend
│   ├── src/
│   │   ├── components/ # React components
│   │   ├── pages/      # Page components
│   │   ├── services/   # API services
│   │   └── hooks/      # Custom React hooks
│   └── public/
│
├── scripts/             # Utility scripts
├── tests/              # Test documentation
├── docs/               # Project documentation
└── research/           # Research materials
```

## Common Tasks

### Create New Django App

```bash
cd backend
python manage.py startapp myapp
```

Then add to `INSTALLED_APPS` in `server/settings.py`.

### Create New API Endpoint

1. Add view in `backend/api/v1/views.py`
2. Add serializer in `backend/api/v1/serializers.py`
3. Add URL in `backend/api/v1/urls.py`
4. Write tests in `backend/tests/test_api.py`

### Add New Chat Command

1. Create command class in `backend/game/commands/`
2. Register in `backend/game/commands/__init__.py`
3. Write tests in `backend/tests/test_chat_commands.py`

### Add New Frontend Component

1. Create component in `frontend/src/components/`
2. Import in parent component
3. Add styles in component CSS file

## Database Management

```bash
cd backend
source venv/bin/activate

# Create migration
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Django shell
python manage.py shell

# Database shell
python manage.py dbshell
```

## Debugging

### Backend

```python
# Add breakpoint in code
import pdb; pdb.set_trace()

# Or use Django debug toolbar (if installed)
```

Run with:
```bash
python manage.py runserver
```

### Frontend

Use browser DevTools:
- Chrome DevTools (F12)
- React DevTools extension
- Console logging: `console.log()`

### WebSocket Debugging

Use browser Network tab → WS filter to see WebSocket traffic.

## Testing

See [TESTING_QUICK_START.md](TESTING_QUICK_START.md) for complete testing guide.

### Quick Test Commands

```bash
# Run all tests
./test.sh all

# Run with output
cd backend
pytest -v -s

# Run specific test
pytest tests/test_accounts.py::TestUserRegistration::test_valid_registration

# Coverage report
./test.sh coverage
```

## Code Style

### Python

- Follow PEP 8
- Use `black` for formatting
- Use `flake8` for linting
- Maximum line length: 100 characters

```bash
# Format code
black .

# Check style
flake8

# Type checking (if using mypy)
mypy .
```

### JavaScript/React

- Use ESLint (if configured)
- Use Prettier for formatting
- Follow React best practices

## Git Workflow

```bash
# Create feature branch
git checkout -b feature/my-feature

# Make changes and commit
git add .
git commit -m "Add feature description"

# Push to remote
git push origin feature/my-feature

# Create pull request on GitHub
```

## Troubleshooting

### Virtual Environment Issues

```bash
# Recreate virtual environment
cd backend
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Database Issues

```bash
# Drop and recreate database
dropdb forgotten_ruin
createdb forgotten_ruin
python manage.py migrate
python manage.py shell < tests/generate_test_data.py
```

### Redis Issues

```bash
# Check if running
redis-cli ping

# Restart Redis
brew services restart redis  # macOS
sudo systemctl restart redis # Linux
```

### Frontend Issues

```bash
# Clear node_modules and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## Documentation

- [TEST_PLAN.md](TEST_PLAN.md) - Testing strategy
- [TESTING_QUICK_START.md](TESTING_QUICK_START.md) - Quick testing guide
- [PREREQUISITES.md](PREREQUISITES.md) - Prerequisites installation
- [tests/MANUAL_TESTS.md](tests/MANUAL_TESTS.md) - Manual testing procedures
- [docs/](docs/) - Additional documentation

## Getting Help

1. Check documentation in `docs/`
2. Check troubleshooting sections
3. Review test examples
4. Check Django/React documentation
5. Create an issue on GitHub

Happy coding! 🚀
