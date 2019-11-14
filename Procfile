web: gunicorn fforg.wsgi
worker: celery -A fforg worker -l ${CELERY_LOG_LEVEL:-info} --autoscale=8,2
beat: celery -A fforg worker -l ${CELERY_LOG_LEVEL:-info} --beat --autoscale=4,1
release: python manage.py migrate
