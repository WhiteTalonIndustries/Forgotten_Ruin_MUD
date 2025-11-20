#!/bin/bash

# =============================================================================
# Test Environment Setup Script
# =============================================================================
# This script sets up a complete local testing environment for Forgotten Ruin MUD
#
# Usage:
#   ./scripts/setup_test_environment.sh [options]
#
# Options:
#   --clean     Clean existing test data before setup
#   --skip-deps Skip dependency installation
#   --help      Show this help message
# =============================================================================

set -e  # Exit on error

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# Navigate to project root (parent of scripts directory)
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Flags
CLEAN_DATA=false
SKIP_DEPS=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --clean)
            CLEAN_DATA=true
            shift
            ;;
        --skip-deps)
            SKIP_DEPS=true
            shift
            ;;
        --help)
            head -n 20 "$0" | tail -n 15
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done

# Print colored message
print_step() {
    echo -e "\n${BLUE}==>${NC} ${GREEN}$1${NC}"
}

print_error() {
    echo -e "${RED}ERROR: $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}WARNING: $1${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

# =============================================================================
# Step 0: Navigate to Project Root
# =============================================================================

cd "$PROJECT_ROOT"
echo "Working directory: $PROJECT_ROOT"
echo ""

# =============================================================================
# Step 1: Check Prerequisites
# =============================================================================

print_step "Checking prerequisites..."

# Check Python
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed"
    exit 1
fi
print_success "Python 3 found: $(python3 --version)"

# Check Node.js
if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed"
    exit 1
fi
print_success "Node.js found: $(node --version)"

# Check PostgreSQL
if ! command -v psql &> /dev/null; then
    print_warning "PostgreSQL client (psql) not found in PATH"
    echo "  If PostgreSQL is installed, you may need to add it to PATH"
    echo "  macOS: Try 'brew services list' to check if it's running"
    echo "  Or install with: 'brew install postgresql@13'"
else
    print_success "PostgreSQL found: $(psql --version | head -n 1)"
fi

# Check Redis
if ! command -v redis-cli &> /dev/null; then
    print_warning "Redis CLI not found in PATH"
    echo "  If Redis is installed, you may need to add it to PATH"
    echo "  macOS: Try 'brew services list' to check if it's running"
    echo "  Or install with: 'brew install redis'"
else
    # Check if Redis is running
    if redis-cli ping &> /dev/null; then
        print_success "Redis is running"
    else
        print_warning "Redis is not running. Please start Redis server."
        echo "  Start with: 'brew services start redis' (macOS)"
    fi
fi

echo ""
echo "NOTE: You can continue setup and install PostgreSQL/Redis later."
echo "      They are only required when running the actual servers."
read -p "Press Enter to continue..."
echo ""

# =============================================================================
# Step 2: Setup Backend
# =============================================================================

print_step "Setting up backend..."

cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    print_step "Creating Python virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created"
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
if [ "$SKIP_DEPS" = false ]; then
    print_step "Installing Python dependencies..."
    pip install --quiet --upgrade pip
    pip install --quiet -r requirements.txt
    print_success "Python dependencies installed"
else
    print_warning "Skipping dependency installation"
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        print_step "Creating .env file from .env.example..."
        cp .env.example .env
        print_success ".env file created"
        print_warning "Please update .env file with your database credentials"
    else
        print_warning ".env.example not found. Please create .env manually"
    fi
fi

# =============================================================================
# Step 3: Setup Test Database
# =============================================================================

print_step "Setting up test database..."

# Load environment variables
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

DB_NAME="${DB_NAME:-forgotten_ruin}"
TEST_DB_NAME="${DB_NAME}_test"

# Create test database (only if psql is available)
if command -v psql &> /dev/null; then
    print_step "Creating test database: $TEST_DB_NAME..."
    # Try to create database (will fail if already exists, that's ok)
    psql -U postgres -c "CREATE DATABASE $TEST_DB_NAME;" 2>/dev/null || true
    print_success "Test database ready: $TEST_DB_NAME"
else
    print_warning "Skipping database creation (psql not found)"
    echo "  You'll need to create the database manually:"
    echo "  CREATE DATABASE $TEST_DB_NAME;"
fi

# =============================================================================
# Step 4: Run Migrations
# =============================================================================

print_step "Running database migrations..."

# Only run migrations if database is available
if python manage.py migrate --noinput 2>/dev/null; then
    print_success "Migrations completed"
else
    print_warning "Migrations failed (database may not be set up yet)"
    echo "  Run migrations later with: python manage.py migrate"
fi

# =============================================================================
# Step 5: Generate Test Data
# =============================================================================

if [ "$CLEAN_DATA" = true ]; then
    print_warning "Cleaning existing test data..."
    if python manage.py shell <<EOF 2>/dev/null
from tests.generate_test_data import clean_test_data
clean_test_data()
EOF
    then
        print_success "Test data cleaned"
    else
        print_warning "Could not clean test data (database may not be ready)"
    fi
fi

print_step "Generating test data..."

if python manage.py shell <<EOF 2>/dev/null
from tests.generate_test_data import generate_all_test_data
generate_all_test_data()
EOF
then
    print_success "Test data generated"
else
    print_warning "Could not generate test data (database may not be ready)"
    echo "  Generate test data later with:"
    echo "  python manage.py shell < tests/generate_test_data.py"
fi

# =============================================================================
# Step 6: Setup Frontend
# =============================================================================

print_step "Setting up frontend..."

cd ../frontend

if [ "$SKIP_DEPS" = false ]; then
    print_step "Installing Node.js dependencies..."
    npm install --silent
    print_success "Node.js dependencies installed"
else
    print_warning "Skipping frontend dependency installation"
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    print_step "Creating frontend .env file..."
    cat > .env <<EOF
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_URL=ws://localhost:8000
EOF
    print_success "Frontend .env file created"
fi

cd ..

# =============================================================================
# Step 7: Summary
# =============================================================================

echo ""
echo "============================================================================="
echo -e "${GREEN}TEST ENVIRONMENT SETUP COMPLETE!${NC}"
echo "============================================================================="
echo ""
echo "Test Accounts Created:"
echo "  Username: testuser1 | Password: TestPassword123!"
echo "  Username: testuser2 | Password: TestPassword123!"
echo "  Username: testuser3 | Password: TestPassword123!"
echo "  Username: alice     | Password: TestPassword123!"
echo "  Username: bob       | Password: TestPassword123!"
echo ""
echo "Next Steps:"
echo ""
echo "1. Start the backend server:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python manage.py runserver"
echo ""
echo "2. In a new terminal, start the frontend server:"
echo "   cd frontend"
echo "   npm start"
echo ""
echo "3. Run automated tests:"
echo "   cd backend"
echo "   pytest"
echo ""
echo "4. Run specific test suites:"
echo "   pytest tests/test_accounts.py          # Account tests"
echo "   pytest tests/test_chat_commands.py     # Chat command tests"
echo "   pytest tests/test_websocket.py         # WebSocket tests"
echo ""
echo "5. Run tests with coverage:"
echo "   pytest --cov=. --cov-report=html"
echo "   open htmlcov/index.html"
echo ""
echo "6. Manual testing:"
echo "   See tests/MANUAL_TESTS.md for detailed manual test procedures"
echo ""
echo "============================================================================="
echo ""

# Save test credentials to a file
cat > TEST_CREDENTIALS.txt <<EOF
Forgotten Ruin MUD - Test Credentials
======================================

Test Accounts:
--------------
Username: testuser1
Password: TestPassword123!
Email: test1@example.com

Username: testuser2
Password: TestPassword123!
Email: test2@example.com

Username: testuser3
Password: TestPassword123!
Email: test3@example.com

Username: alice
Password: TestPassword123!
Email: alice@example.com

Username: bob
Password: TestPassword123!
Email: bob@example.com

URLs:
-----
Frontend: http://localhost:3000
Backend API: http://localhost:8000
Admin Panel: http://localhost:8000/admin

Database:
---------
Database Name: $TEST_DB_NAME
Database User: postgres

Testing:
--------
Manual Tests: tests/MANUAL_TESTS.md
Test Plan: TEST_PLAN.md

Generated: $(date)
EOF

print_success "Test credentials saved to TEST_CREDENTIALS.txt"

exit 0
