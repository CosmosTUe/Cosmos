#!/bin/bash

# This script is run inside the devcontainer after it is created.
echo "------------------------------------------------"
echo "SETTING UP DEVELOPMENT ENVIRONMENT..."
echo "------------------------------------------------"

# Disable git file mode checking to avoid permission issues inside the container
git config core.fileMode false

# 1. Create and configure secrets.json for Docker environment

if [ ! -f secrets.json ]; then
    echo "Creating secrets.json from template..."
    cp secrets.json.template secrets.json
    
    echo "Configuring secrets.json for Docker environment..."

    # Rewrite database USER: github_actions -> cosmos_website_tester
    sed -i 's/"USER": "github_actions"/"USER": "cosmos_website_tester"/g' secrets.json
    
    # Rewrite database HOST: localhost -> db
    sed -i 's/"HOST": "localhost"/"HOST": "db"/g' secrets.json
    
    # Rewrite Redis URL: redis://localhost -> redis://redis
    sed -i 's/redis:\/\/localhost/redis:\/\/redis/g' secrets.json
    
    # Modifying ALLOWED_HOSTS: [] -> ["localhost", "127.0.0.1", "0.0.0.0"]
    # This allows accessing teh server from the host machine
    sed -i 's/"ALLOWED_HOSTS": \[\]/"ALLOWED_HOSTS": \["localhost", "127.0.0.1", "0.0.0.0"\]/g' secrets.json
    
    echo "Docker configuration applied!"
fi

# Copy secrets.json to /etc inside the container (required by secret_settings.py)
echo "Copying secrets.json to /etc/secrets.json..."
cp secrets.json /etc/secrets.json
# Cleaning up secrets.json from the project directory
rm secrets.json

# 2. Install Python dependencies using Pipenv

echo "Installing Python dependencies..."
pipenv install --system --dev

# 3. Install NPM packages
echo "Installing NPM packages..."
npm ci

# 4. Migrate the database
echo "Running database migrations..."
python manage.py migrate

# 5. Create default superuser
# Default superuser credentials: username: admin, password: admin
echo "Creating default superuser (admin / admin)..."
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin')"

echo "------------------------------------------------"
echo "SETUP FINISHED!"
echo "To start the server, go to the 'Run and Debug' tab in VS Code and start the 'Docker: Django Runserver' configuration."
echo "------------------------------------------------"