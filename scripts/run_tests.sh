#!/bin/bash

# =============================================================================
# Test Runner Script
# =============================================================================
# Quick script to run different test suites
#
# Usage:
#   ./scripts/run_tests.sh [test-type]
#
# Test Types:
#   all         - Run all tests (default)
#   unit        - Run only unit tests
#   integration - Run only integration tests
#   accounts    - Run account-related tests
#   chat        - Run chat-related tests
#   websocket   - Run WebSocket tests
#   coverage    - Run tests with coverage report
#   quick       - Run quick smoke tests
# =============================================================================

set -e

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# Navigate to project root (parent of scripts directory)
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

TEST_TYPE="${1:-all}"

print_step() {
    echo -e "\n${BLUE}==>${NC} ${GREEN}$1${NC}"
}

print_error() {
    echo -e "${RED}ERROR: $1${NC}"
}

# Navigate to project root, then backend
cd "$PROJECT_ROOT"

if [ ! -d "backend" ]; then
    print_error "Backend directory not found!"
    echo "Make sure you're in the Forgotten_Ruin_MUD project directory"
    exit 1
fi

cd backend

# Activate virtual environment
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    print_error "Virtual environment not found!"
    echo "Please run setup first: ./scripts/setup_test_environment.sh"
    exit 1
fi

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    print_error "pytest not found!"
    echo "Install dependencies: pip install -r requirements.txt"
    exit 1
fi

# Run tests based on type
case $TEST_TYPE in
    all)
        print_step "Running all tests..."
        pytest -v
        ;;
    unit)
        print_step "Running unit tests..."
        pytest -v tests/test_accounts.py tests/test_chat_commands.py
        ;;
    integration)
        print_step "Running integration tests..."
        pytest -v tests/test_websocket.py
        ;;
    accounts)
        print_step "Running account tests..."
        pytest -v tests/test_accounts.py
        ;;
    chat)
        print_step "Running chat command tests..."
        pytest -v tests/test_chat_commands.py
        ;;
    websocket)
        print_step "Running WebSocket tests..."
        pytest -v tests/test_websocket.py
        ;;
    coverage)
        print_step "Running tests with coverage..."
        pytest --cov=. --cov-report=html --cov-report=term
        echo ""
        echo "Coverage report generated in htmlcov/index.html"
        ;;
    quick)
        print_step "Running quick smoke tests..."
        pytest -v -k "test_valid_registration or test_valid_login or test_connect_with_valid_token"
        ;;
    *)
        echo "Unknown test type: $TEST_TYPE"
        echo ""
        echo "Available test types:"
        echo "  all         - Run all tests"
        echo "  unit        - Run only unit tests"
        echo "  integration - Run integration tests"
        echo "  accounts    - Run account tests"
        echo "  chat        - Run chat tests"
        echo "  websocket   - Run WebSocket tests"
        echo "  coverage    - Run with coverage report"
        echo "  quick       - Run quick smoke tests"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}✓ Tests complete!${NC}"
