from boto.s3.connection import S3Connection
from boto.s3.key import Key
from .models import IsiteImages, LTIResourceImages, LTIResourceCollections

import logging
import json

def assign_images(resource_id, keyword, **kwargs):
    '''
    Assigns images to a resource given a keyword.
    Optionally specify topic_id to map resource images to (keyword, topic_id).
    '''
    log = kwargs.get('logger', logging.getLogger(__file__))
    topic_id = kwargs.get('topic_id', None)

    filter_by = {'isite_keyword': keyword}
    if topic_id is not None:
        filter_by['isite_topic_id'] = topic_id

    lti_resource = LTIResourceImages.get_lti_resource(resource_id)
    log.info('Found LTI resource: %s' % lti_resource)

    LTIResourceImages.objects.filter(resource=lti_resource).delete()
    log.info('Deleted all images assigned to LTI resource: %s' % lti_resource)

    isite_images = IsiteImages.objects.filter(**filter_by)
    log.info('Preparing to assign images: %s' % len(isite_images))
    
    collection_map = {}
    resource_image_records = []
    for n, isite_image in enumerate(isite_images):
        topic_id = isite_image.isite_topic_id
        collection_label = isite_image.isite_topic_title
        if topic_id in collection_map:
            collection = collection_map[topic_id]
        else:
            collection = LTIResourceCollections(sort_order=len(collection_map.keys()), label=collection_label)
            collection.save()
            collection_map[topic_id] = collection
            log.info('Created collection %s' % collection)
        resource_image_records.append(LTIResourceImages(resource=lti_resource, collection=collection, isite_image=isite_image))

    LTIResourceImages.objects.bulk_create(resource_image_records)
    log.info('Assigned %s images to resource: %s' % (len(resource_image_records), lti_resource))


class IsiteImageDataLoader:
    ''''
    The IsiteImageDataLoader class is responsible for loading a list of images that
    have been migrated from the old iSite Slide Tool to an S3 bucket. This class is
    only concerned with the *metadata* about the images, not the images themselves.
    
    This class collaborates with the iSiteImageDataSource to interface with S3 and
    return image metadata in a usable format.

    Usage:
        
        loader = IsiteImageDataLoader({
            'key': 'foo',
            'secret': 'bar',
            'bucket': 'bucket-name',
        })
        loader.delete_all()
        loader.load_all(dry_run=False)
    '''
    
    def __init__(self, aws_credentials, logger=None):
        if 'bucket' not in aws_credentials:
            raise Exception("missing 'bucket' key in aws_credentials")
        self.s3_bucket = aws_credentials['bucket']
        self.can_save = False
        if logger is None:
            self.log = logging.getLogger(__file__)
        else:
            self.log = logger
        self.isite_ds = iSiteImageDataSource(aws_credentials, logger)

    def delete_all(self):
        '''Deletes all image objects.'''
        IsiteImages.objects.all().delete()
        return self
    
    def load_all(self, **kwargs):
        '''Loads metadata for all image objects.'''
        dry_run = kwargs.get('dry_run', False)
        self.can_save = not dry_run

        items = self.isite_ds.get_bucket_as_dict()

        for keyword in items:
            for topic_id in items[keyword]:
                self.load_data_for(keyword, topic_id)

        return self
    
    def load_data_for(self, keyword, topic_id):
        '''Loads data for a given iSite keyword and topic ID.'''
        d = self.isite_ds.get_data_file(keyword, topic_id)
        is_valid, errors = self.validate_data_for(keyword, topic_id, d)
        if not is_valid:
            self.log.info("Skipping load for data file of keyword: %s topic: %s errors: %s" %(keyword, topic_id, errors))
            return self

        site_title = d['site_title']
        topic_title = d['topic_title']
        for n, file_item in enumerate(d['files'], start=1):
            self.log.info("Loading file item #%s: %s" % (n, file_item.values()))
            
            s3_bucket = None
            s3_key = None
            if file_item['type'] == 'file':
                s3_key = file_item['url']
                s3_bucket = self.s3_bucket

            file_description = ""
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
                'isite_site_title': site_title,
                'isite_topic_title': topic_title,
                'isite_topic_id': topic_id,
                'isite_keyword': keyword,
                's3_key': s3_key,
                's3_bucket': s3_bucket,
            })
    
    def validate_data_for(self, keyword, topic_id, data):
        '''Validates the data.json for a given keyword and topic ID.'''
        is_valid, errors = (True, [])
        expected_data_keys = set(['site_title', 'topic_title', 'keyword', 'topic_id'])
        given_data_keys = set(data.keys())

       
        if expected_data_keys.issubset(given_data_keys):
            self.log.debug("Validated data file for (%s, %s) contains expected keys: %s" % (keyword, topic_id, expected_data_keys))
        else:
            error_str = "Invalid data file for (%s, %s) - missing expected keys: %s" %  (keyword, topic_id, expected_data_keys.difference(given_data_keys))
            self.log.error(error_str)
            errors.append(error_str)
            is_valid = False

        return is_valid, errors
    
    def save_file_item(self, item_dict):
        '''Saves an image item to the database.'''
        item_exists = IsiteImages.objects.filter(**item_dict).exists()
        if item_exists:
            self.log.info("Item already exists -- did not save")
        else:
            isite_image_id = None
            if self.can_save:
                isite_image = IsiteImages(**item_dict)
                isite_image.save()
                isite_image_id = isite_image.id
            self.log.info("Saved item %s" % isite_image_id)

        return self


