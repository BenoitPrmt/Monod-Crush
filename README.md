[![Python package](https://github.com/BenoitObelia/Monod-Crush/actions/workflows/test.yml/badge.svg)](https://github.com/BenoitObelia/Monod-Crush/actions/workflows/test.yml)

# ♥️ Monod Crush

Website is available at [monodcrush.fr](https://monodcrush.fr)<br>
NSI project realized by [@BenoitObelia](https://github.com/BenoitObelia), [@JulesGrd](https://github.com/JulesGrd) and [@KillianTib](https://github.com/KillianTib)

## 📥 Install

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

## 🧰 Usage

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

## ⚒️ Test

Run with coverage report
```bash
coverage run -m pytest
coverage report
coverage html  # open htmlcov/index.html in a browser
```

## ✅ For production

```bash
sudo apt-get update
sudo apt-get full-upgrade

cd ~/.ssh
ssh-keygen -o -t rsa -C "email@example.com"
cat id_rsa.pub # paste this in GitHub

cd
git clone git@github.com:BenoitObelia/Monod-Crush.git
cd Monod-Crush/

sudo apt install python3-pip
sudo pip install virtualenv # need sudo for add virtualenv to PATH
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn

export FLASK_APP=flaskr
flask init-db
flask populate-db

# run gunicorn
```
