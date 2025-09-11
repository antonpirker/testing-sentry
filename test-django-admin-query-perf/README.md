## Steps to reproduce the problem:

0. (set django and python version that you want to use in pyproject.toml)
1. uv sync
2. ./init.py
3. ./run-gunicorn.py or ./run-daphne.py
4. Go to `127.0.0.1:8000/admin`
5. See how long it loads :-)
