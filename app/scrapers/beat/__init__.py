"""
Web scraper for Beat Magazine Gig Guide
http://www.beat.com.au/gig-guide
"""
import bs4
import requests
from celery import chord
from celery.utils.log import get_task_logger
from requests.exceptions import RequestException

from scrapers import tasks

logger = get_task_logger(__name__)


def scrape():
    logger.warning('[BEATMAG] Scraping Beat Magazine')
    url = 'http://www.beat.com.au/gig-guide'
    try:
        resp = requests.get(url)
        resp.raise_for_status()
    except RequestException:
        logger.exception('[BEATMAG] Could not scrape Beat Magazine')
        return

    soup = bs4.BeautifulSoup(resp.content.decode('utf-8'), 'html.parser')

    # Marshal gig scraping tasks
    gigs = soup.find_all('a', {'href' : lambda h: h and h.startswith('/gig/')})
    seen = set()
    gig_tasks = []
    for gig in gigs:
        gig_path = gig['href']
        if gig_path in seen:
            continue

        seen.add(gig_path)
        gig_tasks.append(tasks.scrape_beat_gig.si(gig_path))

    # Marshal veneue scraping tasks
    venue_tasks = []
    venues = soup.find_all('a', {'href' : lambda h: h and h.startswith('/venue/')})
    seen = set()
    for venue in venues:
        venue_path = venue['href']
        if venue_path in seen:
            continue

        seen.add(venue_path)
        venue_tasks.append(tasks.scrape_beat_venue.si(venue_path))

    # Execute all venue tasks in parallel, then all gig tasks in parallel, then scrape genres
    gigs_then_genres = chord(gig_tasks, tasks.scrape_beat_genres.si())
    venue_then_gigs_then_genres = chord(venue_tasks, gigs_then_genres).apply_async()
