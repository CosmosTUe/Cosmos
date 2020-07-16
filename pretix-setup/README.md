# Pretix setup

Pretix is the chosen ticketing software for the Cosmos website. It is a Django instance separate from the actual website
and hence require its own set of steps to get everything fully running.

## Dependencies

- cron - periodic task manager
- MariaDB 10.2.7+, latest 10.4.13 - database (Assumed to be installed from installing Django instance for server)
- nginx - HTTP(S) reverse proxy (Setup steps to be added)
- redis - caching, only for development, remove in production

## Setup

Based on the following tutorial: [link](https://docs.pretix.eu/en/latest/admin/installation/manual_smallscale.html)

1. Install dependencies

- MariaDB
```bash
# Arch Linux
yay -S mariadb
# Debian/Ubuntu
sudo apt install mariadb-server
sudo mysql_secure_installation
```

- Redis
```bash
# Arch Linux
yay -S redis
# Debian/Ubuntu
sudo apt update
sudo apt install redis-server
sudo systemctl enable redis
sudo systemctl start redis
```

3. Create new unprivileged user:
```bash
# Arch Linux
useradd pretix --home /var/pretix
# Debian/Ubuntu
adduser pretix --disabled-password --home /var/pretix
```

4. Create a database and database user

```bash
mysql -u root -p
```
```mariadb
CREATE DATABASE pretix DEFAULT CHARACTER SET utf8mb4 DEFAULT COLLATE utf8mb4_unicode_ci;
GRANT ALL PRIVILEGES ON pretix.* TO cosmos_website_tester@localhost;
```

5. Pretix configuration as `root`

```bash
# Run all the following as root!
sudo su
mkdir /etc/pretix
cp pretix.cfg /etc/pretix/pretix.cfg
chown -R pretix:pretix /etc/pretix/
chmod 0600 /etc/pretix/pretix.cfg
```

5. Pretix configuration as `pretix` user

```bash
# Change user to pretix
sudo su pretix
# Setup Python environment
python3 -m venv /var/pretix/venv
source /var/pretix/venv/bin/activate
pip3 install -U pip setuptools wheel
pip install "pretix[mysql]" pretix-mollie gunicorn

### Setup pretix ###
# Create data directory
mkdir -p /var/pretix/data/media
# Compile static files, translation data and create database structure
# Re-run when installing a new plugin!
python -m pretix migrate
python -m pretix rebuild
```

6. Start pretix as a service

```bash
# Run all the following as root!
sudo su
cp pretix-web.service /etc/systemd/system/pretix-web.service
cp pretix-worker.service /etc/systemd/system/pretix-worker.service
systemctl daemon-reload
systemctl enable pretix-web pretix-worker
systemctl start pretix-web pretix-worker
```

7. Login to pretix via [localhost:8345](http://localhost:8345)
```
default username: admin@localhost
default password: admin
```

8. Configure pretix via the web interface

- Create a new `Organizer account` with the umbrella name 'COSMOS' (TODO consider how to handle different years of COSMOS board)
- Create a new `Team` inside of the 'COSMOS' `Organizer account` for each committee in the association
- Add Mollie details in [`Global settings > Settings`](http://localhost:8345/control/global/settings/)
- Set up token-based authentication: https://docs.pretix.eu/en/latest/api/tokenauth.html#rest-tokenauth