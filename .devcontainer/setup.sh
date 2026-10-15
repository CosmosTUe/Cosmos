#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# This script is run inside the devcontainer after it is created.
echo "------------------------------------------------"
echo "SETTING UP DEVELOPMENT ENVIRONMENT..."
echo "------------------------------------------------"

# The project folder is mounted from the host with a different owner; tell git it's safe
git config --global --add safe.directory /workspace

# Disable git file mode checking to avoid permission issues inside the container
git config core.fileMode false

# 1. Handle secrets.json

# Copy dev.secrets.json to /etc/secrets.json inside the container (required by secret_settings.py)
echo "Copying dev.secrets.json to /etc/secrets.json..."
sudo cp dev.secrets.json /etc/secrets.json
sudo chmod 644 /etc/secrets.json

# 2. Install Python dependencies using Pipenv

# Remove existing virtual environment if it exists
rm -rf .venv

echo "Installing Python dependencies..."
pipenv sync --dev  # exactly the locked versions; 'install' could rewrite Pipfile.lock

# 3. Install NPM packages
echo "Installing NPM packages..."
if ! npm ci; then
    echo "npm ci failed. Trying npm install..."
    npm install --no-save --package-lock=false
fi

# 4. Migrate the database
echo "Running database migrations..."
pipenv run python manage.py migrate

# 5. Create default superuser
# Default superuser credentials: username: admin, password: admin
echo "Creating default superuser (admin / admin)..."
pipenv run python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin')"

echo "------------------------------------------------"
echo "SETUP FINISHED!"
echo "To start the server, go to the 'Run and Debug' tab in VS Code and start the 'Docker: Django Runserver' configuration."
echo "Website: http://localhost:8000   Emails the site sends: http://localhost:8025"
echo "------------------------------------------------"