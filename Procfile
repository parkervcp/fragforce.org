web: gunicorn fforg.wsgi
worker: celery -A fforg worker -l info --autoscale=8,2
beat: celery -A fforg worker -l info --beat --autoscale=2,1
release: python manage.py migrate
