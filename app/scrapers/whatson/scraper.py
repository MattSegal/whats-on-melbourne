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

from whatson.models import Event, Venue
from whatson.tasks import geocode_venue

logger = get_task_logger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
}

genres = [
    {"type": "COMEDY", "path": "/Whatson/ArtsandCulture/Comedy/Pages/Comedy.aspx"},
    {
        "type": "ARTS",
        "path": "/Whatson/ArtsandCulture/TheatreandShows/Pages/TheatreandShows.aspx",
    },
]


def scrape():
    base_url = "https://whatson.melbourne.vic.gov.au"
    for genre in genres:
        logger.warning("[WHATSON] Scraping Whatson Melbourne %s", genre["type"])
        url = base_url + genre["path"]
        now = timezone.localtime()
        today_str = now.strftime("%Y-%m-%d")
        params = {"scope": "Whatson", "TMFromDate": today_str, "TMToDate": today_str}
        try:
            resp = requests.get(url, params=params, headers=HEADERS)
            resp.raise_for_status()
        except RequestException:
            logger.exception("[WHATSON] Could not scrape 888 Poker")
            return

        soup = bs4.BeautifulSoup(resp.content.decode("utf-8"), "html.parser")
        results = soup.find("div", {"class": "results"})
        details = results.find_all("div", {"class": "detail"})

        if not details:
            logger.exception(
                "[WHATSON] No search results found for Melbourne Whatson %s",
                genre["type"],
            )
            return

        detail_urls = []

        for detail in details:
            detail_anchor = detail.find("a")
            detail_urls.append(base_url + detail_anchor["href"])

        for url in detail_urls:
            logger.warning("[WHATSON] Scraping Melbourne whatson event: %s", url)
            venue_data = {}
            event_data = {}
            event_data["details_url"] = url

            try:
                resp = requests.get(url, headers=HEADERS)
                resp.raise_for_status()
            except RequestException:
                logger.exception(
                    "[WHATSON] Could not scrape event %s from Melbourne whatson", url
                )
                return

            soup = bs4.BeautifulSoup(resp.content.decode("utf-8"), "html5lib")

            # Get name of venue
            detail_div = soup.find("div", {"class": "EventDetailContent"})
            location_title = detail_div.find("h2")
            location = location_title.next_sibling
            location_parts = [c for c in location.children]
            try:
                venue_name = location_parts[0].text
            except AttributeError:
                venue_name = str(location_parts[0])

            venue_data["name"] = venue_name.strip().split(",")[0]

            # Get lat/long of venue
            scripts = soup.find_all("script", {"type": "text/javascript"})
            for script in scripts:
                contents = script.text.strip()
                if contents.startswith("addMarker"):
                    params = contents[10:].split(",")
                    venue_data["latitude"] = float(params[0])
                    venue_data["longitude"] = float(params[1])

            # Get name of event
            title = soup.find("div", {"class": "titleBanner"})
            event_data["name"] = title.text.strip()

            # Get the starttime of the event
            day_of_week = timezone.datetime.strftime(now, "%a")
            regex = re.compile(
                day_of_week + r": (?P<hour>\d{1,2}).?(?P<min>\d{0,2})(?P<noon>(pm|am))"
            )
            match = re.search(regex, detail_div.text)
            results = match.groupdict()
            hour = int(results["hour"])
            hour += 0 if results["noon"].lower() == "am" else 12
            min_str = results.get("min")
            minute = int(min_str) if min_str else 0
            starts_at = timezone.datetime(
                year=now.year, day=now.day, month=now.month, hour=hour, minute=minute
            )
            event_data["starts_at"] = timezone.make_aware(starts_at)

            venue, created = Venue.objects.update_or_create(
                name=venue_data["name"],
                defaults={
                    "latitude": venue_data["latitude"],
                    "longitude": venue_data["longitude"],
                },
            )
            # Fuck it - no prices or artists for now
            event_data["price"] = 0
            Event.objects.update_or_create(
                name=event_data["name"],
                starts_at=event_data["starts_at"],
                defaults={
                    "details_url": event_data["details_url"],
                    "event_type": genre["type"],
                    "price": event_data["price"],
                    "venue": venue,
                },
            )
