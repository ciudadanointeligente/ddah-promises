from django.core.management.base import BaseCommand, CommandError
import codecs
from promises.csv_loader import CsvProcessor
import django
from distutils.version import StrictVersion


class Command(BaseCommand):
    help = 'Imports a csv file into promises'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', nargs='+', type=str)

    def handle(self, *args, **options):
        if not StrictVersion(django.get_version()) < StrictVersion("1.8"):
            file_name = options['csv_file'][0]
        else:
            file_name = args[0]
        file_ = codecs.open(file_name)
        processor = CsvProcessor(file_)
        processor.work()
