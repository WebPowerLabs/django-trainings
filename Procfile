web: gunicorn --pythonpath="$PWD/dtf" config.wsgi:application
worker: python dtf/manage.py celeryd -E -B -c1 -l INFO