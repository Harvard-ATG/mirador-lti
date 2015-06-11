# django-lti-skeleton

This is a skeleton django project that imports [django-app-lti](https://github.com/Harvard-ATG/django-app-lti) and provides a single view function in **myapp**.

## Quickstart

```sh
$ pip install -r requirements.txt
$ cd skeleton/
$ ./manage.py syncdb && ./manage.py migrate
$ ./manage.py runserver
```

1. Go to [http://localhost:8000/lti/config](http://localhost:8000/lti/config) 
2. Add the tool to Canvas 
3. Launch the tool in Canvas
4. If it worked, you should see a "Welcome to my app" message
