Steps
=====

$ python3 -m venv venv
$ . venv/bin/activate
$ pip install -r requirements.txt
$ ./manage.py migrate
$ ./manage.py createsuperuser
$ ./manage.py runserver

Go to http://127.0.0.1:8000 and see the viewflow in action!
