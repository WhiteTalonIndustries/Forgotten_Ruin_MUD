# Testing Guide

This directory contains all testing resources for the Forgotten Ruin MUD project.

## Quick Start

### 1. Setup Test Environment

```bash
# Make scripts executable
chmod +x scripts/setup_test_environment.sh
chmod +x scripts/run_tests.sh

# Run setup script
./scripts/setup_test_environment.sh
```

### 2. Run Tests

```bash
# Run all tests
./scripts/run_tests.sh all

# Run specific test suite
./scripts/run_tests.sh accounts

# Run with coverage
./scripts/run_tests.sh coverage
```

## Test Accounts

| Username | Password | Email |
|----------|----------|-------|
| testuser1 | TestPassword123! | test1@example.com |
| testuser2 | TestPassword123! | test2@example.com |
| alice | TestPassword123! | alice@example.com |
| bob | TestPassword123! | bob@example.com |

## Documentation

- [TEST_PLAN.md](../TEST_PLAN.md) - Comprehensive test plan
- [MANUAL_TESTS.md](MANUAL_TESTS.md) - Manual testing checklist

Happy testing! 🧪✨
