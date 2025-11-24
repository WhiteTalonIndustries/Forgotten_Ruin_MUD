#!/bin/bash

###############################################################################
# Forgotten Ruin MUD - Stop Script
#
# Stops all running development servers
###############################################################################

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_msg() {
    local color=$1
    shift
    echo -e "${color}$@${NC}"
}

print_msg "$YELLOW" "🛑 Stopping Forgotten Ruin MUD servers..."
echo ""

# Kill Django/Daphne processes
if pgrep -f "python.*daphne.*server.asgi" > /dev/null; then
    print_msg "$YELLOW" "Stopping Daphne backend server..."
    pkill -f "python.*daphne.*server.asgi"
    print_msg "$GREEN" "✓ Backend stopped"
elif pgrep -f "daphne.*server.asgi:application" > /dev/null; then
    print_msg "$YELLOW" "Stopping Daphne backend server..."
    pkill -f "daphne.*server.asgi:application"
    print_msg "$GREEN" "✓ Backend stopped"
elif pgrep -f "manage.py runserver" > /dev/null; then
    print_msg "$YELLOW" "Stopping Django backend server..."
    pkill -f "manage.py runserver"
    print_msg "$GREEN" "✓ Backend stopped"
else
    print_msg "$GREEN" "✓ Backend not running"
fi

# Kill React processes
if pgrep -f "react-scripts start" > /dev/null; then
    print_msg "$YELLOW" "Stopping React frontend server..."
    pkill -f "react-scripts start"
    print_msg "$GREEN" "✓ Frontend stopped"
else
    print_msg "$GREEN" "✓ Frontend not running"
fi

# Ask about Redis
read -p "Stop Redis server? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if command -v brew &> /dev/null; then
        brew services stop redis 2>/dev/null
    else
        redis-cli shutdown 2>/dev/null
    fi
    print_msg "$GREEN" "✓ Redis stopped"
fi

echo ""
print_msg "$GREEN" "✨ All servers stopped successfully"
