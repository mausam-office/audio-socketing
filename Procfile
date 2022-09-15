release: python manage.py migrate
web: daphne AudioAppMain.asgi:application --port $PORT --bind 0.0.0.0 -v2
web: gunicorn AudioAppMain.wsgi --log-file -
AudioAppMainworker: python manage.py runworker --settings=AudioAppMain.settings -v2