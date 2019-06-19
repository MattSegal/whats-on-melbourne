"""
Web scraper for Beat Magazine Gig Guide
http://www.beat.com.au/gig-guide
"""
import re
from datetime import datetime

import bs4
import requests
from celery import chord
from celery.utils.log import get_task_logger
from django.utils import timezone
from requests.exceptions import RequestException

from whatson.models import Event, Venue

logger = get_task_logger(__name__)

GIG_GUIDE_URL = "https://www.beat.com.au/gig-guide/"
GENRE_MAP = {
    "rock": "ROCK",
    "global": "JAZZ",
    "jazz": "JAZZ",
    "electronic": "EDM",
    "hip hop": "HIPHOP",
    "classical": "ARTS",
    "r&b": "HIPHOP",
    "punk": "ROCK",
    "metal": "ROCK",
    "pop": "EDM",
    "acoustic": "FOLK",
    "country/folk": "FOLK",
    "blues": "JAZZ",
    "soul/funk": "JAZZ",
    "experimental": "JAZZ",
}


def scrape():
    logger.warning("[BEATMAG] Scraping Beat Magazine")

    # Get all gigs from the list.
    soups = []
    count = 2
    date = datetime.strftime(timezone.now(), "%d.%m.%Y")
    soup = fetch_soup(GIG_GUIDE_URL, params={"date": date})
    soups.append(soup)

    while count < 20:
        if "No Events found." in soup.text:
            break

        soup = fetch_soup(GIG_GUIDE_URL, params={"date": date, "reload": count})
        soups.append(soup)
        count += 1

    # Extract gigs
    gig_urls = []
    for soup in soups:
        articles = soup.find_all("article", {"class": "article-card"})
        for article in articles:
            anchor = article.find("a")
            gig_url = anchor.attrs["href"]
            gig_urls.append(gig_url)

    for gig_url in gig_urls:
        try:
            scrape_gig_url(gig_url)
        except Exception as e:
            logger.exception("[BEATMAG] Failed to scrape %s", gig_url)


def scrape_gig_url(gig_url):
    logger.warning("[BEATMAG] Scraping %s", gig_url)
    gig_soup = fetch_soup(gig_url)
    gig_name = gig_soup.find("h1").text
    extracted_data = extract_gig_data(gig_soup)

    REQUIRED_FIELDS = ["location", "date", "time", "genre"]
    failed = False
    for f in REQUIRED_FIELDS:
        if not f in extracted_data:
            failed = True

    if failed:
        logger.warning("[BEATMAG]: Insufficient data %s", extracted_data)
        return

    parsed_data = parse_gig_data(extracted_data)

    venue, _ = Venue.objects.get_or_create(name=parsed_data["venue_name"])
    Event.objects.get_or_create(
        name=gig_name,
        starts_at=parsed_data["starts_at"],
        defaults={
            "artist": parsed_data["artist"] or "",
            "event_type": parsed_data["genre"],
            "price": parsed_data["price"],
            "venue": venue,
            "show_search": True,
        },
    )


def parse_gig_data(extracted_data):
    """
    Transform extracted data into usable values
    Returns a dict of parsed data
    {
        "price": 123 | None,  # None means free
        "artist": "Ekranoplans" | None, # None means unknown
        "venue_name": "Post Office Hotel",
        "genre": "EDM",
        "starts_at": build_time(2019, 6, 30, 16, 30),
    }
    """
    parsed_data = {}

    # Price: $31.40, FREE
    price_text = extracted_data.get("price", "FREE")
    if price_text == "FREE":
        parsed_data["price"] = None
    else:
        parsed_data["price"] = int(float(price_text.replace("$", "")))

    # Venue name: Howler, 7-11 Dawson St, Brunswick VIC 3056
    parsed_data["venue_name"] = extracted_data["location"].split(", ")[0]

    # Artists: THE BORNSTEIN ULTIMATUM
    lineup = extracted_data.get("lineup", "").split(", ")
    support = extracted_data.get("support", "").split(", ")
    parsed_data["artist"] = ", ".join([x for x in [*lineup, *support] if x])
    parsed_data["artist"] = parsed_data["artist"] if parsed_data["artist"] else None

    parsed_data["genre"] = None
    for beat_genre, internal_genre in GENRE_MAP.items():
        if extracted_data["genre"].lower().startswith(beat_genre):
            parsed_data["genre"] = internal_genre

    # Date: Wed 19 Jun 2019
    date_str = extracted_data["date"]

    # Time: 7pm
    period = extracted_data["time"][-2:].upper()
    if "." in extracted_data["time"]:
        hour = extracted_data["time"].split(".")[0]
        minute = extracted_data["time"].split(".")[1][:-2]
    else:
        hour = extracted_data["time"][:-2]
        minute = "00"

    if len(hour) == 1:
        hour = f"0{hour}"

    dt_str = f"{date_str} {hour} {minute} {period}"
    starts_at = datetime.strptime(dt_str, "%a %d %b %Y %I %M %p")
    parsed_data["starts_at"] = timezone.make_aware(starts_at)
    return parsed_data


def extract_gig_data(gig_soup):
    """
    Pull gig data out of gig details page HTML soup
    Returns an dict of extracted data
    {
        "location": "Post Office Hotel, 229-231 Sydney Rd, Coburg VIC 3058",
        "date": "Sun 30 Jun 2019",
        "time": "4.30pm",
        "support": "Ekranoplans",
        "price": "FREE",
        "genre": "Electronic",
    },
    """
    gig_content_tags = gig_soup.find_all("div", {"class": "article-meta-item"})
    extracted_data = {}
    for gig_content_tag in gig_content_tags:
        headline_tag = gig_content_tag.find("div", {"class": "article-meta-headline"})
        content_tag = gig_content_tag.find("div", {"class": "article-meta-content"})
        title = headline_tag.text.lower()
        content = re.sub(r"\s+", " ", content_tag.text).strip()
        extracted_data[title] = content

    return extracted_data


def fetch_soup(url, params=None):
    try:
        resp = requests.get(url, params)
        resp.raise_for_status()
        return bs4.BeautifulSoup(resp.content.decode("utf-8"), "html.parser")
    except RequestException:
        logger.exception("[BEATMAG] Could not scrape Beat Magazine")
        raise
