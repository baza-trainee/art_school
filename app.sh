sleep 2

alembic upgrade head

gunicorn -c gunicorn.conf.py src.main:app
