install: pip install -r requirements.txt
web: python manage.py migrate && gunicorn backend.wsgi --log-file -