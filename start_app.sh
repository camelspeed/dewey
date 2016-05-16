cd /webapps/dewey
gunicorn dewey:app -p dewey.pid -b 0.0.0.0:80 -D