import requests
from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings

from .models import Venue

logger = get_task_logger(__name__)


@shared_task
def geocode_venue(venue_pk):
    logger.warning('Geocoding Venue[%s]', venue_pk)
    venue = Venue.objects.get(pk=venue_pk)
    lat, lng, address = geocode_name(venue.name)
    venue.latitude = lat
    venue.longitude = lng
    venue.address = address
    venue.save()
    logger.warning('Finished geocoding Venue[%s]', venue_pk)


def geocode_name(name):
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {
        'address': '{}, Melbourne'.format(name),
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
