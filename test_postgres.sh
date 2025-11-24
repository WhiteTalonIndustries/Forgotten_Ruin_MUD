#!/bin/bash

# Test runner script for Forgotten Ruin MUD with PostgreSQL
# This script sets up the environment and runs tests with PostgreSQL

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}==> Setting up PostgreSQL test environment...${NC}"

# Add PostgreSQL to PATH
export PATH="/opt/homebrew/opt/postgresql@14/bin:$PATH"

# Set environment variable to use PostgreSQL
export USE_POSTGRES_FOR_TESTS=1

# Navigate to backend directory
cd backend || exit 1

# Activate virtual environment
echo -e "${BLUE}==> Activating virtual environment...${NC}"
source venv/bin/activate || exit 1

# Check if we need to run migrations
echo -e "${BLUE}==> Checking database migrations...${NC}"
python manage.py migrate --noinput 2>&1 | head -5

# Run the specified test or all tests
if [ -z "$1" ]; then
    echo -e "${GREEN}==> Running all tests with PostgreSQL...${NC}"
    pytest tests/ -v
else
    echo -e "${GREEN}==> Running tests: $*${NC}"
    pytest "$@" -v
fi

# Capture exit code
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}==> All tests passed!${NC}"
else
    echo -e "${RED}==> Some tests failed (exit code: $EXIT_CODE)${NC}"
fi

exit $EXIT_CODE
