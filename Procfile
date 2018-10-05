web: gunicorn fforg.wsgi
worker: celery -A fforg worker -l info
beat: celery -A fforg worker -l info --beat
release: python manage.py migrate
