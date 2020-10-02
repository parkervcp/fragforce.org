web: gunicorn fforg.wsgi
worker: celery -A fforg worker -l "${CELERY_LOG_LEVEL:-INFO}" --autoscale=8,2
beat: celery -A fforg worker -l "${CELERY_LOG_LEVEL:-INFO}" --beat --autoscale=4,1
release: python manage.py migrate
