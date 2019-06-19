"""
Web scraper for 888 Poker League
http://www.888pl.com.au
"""
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


# THIS DOESN'T WORK
def scrape():
    logger.warning("[888] Scraping 888 Poker")
    url = "http://www.888pl.com.au/Index.asp"
    params = {
        "Action": "Setup",
        "TID": 2,
        "nDay": 0,
        "nWeek": 0,
        "RegionID": 0,
        "OID": "",
        "SuburbPC": "",
    }
    data = {"State": "Victoria_1", "RegionID2": 0}

    try:
        resp = requests.post(url, data=data, params=params, headers=HEADERS)
        resp.raise_for_status()
    except RequestException:
        logger.exception("[888] Could not scrape 888 Poker")
        return

    soup = bs4.BeautifulSoup(resp.content.decode("utf-8"), "html.parser")
    results_tab = soup.find(id="TabContent_1_1")
    if not results_tab:
        logger.exception("[888] No search results found for 888 Poker")
        return

    even_event_rows = list(results_tab.find_all("tr", {"class": "EventsRow_Even"}))
    odd_event_rows = list(results_tab.find_all("tr", {"class": "EventsRow_Odd"}))
    event_rows = even_event_rows + odd_event_rows

    event_data = []
    base_url = "http://www.888pl.com.au/"
    for row_el in event_rows:
        children = [el for el in row_el.children if el != "\n"]
        event_data.append(
            {
                "date": children[1].text,
                "venue_name": children[2].text,
                "venue_url": base_url + children[2].find("a")["href"],
                "event_title": children[3].text,
                "suburb": children[4].text,
                "start_time": children[5].text,
                "entry": children[6].text,
            }
        )

    venues = []
    urls = set()
    for event in event_data:
        if event["venue_url"] in urls:
            continue

        urls.add(event["venue_url"])
        venues.append(
            {
                "url": event["venue_url"],
                "name": event["venue_name"],
                "suburb": event["suburb"],
            }
        )

    events = []
    for event in event_data:
        date = " ".join(event["date"].split(" ")[1:])
        year = str(timezone.now().year)
        datetime_str = year + " " + date + " " + event["start_time"]
        # 2018 15 Jun 18:30
        format_str = "%Y %d %b %H:%M"
        starts_at = timezone.datetime.strptime(datetime_str, format_str)
        starts_at = timezone.make_aware(starts_at)
        price_str = event["entry"].replace("$", "").replace("Free", "0")
        price = int(float(price_str))
        events.append(
            {
                "name": event["event_title"],
                "starts_at": starts_at,
                "price": price,
                "venue_url": event["venue_url"],
            }
        )

    venue_lookup = {}
    for venue in venues:
        url = venue["url"]
        logger.warning("[888] Scraping 888 poker venue: %s", url)

        try:
            resp = requests.get(url, headers=HEADERS)
            resp.raise_for_status()
        except RequestException:
            logger.exception("[888] Could not scrape venue %s from 888 Poker", url)
            return

        soup = bs4.BeautifulSoup(resp.content.decode("utf-8"), "html.parser")
        tab = soup.find(id="TabContent_1_2")
        outer_table = tab.find("table")
        inner_table = outer_table.find("table")

        address = ""
        keys = ("Address", "Suburb", "Region", "State", "Post Code")
        for row in inner_table.find_all("tr"):
            try:
                text = row.text.replace("\n", "").strip()
            except AttributeError:
                continue

            if ":" in text:
                key, value = text.split(":")
                for k in keys:
                    if text.startswith(k):
                        address += value + " "

        address = address.strip()
        venue, created = Venue.objects.update_or_create(
            name=venue["name"],
            defaults={"website": venue["url"], "address": address or venue["suburb"]},
        )
        if created:
            geocode_venue.delay(venue.pk)

        venue_lookup[venue.website] = venue

    for event in events:
        venue = venue_lookup[event["venue_url"]]
        Event.objects.update_or_create(
            name=event["name"],
            starts_at=event["starts_at"],
            defaults={
                "event_type": "POKER",
                "artist": "Pub Poker",
                "price": event["price"],
                "venue": venue,
            },
        )
