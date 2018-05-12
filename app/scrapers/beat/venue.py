import bs4
import requests
from celery.utils.log import get_task_logger
from requests.exceptions import RequestException

from whatson.models import Venue
from whatson.tasks import geocode_venue

logger = get_task_logger(__name__)


def scrape_venue_page(venue_path):
    venue_data = {}
    try:
        venue_resp = requests.get('http://www.beat.com.au' + venue_path)
        venue_resp.raise_for_status()
    except RequestException:
        logger.exception('Could not scrape venue %s', venue_path)
        return

    soup = bs4.BeautifulSoup(venue_resp.content.decode('utf-8'), 'html.parser')

    # Read venue name
    name_el = soup.find('h1', {'class': 'article_title'})
    try:
        name = name_el.text
    except AttributeError:
        logger.error('Could not parse name for %s', venue_path)
        return

    # Read venue website
    website = None
    try:
        website_header_el = soup.find('h5', {'class': 'price'})
        website_el = website_header_el.find('a')
        website = website_el['href']
    except (AttributeError, TypeError):
        logger.error('Could not parse website for %s', venue_path)

    if not website:
        return

    venue, created = Venue.objects.update_or_create(
        name=name,
        defaults={
            'website': website
        }
    )
    if created:
        geocode_venue.delay(venue.pk)
