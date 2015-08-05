from django.core.management.base import BaseCommand, CommandError
from mirador.models import IsiteImages

class Command(BaseCommand):
    help = 'Loads Isite Image data'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        self.stdout.write('Not implemented yet')
