# Startup Scripts Guide

This guide explains how to use the startup scripts to quickly launch the Forgotten Ruin MUD development environment.

## Quick Start

### Start Everything (One Command)

```bash
./start.sh
```

This single command will:
- ✅ Check and start Redis (if needed)
- ✅ Verify Python and Node.js dependencies
- ✅ Run database migrations
- ✅ Start the Django backend server (port 8000)
- ✅ Start the React frontend server (port 3000)
- ✅ Automatically open your browser

### Stop Everything

```bash
./stop.sh
```

Or simply press **Ctrl+C** in the terminal where `start.sh` is running.

## Detailed Usage

### start.sh Features

The startup script includes:

1. **Automatic Dependency Checking**
   - Verifies Redis is installed and running
   - Checks Python/Django installation
   - Checks Node.js/npm installation
   - Installs missing dependencies if needed

2. **Database Management**
   - Automatically runs pending migrations
   - Checks database health

3. **Process Management**
   - Starts both servers as background processes
   - Captures PIDs for clean shutdown
   - Properly handles Ctrl+C signals
   - Cleans up all processes on exit

4. **Logging**
   - Backend logs: `/tmp/forgotten_ruin_backend.log`
   - Frontend logs: `/tmp/forgotten_ruin_frontend.log`

5. **Colored Output**
   - Clear status messages
   - Easy-to-read error reporting
   - Progress indicators

### Configuration Options

You can customize the startup behavior with environment variables:

```bash
# Don't auto-open browser
OPEN_BROWSER=false ./start.sh

# Use PostgreSQL instead of SQLite (requires PostgreSQL to be running)
USE_POSTGRES=true ./start.sh

# Use specific Python version
PYTHON_CMD=python3.11 ./start.sh
```

#### Database Configuration

By default, the project uses **SQLite** for development (no setup required). To use PostgreSQL:

```bash
# Start PostgreSQL (macOS with Homebrew)
brew services start postgresql

# Set environment variable to use PostgreSQL
export USE_POSTGRES=true

# Then start the servers
./start.sh
```

Or configure PostgreSQL connection details:

```bash
export USE_POSTGRES=true
export DB_NAME=forgotten_ruin
export DB_USER=your_username
export DB_PASSWORD=your_password
export DB_HOST=localhost
export DB_PORT=5432
```

### Script Locations

- **Start Script**: `./start.sh`
- **Stop Script**: `./stop.sh`
- Both scripts must be run from the project root directory

## Troubleshooting

### "Permission denied" Error

If you get a permission error, make the scripts executable:

```bash
chmod +x start.sh stop.sh
```

### Redis Not Starting

**macOS (Homebrew):**
```bash
brew services start redis
```

**Linux:**
```bash
sudo systemctl start redis
# or
redis-server --daemonize yes
```

**Manual check:**
```bash
redis-cli ping
# Should return: PONG
```

### Port Already in Use

If port 8000 or 3000 is already in use:

**Find and kill the process:**
```bash
# For backend (port 8000)
lsof -ti:8000 | xargs kill

# For frontend (port 3000)
lsof -ti:3000 | xargs kill
```

Or use the stop script:
```bash
./stop.sh
```

### Backend/Frontend Won't Start

Check the log files for detailed error messages:

```bash
# Backend logs
tail -f /tmp/forgotten_ruin_backend.log

# Frontend logs
tail -f /tmp/forgotten_ruin_frontend.log
```

### Missing Dependencies

If dependencies are missing:

**Backend:**
```bash
cd backend
pip3 install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

Then run `./start.sh` again.

## Manual Startup (Without Scripts)

If you prefer to start servers manually:

### Terminal 1 - Redis
```bash
redis-server
```

### Terminal 2 - Backend
```bash
cd backend
python manage.py runserver
```

### Terminal 3 - Frontend
```bash
cd frontend
npm start
```

## Accessing the Application

Once started, you can access:

- **🎮 Game Interface**: http://localhost:3000
- **🔧 Django Admin**: http://localhost:8000/admin
- **📡 API Documentation**: http://localhost:8000/api/v1/

## Development Workflow

### Typical Development Session

```bash
# 1. Start everything
./start.sh

# 2. Make your changes to code files
# Both servers will auto-reload on changes

# 3. View logs in separate terminals (optional)
tail -f /tmp/forgotten_ruin_backend.log
tail -f /tmp/forgotten_ruin_frontend.log

# 4. When done, stop everything
# Press Ctrl+C or run:
./stop.sh
```

### Running Tests

Keep servers running and open a new terminal:

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## Advanced Usage

### Starting Only Backend

```bash
cd backend
python manage.py runserver
```

### Starting Only Frontend

```bash
cd frontend
npm start
```

### Production-Like Build

```bash
# Build frontend for production
cd frontend
npm run build

# Serve with Django
cd ../backend
python manage.py collectstatic --noinput
python manage.py runserver
```

## Script Maintenance

### Customizing start.sh

The script is well-commented. Key sections:

- **Lines 25-35**: Color definitions
- **Lines 37-42**: Path configuration
- **Lines 77-101**: Redis management
- **Lines 169-190**: Backend startup
- **Lines 193-213**: Frontend startup

Feel free to modify these sections for your needs.

### Adding Custom Checks

To add custom dependency checks, add a function following this pattern:

```bash
check_custom_dependency() {
    print_header "🔍 Checking Custom Dependency..."

    if command_exists your_command; then
        print_msg "$GREEN" "✓ Found: $(your_command --version)"
    else
        print_msg "$RED" "✗ Not found!"
        exit 1
    fi
}
```

Then call it in the `main()` function.

## Environment-Specific Configuration

### Development
```bash
./start.sh
```

### Staging (with production settings)
```bash
DJANGO_SETTINGS_MODULE=server.staging_settings ./start.sh
```

### Custom Ports

Edit the scripts to use different ports:

**In start.sh:**
```bash
# Change line ~175:
$PYTHON_CMD manage.py runserver 8080  # Backend on port 8080

# Frontend port is set in package.json:
# "start": "PORT=3001 react-scripts start"
```

## Continuous Integration

For CI/CD pipelines, use the script with the following settings:

```bash
# Run without opening browser
OPEN_BROWSER=false ./start.sh &

# Wait for servers to be ready
sleep 10

# Run tests
cd backend && pytest
cd ../frontend && npm test

# Stop servers
./stop.sh
```

## Getting Help

If you encounter issues:

1. Check the troubleshooting section above
2. Review log files
3. Try manual startup to isolate the problem
4. Check Redis is running: `redis-cli ping`
5. Verify ports are available: `lsof -i :8000` and `lsof -i :3000`

## Contributing

When modifying the startup scripts:

1. Test on your local environment
2. Document any new features or options
3. Update this guide with changes
4. Ensure backward compatibility
5. Add error handling for new features

## Related Documentation

- [Quick Start Testing Guide](docs/QUICK_START_TESTING.md)
- [Chat and Player Integration](docs/CHAT_AND_PLAYER_INTEGRATION.md)
- [Main README](README.md)

---

**Happy Developing!** 🏰✨
