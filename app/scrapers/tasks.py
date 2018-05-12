from celery import shared_task
from celery.utils.log import get_task_logger

from .beat.gig import scrape_gig_page
from .beat.venue import scrape_venue_page
from .beat.genre import scrape_genre_page

logger = get_task_logger(__name__)


@shared_task
def scrape_beat_venue(venue_path):
    logger.warning('Scraping Beat Magazine venue: %s', venue_path)
    scrape_venue_page(venue_path)
    logger.warning('Done scraping Beat Magazine venue: %s', venue_path)


@shared_task
def scrape_beat_gig(gig_path):
    logger.warning('Scraping Beat Magazine gig: %s', gig_path)
    scrape_gig_page(gig_path)
    logger.warning('Done scraping Beat Magazine gig: %s', gig_path)

@shared_task
def scrape_beat_genres():
    logger.warning('Scraping Beat Magazine genres')
    scrape_genre_page()
    logger.warning('Done scraping Beat Magazine genres')
