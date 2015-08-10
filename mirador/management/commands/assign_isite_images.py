from django.core.management.base import BaseCommand, CommandError
from mirador.isite import assign_images
import logging

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('course_id', help="LTI Course ID") 
        parser.add_argument('keyword', help="iSite keyword")
        parser.add_argument('--topic_id', help="iSite topic_id")

    def handle(self, *args, **options):
        logger = logging.getLogger(__file__)
        ch = logging.StreamHandler()
        logger.addHandler(ch)
        logger.setLevel(logging.DEBUG)

        assign_images(options['course_id'], options['keyword'], topic_id=options['topic_id'], logger=logger)