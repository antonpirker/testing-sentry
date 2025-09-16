## Steps to reproduce the problem:

0. (install `uv`. Optional: set django and python version that you want to use in pyproject.toml)
1. uv sync
2. ./init.py
3. ./run-gunicorn.py or ./run-daphne.py
4. Go to `http://localhost:8000/admin/auth/user/`
5. It takes about 3-4 seconds in Django 5.x (and renders instandly in Django 4.x)
