import importlib

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """
    Scrapes a given site
    """
    help = __doc__

    def add_arguments(self, parser):
        parser.add_argument('site')

    def handle(self, **options):
        scraper_name = options['site']
        func_path = 'scrapers.{}'.format(scraper_name)
        scraper = importlib.import_module(func_path)
        scraper.scrape()
