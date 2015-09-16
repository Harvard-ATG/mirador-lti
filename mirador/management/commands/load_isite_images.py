from django.core.management.base import BaseCommand, CommandError
from mirador.isite import IsiteImageDataLoader, iSiteImageDataSource
import logging

class Command(BaseCommand):
    help = 'Refresh database of available images exported from iSite Slide Tools'

    def add_arguments(self, parser):
        parser.add_argument('s3_bucket')
        parser.add_argument('--aws-key', help="AWS Key", required=True)
        parser.add_argument('--aws-secret', help="AWS Secret", required=True)
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
        logger = logging.getLogger(__file__)
        ch = logging.StreamHandler()
        logger.addHandler(ch)
        logger.setLevel(logging.DEBUG)

        loader = IsiteImageDataLoader({
            'key': options['aws_key'],
            'secret': options['aws_secret'],
            'bucket': options['s3_bucket'],
        }, logger)

        if options['reload']:
            loader.delete_all()
        
        loader.load_all(dry_run=options['dry-run'])

