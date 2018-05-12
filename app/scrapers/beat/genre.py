import bs4
import requests
from celery.utils.log import get_task_logger
from requests.exceptions import RequestException

from whatson.models import Event

logger = get_task_logger(__name__)


def scrape_genre_page():
    url = 'http://www.beat.com.au/gig-guide'
    try:
        resp = requests.get(url)
        resp.raise_for_status()
    except RequestException:
        logger.exception('Could not scrape Beat Magazine genres')
        return
    # from scrapers.beat.genre import scrape_genre_page as s;s()
    soup = bs4.BeautifulSoup(resp.content.decode('utf-8'), 'html.parser')

    for genre_classname, genre_name in GENRES.items():
        class_name = 'w-clearfix archive_node-summary-wrapper ' + genre_classname
        genre_gigs = soup.find_all('div', {'class' : class_name})
        for gig_el in genre_gigs:
            title_el = gig_el.find('h3', {'class': 'archive_node-summary-title'})
            title = None
            if title_el:
                title = title_el.text
            if not title:
                logger.error('Could not find title for genre %s', genre_name)
                continue

            try:
                event = Event.objects.get(name=title)
            except Event.DoesNotExist:
                logger.error('Could not find Event for title %s', title)
                continue

            event.event_type = genre_name
            event.save()


GENRES = {
    'trivia-gaming': 'TRIVIA',
    'jazz-soul-funk-latin-world-music': 'JAZZ',
    'arts-theatre-burlesque-markets': 'ARTS',
    'hip-hop-r-b': 'HIPHOP',
    'house-electro-trance-club-nights': 'EDM',
    'indie-rock-pop-metal-punk-covers': 'ROCK',
    'acoustic-country-blues-folk': 'FOLK',
    'comedy': 'COMEDY',
}
