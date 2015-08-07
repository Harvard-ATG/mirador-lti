from django.core.management.base import BaseCommand, CommandError
from mirador.models import IsiteImages
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import json

class Command(BaseCommand):
    help = 'Loads isite image data'

    def add_arguments(self, parser):
        parser.add_argument('s3_bucket')
        parser.add_argument('--aws-key', help="AWS Key")
        parser.add_argument('--aws-secret', help="AWS Secret")
        parser.add_argument('--reload',
            dest="reload",
            default=False,
            action="store_true",
            help="Reloads the data from scratch (defaults to incremental)")
        parser.add_argument('--dry-run',
            dest="dry-run",
            default=False,
            action="store_true",
            help="Displays the images that will be loaded without loading htem")
        

    def handle(self, *args, **options):
        print options
        loader = IsiteImageDataLoader({
            'key': options['aws_key'],
            'secret': options['aws_secret'],
            'bucket': options['s3_bucket'],
        })

        if options['reload']:
            loader.delete_all()
        
        loader.can_save_data(not options['dry-run'])
        
        loader.load_all()

class IsiteImageDataLoader:
    def __init__(self, aws_credentials):
        self.isite_ds = iSiteImageDataSource(aws_credentials)
        self.s3_bucket = aws_credentials['bucket']
        self.can_save = False
    
    def can_save_data(self, can_save):
        self.can_save = can_save
    
    def delete_all(self):
        IsiteImages.objects.all().delete()
        return self
    
    def load_all(self):
        items = self.isite_ds.get_bucket_as_dict()

        for keyword in items:
            for topic_id in items[keyword]:
                self.load_data_for(keyword, topic_id)

        return self
    
    def load_data_for(self, keyword, topic_id):
        d = self.isite_ds.get_data_file(keyword, topic_id)
        is_valid, errors = self.validate_data_for(keyword, topic_id, d)
        if not is_valid:
            print "Skipping load for data file of keyword: %s topic: %s errors: %s" %(keyword, topic_id, errors)
            return self

        site_title = d['site_title']
        topic_title = d['topic_title']
        for n, file_item in enumerate(d['files'], start=1):
            print "Loading file item #%s: %s" % (n, file_item.values())
            
            s3_bucket = None
            s3_key = None
            if file_item['type'] == 'file':
                s3_key = file_item['url']
                s3_bucket = self.s3_bucket

            file_description = "%s - %s" % (site_title, topic_title)
            if 'Description' in file_item:
                file_description = file_item['Description']
                
            file_title = file_item['filename']
            if 'Title' in file_item:
                file_title = file_item['Title']

            self.save_file_item({
                'isite_file_type': file_item['type'],
                'isite_file_name': file_item['filename'],
                'isite_file_url': file_item['url'],
                'isite_file_title': file_title,
                'isite_file_description': file_description,
                'isite_topic_id': topic_id,
                'isite_keyword': keyword,
                's3_key': s3_key,
                's3_bucket': s3_bucket,
            })
    
    def validate_data_for(self, keyword, topic_id, data):
        is_valid, errors = (True, [])
        expected_data_keys = set(['site_title', 'topic_title', 'keyword', 'topic_id'])
        given_data_keys = set(data.keys())

        if not expected_data_keys.issubset(given_data_keys):
            errors.append("Data missing expected keys: %s" % expected_data_keys.difference(given_data_keys))
            is_valid = False

        return is_valid, errors
    
    def save_file_item(self, item_dict):
        item_exists = IsiteImages.objects.filter(**item_dict).exists()
        if item_exists:
            print "Skipping save because it already exists in the database"
        else:
            isite_image_id = None
            if self.can_save:
                isite_image = IsiteImages(**item_dict)
                isite_image.save()
                isite_image_id = isite_image.id
            print "Saved item %s" % isite_image_id

        return self


class iSiteImageDataSource:
    def __init__(self, aws_credentials):
        self.conn = None
        self.bucket = None
        self.connect_to_s3(aws_credentials)

    def connect_to_s3(self, aws_credentials):
        self.conn = S3Connection(aws_credentials['key'], aws_credentials['secret'])
        self.bucket = self.conn.get_bucket(aws_credentials['bucket'])

    def get_bucket_as_dict(self):
        d = {}
        for bucket_key in self.bucket.list():
            (keyword, topic_id, item) = [None, None, None]
            parts = bucket_key.name.split('/', 3)
            if len(parts) == 3:
                (keyword, topic_id, item) = parts
            elif len(parts) == 2:
                (keyword, topic_id) = parts
            elif len(parts) == 1:
                (keyword,) = parts
            else:
                continue
            
            if keyword not in d:
                d[keyword] = {}
            if topic_id is not None and topic_id != "" and topic_id not in d[keyword]:
                d[keyword][topic_id] = []
            if item is not None and item not in d[keyword][topic_id]:
                d[keyword][topic_id].append(item)
    
        return d
    
    def get_data_file(self, keyword, topic_id):
        k = Key(self.bucket)
        k.key = "/".join([keyword, topic_id, "data.json"])
        data_str = k.get_contents_as_string()
        return json.loads(data_str)