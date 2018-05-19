import bs4
import requests
from celery.utils.log import get_task_logger
from django.utils import timezone
from requests.exceptions import RequestException

from whatson.models import Venue, Event

logger = get_task_logger(__name__)


def scrape_gig_page(gig_path):
    logger.warning('Scraping gig: %s', gig_path)
    gig_data = {}
    try:
        gig_resp = requests.get('http://www.beat.com.au' + gig_path)
        gig_resp.raise_for_status()
    except RequestException:
        logger.exception('Could not scrape gig %s', gig_path)
        return

    soup = bs4.BeautifulSoup(gig_resp.content.decode('utf-8'), 'html.parser')

    # Read gig name
    name_el = soup.find('h2', {'class': 'title'})
    try:
        gig_data['name'] = name_el.text
    except AttributeError:
        logger.error('Could not parse name for %s', gig_path)
        return

    # Read venue name
    venue_el = soup.find('a', {'href' : lambda h: h and h.startswith('/venue/')})
    try:
        gig_data['venue'] = venue_el.text
    except AttributeError:
        logger.error('Could not parse venue for %s', gig_path)
        return

    # Read artist name
    artist_el = soup.find('a', {'href' : lambda h: h and h.startswith('/category/gig-artist/')})
    try:
        gig_data['artist'] = artist_el.text
    except AttributeError:
        logger.error('Could not artist name for %s', gig_path)
        return

    # Read time
    time_el = soup.find('span', {'class': 'date-display-single'})
    time_str = time_el.text
    # Datetime format is '2 May 2018 @ 7:00pm'
    format_str = '%d %B %Y @ %I:%M%p'
    try:
        starts_at = timezone.datetime.strptime(time_str, format_str)
    except ValueError:
        logger.error('Could not parse time %s for %s', time_str, gig_path)
        return

    starts_at = timezone.make_aware(starts_at)
    gig_data['starts_at'] = starts_at

    # Read price
    gig_data['price'] = None
    price_header_el = soup.find('h5', {'class': 'price'})
    if price_header_el:
        price_data_el = price_header_el.next_sibling
        price_data_text = price_data_el.text.replace('$', '')
        try:
            gig_data['price'] = int(price_data_text)
        except ValueError:
            logger.warning('Could not parse price %s for %s', price_data_text, gig_path)

    gig_data['venue'], _ = Venue.objects.get_or_create(name=gig_data['venue'])

    if 'trivia' in gig_data['name'].lower():
        gig_data['event_type'] = 'TRIVIA'


    gig_data['show_search'] = True
    Event.objects.get_or_create(
        name=gig_data['name'],
        starts_at=gig_data['starts_at'],
        defaults=gig_data
    )
