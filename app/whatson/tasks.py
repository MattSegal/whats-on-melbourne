import importlib

import requests
from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from django.utils import timezone
from redis import Redis

from .models import Venue, Source

logger = get_task_logger(__name__)
THIRTY_MINUTES = 60 * 30

@shared_task
def run_scrapers():
    logger.warning('Running scrapers')
    now = timezone.localtime()
    today_naieve = timezone.datetime(year=now.year, month=now.month, day=now.day)
    today = timezone.make_aware(today_naieve)
    sources = Source.objects.exclude(scraped_at__gte=today).all()
    for source in sources:
        redis = Redis(host=settings.REDIS_HOST)
        cache_key = 'scrape-{}'.format(source.name)
        runtime = redis.get(cache_key)

        if not runtime:
            logger.warning('Dispatching %s scraper', source.name)
            run_scraper.delay(source.pk)
            logger.warning('Finished dispatching %s scraper', source.name)
        else:
            logger.warning('Scraper %s is already running: %s', source.name, runtime)

    logger.warning('Finished running scrapers')


@shared_task
def run_scraper(source_pk):
    source = Source.objects.get(pk=source_pk)

    redis = Redis(host=settings.REDIS_HOST)
    cache_key = 'scrape-{}'.format(source.name)
    now = timezone.localtime()
    result = redis.set(cache_key, str(now), ex=THIRTY_MINUTES)
    logger.warning('Running %s scraper', source.name)

    func_path = 'scrapers.{}'.format(source.scraper)
    scraper = importlib.import_module(func_path)
    scraper.scrape()

    source.scraped_at = now
    source.save()
    redis.delete(cache_key)

    logger.warning('Finished running %s scraper', source.name)
    geocode_venues.delay()


@shared_task
def geocode_venues():
    logger.warning('Geocoding Venues')
    venues = Venue.objects.all()
    for venue in venues:
        if not (venue.address and venue.latitude and venue.longitude):
            geocode_venue.delay(venue.pk)

    logger.warning('Finished geocoding Venues')


@shared_task
def geocode_venue(venue_pk):
    venue = Venue.objects.get(pk=venue_pk)

    if venue.address:
        name = '{}, {}'.format(venue.name, venue.address)
    else:
        name = '{}, {}'.format(venue.name, 'Melbourne')

    logger.warning('Geocoding Venue[%s] with name %s', venue_pk, name)
    lat, lng, address = geocode_name(name)
    venue.latitude = lat
    venue.longitude = lng
    venue.address = address
    venue.save()
    logger.warning('Finished geocoding Venue[%s]', venue_pk)


def geocode_name(name):
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {
        'address': name,
        'key': settings.GEOCODING_API_KEY,
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()
    if 'status' not in data or not data['status'] == 'OK':
        raise ValueError('Bad geocoding status: {}'.format(data))

    lat = data['results'][0]['geometry']['location']['lat']
    lng = data['results'][0]['geometry']['location']['lng']
    address = data['results'][0]['formatted_address']
    return lat, lng, address
