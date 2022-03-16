[![Python package](https://github.com/BenoitObelia/Monod-Crush/actions/workflows/test.yml/badge.svg)](https://github.com/BenoitObelia/Monod-Crush/actions/workflows/test.yml)

# Monod Crush

NSI project realized by [@BenoitObelia](https://github.com/BenoitObelia), [@JulesGrd](https://github.com/JulesGrd) and [@KillianTib](https://github.com/KillianTib)


## Install

### Windows and Linux

Clone the repository
```bash
git clone https://github.com/BenoitObelia/Monod-Crush
cd Monod-Crush
```

Create a virtualenv and activate it (optional)
```bash
virtualenv venv
venv/Scripts/activate # for Windows
source venv/bin/activate # for Linux
```

Install dependencies
```bash
pip install -r requirements.txt
```

or for development
```bash
pip install -r requirements-dev.txt
```

## Usage

## For development
*don't forget to activate the virtual environment if you have it installed*

### 1) setup environment variables

Linux :
```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
```

Windows (CMD) :
```cmd
set FLASK_APP=flaskr
set FLASK_ENV=development
```

Windows (PowerShell) :
```powershell
$env:FLASK_APP="flaskr"
$env:FLASK_ENV="development"
```

### 2) Setup database

```bash
flask init-db
```

You can populate the database with some data with the following command
```bash
flask populate-db
```

### 3) Run the server

Local :
```bash
flask run
```
LAN (/!\ Do not use it in a production deployment) :
```bash
flask run --host=0.0.0.0
```

Then open http://localhost:5000/

## For production

Need a wsgi server (like gunicorn)

# Test

Run with coverage report
```bash
coverage run -m pytest
coverage report
coverage html  # open htmlcov/index.html in a browser
```
