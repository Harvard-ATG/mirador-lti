[![Build Status](https://travis-ci.org/Harvard-ATG/mirador-lti.svg?branch=master)](https://travis-ci.org/Harvard-ATG/mirador-lti)

# Mirador LTI Tool

## Quickstart

```sh
$ pip install -r mirador_lti/requirements/local.txt
$ ./manage.py syncdb && ./manage.py migrate
$ ./manage.py runserver
```

1. Go to [http://localhost:8000/lti/config](http://localhost:8000/lti/config) 
2. Add the tool to Canvas 
3. Launch the tool in Canvas
4. If it worked, you should see a "Welcome to my app" message

## Technical Documentation

See the [wiki](https://github.com/Harvard-ATG/mirador-lti/wiki).
