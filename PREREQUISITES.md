# Prerequisites Installation Guide

Before running the test setup, you need to install PostgreSQL and Redis.

## macOS Installation

### Using Homebrew (Recommended)

If you don't have Homebrew installed:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Install PostgreSQL

```bash
# Install PostgreSQL 13
brew install postgresql@13

# Start PostgreSQL
brew services start postgresql@13

# Add to PATH (add to your ~/.zshrc or ~/.bash_profile)
echo 'export PATH="/opt/homebrew/opt/postgresql@13/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Verify installation
psql --version
```

### Install Redis

```bash
# Install Redis
brew install redis

# Start Redis
brew services start redis

# Verify Redis is running
redis-cli ping  # Should return PONG
```

### Create Database

```bash
# Create the database user and database
psql postgres

# In psql:
CREATE DATABASE forgotten_ruin;
CREATE DATABASE forgotten_ruin_test;
\q
```

## Linux Installation

### Ubuntu/Debian

```bash
# Update package list
sudo apt update

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Install Redis
sudo apt install redis-server

# Start services
sudo systemctl start postgresql
sudo systemctl start redis-server

# Enable services to start on boot
sudo systemctl enable postgresql
sudo systemctl enable redis-server

# Create database
sudo -u postgres psql
CREATE DATABASE forgotten_ruin;
CREATE DATABASE forgotten_ruin_test;
\q
```

### Fedora/RHEL/CentOS

```bash
# Install PostgreSQL
sudo dnf install postgresql postgresql-server

# Install Redis
sudo dnf install redis

# Initialize PostgreSQL database
sudo postgresql-setup --initdb

# Start services
sudo systemctl start postgresql
sudo systemctl start redis

# Enable services
sudo systemctl enable postgresql
sudo systemctl enable redis

# Create database
sudo -u postgres psql
CREATE DATABASE forgotten_ruin;
CREATE DATABASE forgotten_ruin_test;
\q
```

## Windows Installation

### PostgreSQL

1. Download PostgreSQL installer from https://www.postgresql.org/download/windows/
2. Run the installer
3. Remember the password you set for the postgres user
4. Add PostgreSQL bin directory to PATH:
   - Default location: `C:\Program Files\PostgreSQL\13\bin`

### Redis

1. Download Redis for Windows from https://github.com/microsoftarchive/redis/releases
2. Install and run as a Windows service
3. Or use WSL2 (Windows Subsystem for Linux) and follow Linux instructions

## Verify Installation

After installation, verify everything is working:

```bash
# Check PostgreSQL
psql --version
psql -U postgres -c "SELECT version();"

# Check Redis
redis-cli ping  # Should return PONG

# Check Python
python3 --version  # Should be 3.10 or higher

# Check Node.js
node --version  # Should be 16 or higher
```

## Troubleshooting

### PostgreSQL not in PATH (macOS)

If `psql` command is not found after installation:

```bash
# For Intel Macs
echo 'export PATH="/usr/local/opt/postgresql@13/bin:$PATH"' >> ~/.zshrc

# For Apple Silicon (M1/M2) Macs
echo 'export PATH="/opt/homebrew/opt/postgresql@13/bin:$PATH"' >> ~/.zshrc

# Reload shell
source ~/.zshrc
```

### PostgreSQL Connection Error

If you get "role does not exist" error:

```bash
# Create your user
createdb $(whoami)
```

### Redis Not Starting

```bash
# macOS - Check if running
brew services list

# macOS - Restart Redis
brew services restart redis

# Linux - Check status
sudo systemctl status redis

# Linux - Restart
sudo systemctl restart redis
```

### Port Already in Use

If PostgreSQL or Redis ports are already in use:

```bash
# Check what's using port 5432 (PostgreSQL)
lsof -i :5432

# Check what's using port 6379 (Redis)
lsof -i :6379

# Kill the process if needed (use PID from lsof output)
kill -9 <PID>
```

## Next Steps

Once all prerequisites are installed, you can run the setup script:

```bash
./scripts/setup_test_environment.sh
```

Or follow the manual setup in TESTING_QUICK_START.md
