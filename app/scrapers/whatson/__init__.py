"""
Web scraper for Whatson Melbourne
https://whatson.melbourne.vic.gov.au/
"""
import re

import bs4
import requests
from celery import chord
from celery.utils.log import get_task_logger
from django.utils import timezone
from requests.exceptions import RequestException

from scrapers import tasks
from whatson.models import Venue, Event
from whatson.tasks import geocode_venue

logger = get_task_logger(__name__)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
}


# script type="text/javascript">
# TODO: Consider reverse Geocoding
# addMarker(-37.8084088943931, 144.96346578623, "Quiz Night - Live Audience", "Centre", "<h4>Quiz Night - Live Audience</h4><br /> Swanston Street  Street <br> RMIT tram stop (outside Boost Juice)<br>Melbourne 3000");</script>


def scrape():
    logger.warning('Scraping Whatson Melbourne Comedy')
    url = 'https://whatson.melbourne.vic.gov.au/Whatson/ArtsandCulture/Comedy/Pages/Comedy.aspx'
    now = timezone.now()
    today_str = timezone.datetime.strftime(now, '%Y-%m-%d')
    params = {
        'scope': 'Whatson',
        'TMFromDate': today_str,
        'TMToDate': today_str,
    }
    try:
        resp = requests.get(url, params=params, headers=HEADERS)
        resp.raise_for_status()
    except RequestException:
        logger.exception('Could not scrape 888 Poker')
        return

    soup = bs4.BeautifulSoup(resp.content.decode('utf-8'), 'html.parser')
    results = soup.find('div', {'class': 'results'})
    details = results.find_all('div', {'class': 'detail'})

    if not details:
        logger.exception('No search results found for Melbourne Whatson')
        return

    detail_urls = []
    base_url = 'https://whatson.melbourne.vic.gov.au'
    for detail in details:
        detail_anchor = detail.find('a')
        detail_urls.append(base_url + detail_anchor['href'])


    for url in detail_urls:
        logger.warning('Scraping Melbourne whatson event: %s', url)
        venue_data = {}
        event_data = {}
        event_data['details_url'] = url

        try:
            resp = requests.get(url, headers=HEADERS)
            resp.raise_for_status()
        except RequestException:
            logger.exception('Could not scrape event %s from Melbourne whatson', url)
            return

        soup = bs4.BeautifulSoup(resp.content.decode('utf-8'), 'html5lib')

        # Get name of venue
        detail_div = soup.find('div', {'class': 'EventDetailContent'})
        location_title = detail_div.find('h2')
        location = location_title.next_sibling
        location_parts = [c for c in location.children]
        try:
            venue_name = location_parts[0].text
        except AttributeError:
            venue_name = str(location_parts[0])

        venue_data['name'] = venue_name.strip().split(',')[0]

        # Get lat/long of venue
        scripts = soup.find_all('script', {'type': 'text/javascript'})
        for script in scripts:
            contents = script.text.strip()
            if contents.startswith('addMarker'):
                params = contents[10:].split(',')
                venue_data['latitude'] = float(params[0])
                venue_data['longitude'] = float(params[1])

        # Get name of event
        title = soup.find('div', {'class': 'titleBanner'})
        event_data['name'] = title.text.strip()

        # Get the starttime of the event
        day_of_week = timezone.datetime.strftime(now, '%a')
        regex = re.compile(day_of_week + r': (?P<hour>\d{1,2}).?(?P<min>\d{0,2})(?P<noon>(pm|am))')
        match = re.search(regex, detail_div.text)
        results = match.groupdict()
        hour = int(results['hour'])
        hour += 0 if results['noon'].lower() == 'am' else 12
        min_str = results.get('min')
        minute = int(min_str) if min_str else 0
        starts_at = timezone.datetime(
            year=now.year,
            day=now.day,
            month=now.month,
            hour=hour,
            minute=minute,
        )
        print(venue_data['name'], hour, minute)
        event_data['starts_at'] = timezone.make_aware(starts_at)

        # Location
        # Contact details
        # Dates and times
        # Price
        # Bookings
        # How to get there
        # Features
        # Accessibility

        # titles = detail_div.find_all('div', {'class': 'noindex'})
        # for title in titles:
        #     if title.text.strip() == 'Price':
        #         print('Price: ', title.next_sibling.text)


        # import pdb;pdb.set_trace()

        venue, created = Venue.objects.update_or_create(
            name=venue_data['name'],
            defaults={
                'latitude': venue_data['latitude'],
                'longitude': venue_data['longitude'],
            }
        )
        # Fuck it - no prices or artists for now
        event_data['price'] = 0
        Event.objects.update_or_create(
            name=event_data['name'],
            starts_at=event_data['starts_at'],
            defaults={
                'details_url': event_data['details_url'],
                'event_type': 'COMEDY',
                'price': event_data['price'],
                'venue': venue,
            }
        )
