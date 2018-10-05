web: gunicorn fforg.wsgi
worker: celery -A fforg worker -l info -E
beat: celery -A fforg worker -l info --beat -E
release: python manage.py migrate
