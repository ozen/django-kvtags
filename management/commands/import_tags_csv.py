from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError
from tagging.models import Tag
from tagging.utils import import_tags_csv
import unicodecsv


class Command(BaseCommand):
    """Provides command interface to tagging.utils.import_tags_csv"""
    args = '<csv_file>'
    help = 'Imports tags from csv file to database'

    def handle(self, *args, **options):
        with open(args[0], 'rb') as csvfile:
            import_tags_csv(csvfile)
