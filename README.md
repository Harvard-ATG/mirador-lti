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

## CLI Tools

**Load iSite Image Metadata from S3**:

```sh
$ ./manage.py load_isite_images isites-slide-data --aws-key="mykey" --aws-secret="mysecret"
```
