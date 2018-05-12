from celery import shared_task
from celery.utils.log import get_task_logger

from .beat.gig import scrape_gig_page
from .beat.venue import scrape_venue_page

logger = get_task_logger(__name__)


@shared_task
def scrape_beat_venue(venue_path):
    scrape_venue_page(venue_path)


@shared_task
def scrape_beat_gig(gig_path):
    scrape_gig_page(gig_path)
