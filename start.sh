#!/bin/bash

###############################################################################
# Forgotten Ruin MUD - Development Server Startup Script
#
# This script starts both backend and frontend development servers
# and manages their lifecycle.
###############################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$PROJECT_ROOT/backend"
FRONTEND_DIR="$PROJECT_ROOT/frontend"

# PID files for process management
BACKEND_PID=""
FRONTEND_PID=""
REDIS_STARTED_BY_SCRIPT=false

# Print colored message
print_msg() {
    local color=$1
    shift
    echo -e "${color}$@${NC}"
}

# Print section header
print_header() {
    echo ""
    print_msg "$BLUE" "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    print_msg "$BLUE" "$1"
    print_msg "$BLUE" "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

# Cleanup function - called on script exit
cleanup() {
    print_header "🛑 Shutting down servers..."

    if [ ! -z "$BACKEND_PID" ]; then
        print_msg "$YELLOW" "Stopping backend server (PID: $BACKEND_PID)..."
        kill $BACKEND_PID 2>/dev/null || true
        wait $BACKEND_PID 2>/dev/null || true
    fi

    if [ ! -z "$FRONTEND_PID" ]; then
        print_msg "$YELLOW" "Stopping frontend server (PID: $FRONTEND_PID)..."
        kill $FRONTEND_PID 2>/dev/null || true
        wait $FRONTEND_PID 2>/dev/null || true
    fi

    # Stop Redis if we started it
    if [ "$REDIS_STARTED_BY_SCRIPT" = true ]; then
        print_msg "$YELLOW" "Stopping Redis server..."
        if command -v brew &> /dev/null; then
            brew services stop redis 2>/dev/null || true
        else
            redis-cli shutdown 2>/dev/null || true
        fi
    fi

    print_msg "$GREEN" "✓ All servers stopped"
    echo ""
}

# Set trap to cleanup on exit
trap cleanup EXIT INT TERM

# Check if a command exists
command_exists() {
    command -v "$1" &> /dev/null
}

# Check if Redis is running
check_redis() {
    redis-cli ping &> /dev/null
    return $?
}

# Start Redis if not running
ensure_redis() {
    print_header "🔍 Checking Redis..."

    if ! command_exists redis-cli; then
        print_msg "$RED" "✗ Redis is not installed!"
        print_msg "$YELLOW" "Please install Redis:"
        print_msg "$YELLOW" "  macOS: brew install redis"
        print_msg "$YELLOW" "  Ubuntu/Debian: sudo apt-get install redis-server"
        print_msg "$YELLOW" "  Fedora: sudo dnf install redis"
        exit 1
    fi

    if check_redis; then
        print_msg "$GREEN" "✓ Redis is already running"
    else
        print_msg "$YELLOW" "Starting Redis server..."

        if command_exists brew; then
            # macOS with Homebrew
            brew services start redis &> /dev/null || redis-server --daemonize yes
            REDIS_STARTED_BY_SCRIPT=true
        else
            # Linux or manual start
            redis-server --daemonize yes
            REDIS_STARTED_BY_SCRIPT=true
        fi

        # Wait for Redis to start
        sleep 2

        if check_redis; then
            print_msg "$GREEN" "✓ Redis started successfully"
        else
            print_msg "$RED" "✗ Failed to start Redis"
            exit 1
        fi
    fi
}

# Check Python and dependencies
check_backend_deps() {
    print_header "🔍 Checking Backend Dependencies..."

    # Check Python
    if ! command_exists python3 && ! command_exists python; then
        print_msg "$RED" "✗ Python is not installed!"
        exit 1
    fi

    PYTHON_CMD=$(command_exists python3 && echo "python3" || echo "python")
    print_msg "$GREEN" "✓ Found Python: $($PYTHON_CMD --version)"

    # Check if backend directory exists
    if [ ! -d "$BACKEND_DIR" ]; then
        print_msg "$RED" "✗ Backend directory not found: $BACKEND_DIR"
        exit 1
    fi

    # Check if requirements are installed
    cd "$BACKEND_DIR"
    if [ ! -f "requirements.txt" ]; then
        print_msg "$RED" "✗ requirements.txt not found"
        exit 1
    fi

    # Check if Django is installed
    if ! $PYTHON_CMD -c "import django" 2>/dev/null; then
        print_msg "$YELLOW" "⚠ Django not found. Installing dependencies..."
        pip3 install -r requirements.txt
    fi

    print_msg "$GREEN" "✓ Backend dependencies OK"
}

# Check Node.js and dependencies
check_frontend_deps() {
    print_header "🔍 Checking Frontend Dependencies..."

    # Check Node.js
    if ! command_exists node; then
        print_msg "$RED" "✗ Node.js is not installed!"
        print_msg "$YELLOW" "Please install Node.js from https://nodejs.org/"
        exit 1
    fi

    print_msg "$GREEN" "✓ Found Node.js: $(node --version)"

    # Check npm
    if ! command_exists npm; then
        print_msg "$RED" "✗ npm is not installed!"
        exit 1
    fi

    print_msg "$GREEN" "✓ Found npm: $(npm --version)"

    # Check if frontend directory exists
    if [ ! -d "$FRONTEND_DIR" ]; then
        print_msg "$RED" "✗ Frontend directory not found: $FRONTEND_DIR"
        exit 1
    fi

    # Check if node_modules exists
    cd "$FRONTEND_DIR"
    if [ ! -d "node_modules" ]; then
        print_msg "$YELLOW" "⚠ node_modules not found. Installing dependencies..."
        npm install
    fi

    print_msg "$GREEN" "✓ Frontend dependencies OK"
}

# Create necessary directories
create_directories() {
    print_header "📁 Creating Required Directories..."

    cd "$BACKEND_DIR"

    # Create logs directory if it doesn't exist
    if [ ! -d "logs" ]; then
        mkdir -p logs
        print_msg "$YELLOW" "Created logs directory"
    fi

    # Create static directory if it doesn't exist
    if [ ! -d "static" ]; then
        mkdir -p static
        print_msg "$YELLOW" "Created static directory"
    fi

    # Create media directory if it doesn't exist
    if [ ! -d "media" ]; then
        mkdir -p media
        print_msg "$YELLOW" "Created media directory"
    fi

    print_msg "$GREEN" "✓ All required directories present"
}

# Run database migrations
run_migrations() {
    print_header "🗄️  Running Database Migrations..."

    cd "$BACKEND_DIR"
    PYTHON_CMD=$(command_exists python3 && echo "python3" || echo "python")

    if $PYTHON_CMD manage.py migrate --check &> /dev/null; then
        print_msg "$GREEN" "✓ Database is up to date"
    else
        print_msg "$YELLOW" "Running migrations..."
        $PYTHON_CMD manage.py migrate
        print_msg "$GREEN" "✓ Migrations complete"
    fi
}

# Start backend server
start_backend() {
    print_header "🚀 Starting Backend Server..."

    cd "$BACKEND_DIR"
    PYTHON_CMD=$(command_exists python3 && echo "python3" || echo "python")

    # Check if Daphne is installed (required for WebSockets)
    if ! $PYTHON_CMD -c "import daphne" 2>/dev/null; then
        print_msg "$YELLOW" "⚠ Daphne not found. Installing..."
        pip3 install daphne
    fi

    # Start ASGI server (Daphne) for WebSocket support
    # Note: Django's runserver doesn't support WebSockets
    # Use python -m to ensure we use the correct daphne installation
    $PYTHON_CMD -m daphne -b 0.0.0.0 -p 8000 server.asgi:application > /tmp/forgotten_ruin_backend.log 2>&1 &
    BACKEND_PID=$!

    # Wait a moment and check if it's still running
    sleep 3
    if kill -0 $BACKEND_PID 2>/dev/null; then
        print_msg "$GREEN" "✓ Backend server started with Daphne (PID: $BACKEND_PID)"
        print_msg "$GREEN" "  HTTP: http://localhost:8000"
        print_msg "$GREEN" "  WebSocket: ws://localhost:8000/ws/"
        print_msg "$YELLOW" "  Logs: tail -f /tmp/forgotten_ruin_backend.log"
    else
        print_msg "$RED" "✗ Backend server failed to start"
        print_msg "$RED" "Check logs: cat /tmp/forgotten_ruin_backend.log"
        exit 1
    fi
}

# Start frontend server
start_frontend() {
    print_header "🚀 Starting Frontend Server..."

    cd "$FRONTEND_DIR"

    # Start React development server in background
    BROWSER=none npm start > /tmp/forgotten_ruin_frontend.log 2>&1 &
    FRONTEND_PID=$!

    # Wait a moment and check if it's still running
    sleep 3
    if kill -0 $FRONTEND_PID 2>/dev/null; then
        print_msg "$GREEN" "✓ Frontend server started (PID: $FRONTEND_PID)"
        print_msg "$GREEN" "  URL: http://localhost:3000"
        print_msg "$YELLOW" "  Logs: tail -f /tmp/forgotten_ruin_frontend.log"
    else
        print_msg "$RED" "✗ Frontend server failed to start"
        print_msg "$RED" "Check logs: cat /tmp/forgotten_ruin_frontend.log"
        exit 1
    fi
}

# Show status and instructions
show_status() {
    print_header "✨ Forgotten Ruin MUD is Running!"

    echo ""
    print_msg "$GREEN" "🎮 Game Interface:  http://localhost:3000"
    print_msg "$GREEN" "🔧 Admin Panel:     http://localhost:8000/admin"
    print_msg "$GREEN" "📡 API Docs:        http://localhost:8000/api/v1/"
    echo ""
    print_msg "$YELLOW" "📝 View Logs:"
    print_msg "$YELLOW" "  Backend:  tail -f /tmp/forgotten_ruin_backend.log"
    print_msg "$YELLOW" "  Frontend: tail -f /tmp/forgotten_ruin_frontend.log"
    echo ""
    print_msg "$BLUE" "Press Ctrl+C to stop all servers"
    echo ""
    print_msg "$BLUE" "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
}

# Open browser (optional)
open_browser() {
    if [ "${OPEN_BROWSER:-true}" = "true" ]; then
        print_msg "$YELLOW" "Opening browser..."
        sleep 5

        if command_exists open; then
            # macOS
            open http://localhost:3000
        elif command_exists xdg-open; then
            # Linux
            xdg-open http://localhost:3000
        elif command_exists start; then
            # Windows Git Bash
            start http://localhost:3000
        fi
    fi
}

###############################################################################
# Main Script
###############################################################################

main() {
    clear

    print_header "🏰 Forgotten Ruin MUD - Startup Script"
    print_msg "$BLUE" "Starting development environment..."

    # Run checks
    ensure_redis
    check_backend_deps
    check_frontend_deps
    create_directories
    run_migrations

    # Start servers
    start_backend
    start_frontend

    # Show status
    show_status

    # Optionally open browser
    open_browser &

    # Wait for user interrupt
    print_msg "$GREEN" "Servers are running. Press Ctrl+C to stop..."

    # Keep script running and wait for both processes
    wait $BACKEND_PID $FRONTEND_PID
}

# Run main function
main
