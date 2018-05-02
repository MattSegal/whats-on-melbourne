"""
Web scraper for Beat Magazine Gig Guide
http://www.beat.com.au/gig-guide
from whatson.scrapers.beat import scrape;scrape()
"""
from django.utils import timezone

import bs4
import requests

from ..models import Venue, Event


def scrape():
    url = 'http://www.beat.com.au/gig-guide'
    resp = requests.get(url)
    resp.raise_for_status()
    soup = bs4.BeautifulSoup(resp.content.decode('utf-8'), 'html.parser')
    gigs = soup.select('div[class*="archive_node-summary-wrapper"]')

    for gig in gigs:
        name_tag = gig.select('[class*="archive_node-summary-title"]')[0]
        gig_details_url = name_tag.find('a')['href']
        try:
            gig_data = scrape_gig_page(gig_details_url)
            gig_data['venue'], _ = Venue.objects.get_or_create(name=gig_data['venue'])
            Event.objects.get_or_create(
                name=gig_data['name'],
                starts_at=gig_data['starts_at'],
                defaults=gig_data
            )
        except Exception as e:
            print(e)
            pass


def scrape_gig_page(gig_details_path):
    gig_data = {}
    gig_resp = requests.get('http://www.beat.com.au' + gig_details_path)
    gig_resp.raise_for_status()
    soup = bs4.BeautifulSoup(gig_resp.content.decode('utf-8'), 'html.parser')

    # Read gig name
    name_el = soup.find('h2', {'class': 'title'})
    gig_data['name'] = name_el.text

    # Read venue name
    venue_el = soup.find('a', {'href' : lambda h: h and h.startswith('/venue/')})
    gig_data['venue'] = venue_el.text

    # Read artist name
    artist_el = soup.find('a', {'href' : lambda h: h and h.startswith('/category/gig-artist/')})
    gig_data['artist'] = artist_el.text

    # Read time
    time_el = soup.find('span', {'class': 'date-display-single'})
    time_str = time_el.text
    # Datetime format is '2 May 2018 @ 7:00pm'
    format_str = '%d %B %Y @ %I:%M%p'
    starts_at = timezone.datetime.strptime(time_str, format_str)
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
            pass

    return gig_data
