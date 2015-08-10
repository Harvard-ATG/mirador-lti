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

**Load iSite image metadata from S3 into the application**:

```sh
$ ./manage.py load_isite_images [s3_bucket] --aws-key=[aws_key] --aws-secret=[aws_secret]
```

**Assign iSite image(s) by keyword and topic (optional) to a course**:

```sh
$ ./manage.py assign_isite_images [course_id] [keyword] --topic_id [topic_id]
```