class iSiteImageDataSource:
    '''
    The iSiteImageDataSource class is responsbile for knowing how to interface with
    the S3 bucket that contains migrated iSite Slide Tool images. The bucket is
    structured such that the keys are tuples like this: (keyword, topic_id, item).
    
    As a tree, the bucket looks like this:
    
    keyword/
        topic_id/
            data.json
            image1.jpg
            image2.jpg
            ...
            imageN.jpg
    
    Note that in iSites, the keyword uniquely identified the site and the topic_id
    uniquely identified the instance of the iSite Slide Tool. Each (keyword, topic_id)
    tuple should have a data.json file that acts as a manifest for the images that
    were in the iSite topic. The manifest contains the metadata for the images.
    '''
    def __init__(self, aws_credentials, logger=None):
        self.conn = None
        self.bucket = None
        if logger is None:
            self.log = logging.getLogger(__file__)
        else:
            self.log = logger

        self.connect_to_s3(aws_credentials)       

    def connect_to_s3(self, aws_credentials):
        '''Connects to the S3 bucket given AWS credentials for the key, secret.'''
        errors = []
        for k in ('key', 'secret'):
            if k not in aws_credentials:
                errors.append("missing key %s" % k)
            elif aws_credentials[k] is None or aws_credentials[k] == "":
                errors.append("key is empty: %s" % k)
        if len(errors) > 0:
            raise Exception("Error(s) connecting to S3: " + ", ".join(errors))

        self.conn = S3Connection(aws_credentials['key'], aws_credentials['secret'])
        self.bucket = self.conn.get_bucket(aws_credentials['bucket'])
        self.log.debug("Connected to S3 bucket %s via AWS key %s" % (aws_credentials['bucket'], aws_credentials['key']))

    def get_bucket_as_dict(self):
        '''Returns the bucket as a dictionary structure rather than a list of strings (i.e. bucket keys).'''
        d = {}
        self.log.debug("Iterating over bucket keys and converting to dict...")
        for bucket_key in self.bucket.list():
            self.log.debug("S3 bucket key: %s" % bucket_key.name)
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
        '''Returns the data.json content for a given keyword and topic_id.'''
        k = Key(self.bucket)
        k.key = "/".join([keyword, topic_id, "data.json"])
        data_str = k.get_contents_as_string()
        return json.loads(data_str)
