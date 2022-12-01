python manage.py collectstatic --no-input
gunicorn school.wsgi:application -c gunicorn.conf.py