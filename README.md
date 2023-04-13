[![Python package](https://github.com/BenoitObelia/Monod-Crush/actions/workflows/django.yml/badge.svg)](https://github.com/BenoitObelia/Monod-Crush/actions/workflows/test.yml)

# ♥️ Monod Crush

Website is available at [monodcrush.fr](https://monodcrush.fr)

NSI project realized by [@BenoitPrmt](https://github.com/BenoitPrmt), [@JulesGrd](https://github.com/JulesGrd) and [@KillianTib](https://github.com/KillianTib)


Project documentation : [PROJECT.md](./PROJECT.md)

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

## 🧰 Usage

## For development
*don't forget to activate the virtual environment if you have it installed*

### 1) Setup database

```bash
python manage.py migrate
```

### 2) Run the server

Local :
```bash
python manage.py runserver
```
Then open http://localhost:5000/ in your browser

---
LAN (/!\ Do not use it in a production deployment) :
```bash
python manage.py runserver 0.0.0.0:5000
```
Then open http://<your_ip>:5000/ in your browser

## ✅ For production

use gunicorn with a reverse proxy server like Nginx
