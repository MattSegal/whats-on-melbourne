"""
Web scraper for Beat Magazine Gig Guide
http://www.beat.com.au/gig-guide
from whatson.scrapers.beat import scrape;scrape()
"""
import bs4
import requests
from celery import shared_task
from celery.utils.log import get_task_logger
from django.utils import timezone
from requests.exceptions import RequestException

from ..models import Venue, Event
from ..celery import app

logger = get_task_logger(__name__)


def scrape():
    logger.warning('Scraping Beat Magazine')
    url = 'http://www.beat.com.au/gig-guide'
    resp = requests.get(url)
    resp.raise_for_status()
    soup = bs4.BeautifulSoup(resp.content.decode('utf-8'), 'html.parser')

    # Gigs
    gigs = soup.find_all('a', {'href' : lambda h: h and h.startswith('/gig/')})
    seen = set()
    for gig in gigs:
        gig_path = gig['href']
        if gig_path in seen:
            continue

        seen.add(gig_path)
        try:
            scrape_gig_page(gig_path)
        except RequestException:
            logger.exception('Could not scrape gig %s', gig_path)

    # Venues
    venues = soup.find_all('a', {'href' : lambda h: h and h.startswith('/venue/')})
    seen = set()
    for venue in venues:
        venue_path = venue['href']
        if venue_path in seen:
            continue

        seen.add(venue_path)
        try:
            venue_data = scrape_venue_page(venue_path)
        except RequestException:
            logger.exception('Could not scrape venue %s', venue_path)


def scrape_gig_page(gig_path):
    logger.warning('Scraping gig: %s', gig_path)
    gig_data = {}
    gig_resp = requests.get('http://www.beat.com.au' + gig_path)
    gig_resp.raise_for_status()
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
    else:
        gig_data['event_type'] = 'MUSIC'

    Event.objects.get_or_create(
        name=gig_data['name'],
        starts_at=gig_data['starts_at'],
        defaults=gig_data
    )


def scrape_venue_page(venue_path):
    logger.warning('Scraping venue: %s', venue_path)
    venue_data = {}
    venue_resp = requests.get('http://www.beat.com.au' + venue_path)
    venue_resp.raise_for_status()
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

    Venue.objects.update_or_create(
        name=name,
        defaults={
            'website': website
        }
    )
