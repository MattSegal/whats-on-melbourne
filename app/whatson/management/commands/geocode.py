import importlib

from django.core.management.base import BaseCommand
from whatson.tasks import geocode_venues

class Command(BaseCommand):
    """
    Scrapes a given site
    """
    help = __doc__

    def handle(self, **options):
        geocode_venues.delay()
