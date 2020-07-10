# To install:
Create a python [venv](https://docs.python.org/3/tutorial/venv.html) for this project to keep all the packages separate and at the correct version.
`python3 -m venv .venv`
To use this newly created venv you must activate it every time you want to start using it.  
For windows use:
`.venv\Scripts\activate.bat`
For Unix or MacOS use:
`source .venv/bin/activate`
Update pip to the newest version with the following command:
`pip install --upgrade pip`
Next install all the requirements for this project by running:
`pip install -r requirements.txt`
This project uses [MariaDB](https://mariadb.org/download/) as the database, which needs to be installed.

# Linting
In order to check the code for errors, we use flake8, which also gives some style enforcement. The configuration for flake8 can be found in the tox.ini file. Additional plugins installed for flake8 give support for django specific linting, pep8 compliant naming and correct sorting of imports. To install flake8 and all plugins run:
`pip install flake8 flake8-django pep8-naming flake8-isort`
To make sure everything is checked before creating a commit, install pre-commit and install the git hook.
`pip install pre-commit`
`pre-commit install`

# Formatting
To keep code nicely formatted we use [black](https://github.com/psf/black) to enforce the code style. The configuration for black can be found in the pyproject.toml file. To install black run:
`pip install black`
To make sure everything is formatted correctly before creating a commit, assumming pre-commit is already installed, run:
`pre-commit install`

# Testing
For testing purposes we use Tox. To install run:
`pip install tox`
To run all tests run:
`tox`

# Development:
To run the project for development purposes run the following command:
`python manage.py runserver`