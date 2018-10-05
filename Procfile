web: gunicorn fforg.wsgi
worker: celery -A fforg worker -l info --autoscale=8,2
beat: celery -A fforg worker -l info --beat --autoscale=0,0
release: python manage.py migrate
