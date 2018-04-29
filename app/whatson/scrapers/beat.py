"""
Web scraper for Beat Magazine Gig Guide
http://www.beat.com.au/gig-guide
"""
import bs4
import requests

def scrape():
    url = 'http://www.beat.com.au/gig-guide'
    resp = requests.get(url)
    resp.raise_for_status()
    soup = bs4.BeautifulSoup(resp.content.decode('utf-8'), 'html.parser')
    gigs = soup.select('div[class*="archive_node-summary-wrapper"]')

    for gig in gigs:
        name_tag = gig.select('[class*="archive_node-summary-title"]')[0]
        gig_details_url = name_tag.find('a')['href']
        gig_resp = requests.get('http://www.beat.com.au' + gig_details_url)
        gig_resp.raise_for_status()
        gig_soup = bs4.BeautifulSoup(gig_resp.content.decode('utf-8'), 'html.parser')
        name = gig_soup.find('h2', {'class': 'title'}).text
        # http://www.beat.com.au/gig/sunday-session-134

# from whatson.scrapers.beat import scrape;scrape()
