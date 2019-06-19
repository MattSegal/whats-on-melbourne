import bs4
import pytest
from django.utils import timezone

from scrapers.beat.scraper import extract_gig_data, parse_gig_data


def test_extract_gig_data():
    for data in TEST_DATA:
        soup = bs4.BeautifulSoup(data["html"], "html.parser")
        extracted = extract_gig_data(soup)
        assert extracted == data["extracted_data"]


def test_parse_gig_data():
    for data in TEST_DATA:
        extracted = data["extracted_data"]
        parsed = parse_gig_data(extracted)
        assert parsed == data["parsed_data"]


def build_time(year, month, day, hour, minute):
    return timezone.make_aware(timezone.datetime(year, month, day, hour, minute))


TEST_DATA = [
    {
        "html": """<div class="article-meta-item">
            <div class="article-meta-headline">LOCATION</div>
            <div class="article-meta-content">
            <div>
            <a href="https://www.beat.com.au/directory/caravan-music-club/">Caravan Music Club</a>, 
				</div>
            <div>
										1 Victor Rd, Bentleigh East VIC 3165		</div>
            </div>
            </div>, <div class="article-meta-item">
            <div class="article-meta-headline">DATE</div>
            <div class="article-meta-content">
				Sun 30 Jun 2019			</div>
            </div>, <div class="article-meta-item">
            <div class="article-meta-headline">Time</div>
            <div class="article-meta-content">
            <div>2.30pm</div>
            </div>
            </div>, <div class="article-meta-item">
            <div class="article-meta-headline">LINEUP</div>
            <div class="article-meta-content">
				Atlanta Coogan			</div>
            </div>, <div class="article-meta-item">
            <div class="article-meta-headline">PRICE</div>
            <div class="article-meta-content">
				$23.00			</div>
            </div>, <div class="article-meta-item">
            <div class="article-meta-headline">Genre</div>
            <div class="article-meta-content">
            <div class="breadcrumb">
            <a href="https://www.beat.com.au/genre/rock/">Rock</a> </div>
            </div>
            </div>""",
        "parsed_data": {
            "price": 23,
            "venue_name": "Caravan Music Club",
            "artist": "Atlanta Coogan",
            "genre": "ROCK",
            "starts_at": build_time(2019, 6, 30, 14, 30),
        },
        "extracted_data": {
            "location": "Caravan Music Club, 1 Victor Rd, Bentleigh East VIC 3165",
            "date": "Sun 30 Jun 2019",
            "time": "2.30pm",
            "lineup": "Atlanta Coogan",
            "price": "$23.00",
            "genre": "Rock",
        },
    },
    {
        "html": """<div class="article-meta-item">
                <div class="article-meta-headline">LOCATION</div>
                <div class="article-meta-content">
                <div>
                <a href="https://www.beat.com.au/directory/whole-lotta-love/">Whole Lotta Love</a>,
                                </div>
                <div>
                                                        524 Lygon St, Brunswick East VIC 3057		</div>
                </div>
                </div>, <div class="article-meta-item">
                <div class="article-meta-headline">DATE</div>
                <div class="article-meta-content">
                                Sun 30 Jun 2019			</div>
                </div>, <div class="article-meta-item">
                <div class="article-meta-headline">Time</div>
                <div class="article-meta-content">
                <div>7pm</div>
                </div>
                </div>, <div class="article-meta-item">
                <div class="article-meta-headline">LINEUP</div>
                <div class="article-meta-content">
                                Filth Dimension			</div>
                </div>, <div class="article-meta-item">
                <div class="article-meta-headline">Support</div>
                <div class="article-meta-content">
                                Criminal Blonde, Charlie Rebel			</div>
                </div>, <div class="article-meta-item">
                <div class="article-meta-headline">PRICE</div>
                <div class="article-meta-content">
                                FREE			</div>
                </div>, <div class="article-meta-item">
                <div class="article-meta-headline">Genre</div>
                <div class="article-meta-content">
                <div class="breadcrumb">
                <a href="https://www.beat.com.au/genre/punk/">Punk</a> </div>
                </div>
                </div>""",
        "parsed_data": {
            "price": None,
            "venue_name": "Whole Lotta Love",
            "artist": "Filth Dimension, Criminal Blonde, Charlie Rebel",
            "genre": "ROCK",
            "starts_at": build_time(2019, 6, 30, 19, 00),
        },
        "extracted_data": {
            "location": "Whole Lotta Love, 524 Lygon St, Brunswick East VIC 3057",
            "date": "Sun 30 Jun 2019",
            "time": "7pm",
            "lineup": "Filth Dimension",
            "support": "Criminal Blonde, Charlie Rebel",
            "price": "FREE",
            "genre": "Punk",
        },
    },
    {
        "html": """<div class="article-meta-item">            <div class="article-meta-headline">LOCATION</div>
    <div class="article-meta-content">
    <div>
    <a href="https://www.beat.com.au/directory/post-office-hotel/">Post Office Hotel</a>,
    				</div>
    <div>
    										229-231 Sydney Rd, Coburg VIC 3058		</div>
    </div>
    </div>, <div class="article-meta-item">
    <div class="article-meta-headline">DATE</div>
    <div class="article-meta-content">
    				Sun 30 Jun 2019			</div>
    </div>, <div class="article-meta-item">
    <div class="article-meta-headline">Time</div>
    <div class="article-meta-content">
    <div>4.30pm</div>
    </div>
    </div>, <div class="article-meta-item">
    <div class="article-meta-headline">Support</div>
    <div class="article-meta-content">
    				Ekranoplans			</div>
    </div>, <div class="article-meta-item">
    <div class="article-meta-headline">PRICE</div>
    <div class="article-meta-content">
    				FREE			</div>
    </div>, <div class="article-meta-item">
    <div class="article-meta-headline">Genre</div>
    <div class="article-meta-content">
    <div class="breadcrumb">
    <a href="https://www.beat.com.au/genre/electronic/">Electronic</a> </div>
    </div>
    </div>""",
        "parsed_data": {
            "price": None,
            "venue_name": "Post Office Hotel",
            "artist": "Ekranoplans",
            "genre": "EDM",
            "starts_at": build_time(2019, 6, 30, 16, 30),
        },
        "extracted_data": {
            "location": "Post Office Hotel, 229-231 Sydney Rd, Coburg VIC 3058",
            "date": "Sun 30 Jun 2019",
            "time": "4.30pm",
            "support": "Ekranoplans",
            "price": "FREE",
            "genre": "Electronic",
        },
    },
    {
        "html": """<div class="article-meta-item">
    <div class="article-meta-headline">LOCATION</div>
    <div class="article-meta-content">
    <div>
    <a href="https://www.beat.com.au/directory/side-street-lounge/">Side Street Lounge</a>,
    				</div>
    <div>
    										501-505 Main Street, Mordialloc VIC 3195	</div>
    </div>
    </div>, <div class="article-meta-item">
    <div class="article-meta-headline">DATE</div>
    <div class="article-meta-content">
    				Sun 30 Jun 2019			</div>
    </div>, <div class="article-meta-item">
    <div class="article-meta-headline">Time</div>
    <div class="article-meta-content">
    <div>6pm</div>
    </div>
    </div>, <div class="article-meta-item">
    <div class="article-meta-headline">LINEUP</div>
    <div class="article-meta-content">
    				Andy Murphy			</div>
    </div>, <div class="article-meta-item">
    <div class="article-meta-headline">PRICE</div>
    <div class="article-meta-content">
    				$10.00			</div>
    </div>, <div class="article-meta-item">
    <div class="article-meta-headline">Genre</div>
    <div class="article-meta-content">
    <div class="breadcrumb">
    <a href="https://www.beat.com.au/genre/electronic/">Electronic</a> </div>
    </div>
    </div>""",
        "parsed_data": {
            "price": 10,
            "venue_name": "Side Street Lounge",
            "artist": "Andy Murphy",
            "genre": "EDM",
            "starts_at": build_time(2019, 6, 30, 18, 00),
        },
        "extracted_data": {
            "location": "Side Street Lounge, 501-505 Main Street, Mordialloc VIC 3195",
            "date": "Sun 30 Jun 2019",
            "time": "6pm",
            "lineup": "Andy Murphy",
            "price": "$10.00",
            "genre": "Electronic",
        },
    },
    {
        "html": """<div class="article-meta-item">
    <div class="article-meta-headline">LOCATION</div>
    <div class="article-meta-content">
    <div>
    <a href="https://www.beat.com.au/directory/the-quiet-man-irish-pub/">The Quiet Man Irish Pub</a>,
    				</div>
    <div>
    										271 Racecourse Rd, Flemington VIC 3031		</div>
    </div>
    </div>, <div class="article-meta-item">
    <div class="article-meta-headline">DATE</div>
    <div class="article-meta-content">
    				Sun 30 Jun 2019			</div>
    </div>, <div class="article-meta-item">
    <div class="article-meta-headline">Time</div>
    <div class="article-meta-content">
    <div>6pm</div>
    </div>
    </div>, <div class="article-meta-item">
    <div class="article-meta-headline">PRICE</div>
    <div class="article-meta-content">
    				FREE			</div>
    </div>, <div class="article-meta-item">
    <div class="article-meta-headline">Genre</div>
    <div class="article-meta-content">
    <div class="breadcrumb">
    <a href="https://www.beat.com.au/genre/country-folk/">Country/Folk</a> </div>
    </div>
    </div>""",
        "parsed_data": {
            "price": None,
            "venue_name": "The Quiet Man Irish Pub",
            "artist": None,
            "genre": "FOLK",
            "starts_at": build_time(2019, 6, 30, 18, 0),
        },
        "extracted_data": {
            "location": "The Quiet Man Irish Pub, 271 Racecourse Rd, Flemington VIC 3031",
            "date": "Sun 30 Jun 2019",
            "time": "6pm",
            "price": "FREE",
            "genre": "Country/Folk",
        },
    },
    {
        "html": """<div class="article-meta-item">
    <div class="article-meta-headline">LOCATION</div>
    <div class="article-meta-content">
    <div>
    <a href="https://www.beat.com.au/directory/wesley-anne/">Wesley Anne</a>,
    				</div>
    <div>
    										250 High St, Northcote VIC 3070			</div>
    </div>
    </div>, <div class="article-meta-item">
    <div class="article-meta-headline">DATE</div>
    <div class="article-meta-content">
    				Sun 30 Jun 2019			</div>
    </div>, <div class="article-meta-item">
    <div class="article-meta-headline">Time</div>
    <div class="article-meta-content">
    <div>3pm</div>
    </div>
    </div>, <div class="article-meta-item">
    <div class="article-meta-headline">PRICE</div>
    <div class="article-meta-content">
    				$10.00			</div>
    </div>, <div class="article-meta-item">
    <div class="article-meta-headline">Genre</div>
    <div class="article-meta-content">
    <div class="breadcrumb">
    <a href="https://www.beat.com.au/genre/jazz/">Jazz</a> </div>
    </div>
    </div>""",
        "parsed_data": {
            "price": 10,
            "venue_name": "Wesley Anne",
            "artist": None,
            "genre": "JAZZ",
            "starts_at": build_time(2019, 6, 30, 15, 0),
        },
        "extracted_data": {
            "location": "Wesley Anne, 250 High St, Northcote VIC 3070",
            "date": "Sun 30 Jun 2019",
            "time": "3pm",
            "price": "$10.00",
            "genre": "Jazz",
        },
    },
    {
        "html": """<div class="article-meta-item">
    <div class="article-meta-headline">LOCATION</div>
    <div class="article-meta-content">
    <div>
    <a href="https://www.beat.com.au/directory/wesley-anne/">Wesley Anne</a>,
    				</div>
    <div>
    										250 High St, Northcote VIC 3070			</div>
    </div>
    </div>, <div class="article-meta-item">
    <div class="article-meta-headline">DATE</div>
    <div class="article-meta-content">
    				Sun 30 Jun 2019			</div>
    </div>, <div class="article-meta-item">
    <div class="article-meta-headline">Time</div>
    <div class="article-meta-content">
    <div>6pm</div>
    </div>
    </div>, <div class="article-meta-item">
    <div class="article-meta-headline">PRICE</div>
    <div class="article-meta-content">
    				FREE			</div>
    </div>, <div class="article-meta-item">
    <div class="article-meta-headline">Genre</div>
    <div class="article-meta-content">
    <div class="breadcrumb">
    <a href="https://www.beat.com.au/genre/global/">Global</a> </div>
    </div>
    </div>""",
        "parsed_data": {
            "price": None,
            "venue_name": "Wesley Anne",
            "artist": None,
            "genre": "JAZZ",
            "starts_at": build_time(2019, 6, 30, 18, 00),
        },
        "extracted_data": {
            "location": "Wesley Anne, 250 High St, Northcote VIC 3070",
            "date": "Sun 30 Jun 2019",
            "time": "6pm",
            "price": "FREE",
            "genre": "Global",
        },
    },
    {
        "html": """<div class="article-meta-item">
    <div class="article-meta-headline">LOCATION</div>
    <div class="article-meta-content">
    <div>
    <a href="https://www.beat.com.au/directory/the-drunken-poet/">The Drunken Poet</a>,
    				</div>
    <div>
    										65 Peel St, West Melbourne VIC 3003		</div>
    </div>
    </div>, <div class="article-meta-item">
    <div class="article-meta-headline">DATE</div>
    <div class="article-meta-content">
    				Sun 30 Jun 2019			</div>
    </div>, <div class="article-meta-item">
    <div class="article-meta-headline">Time</div>
    <div class="article-meta-content">
    <div>4pm</div>
    </div>
    </div>, <div class="article-meta-item">
    <div class="article-meta-headline">PRICE</div>
    <div class="article-meta-content">
    				FREE			</div>
    </div>, <div class="article-meta-item">
    <div class="article-meta-headline">Genre</div>
    <div class="article-meta-content">
    <div class="breadcrumb">
    <a href="https://www.beat.com.au/genre/blues/">Blues</a> </div>
    </div>
    </div>""",
        "parsed_data": {
            "price": None,
            "venue_name": "The Drunken Poet",
            "artist": None,
            "genre": "JAZZ",
            "starts_at": build_time(2019, 6, 30, 16, 0),
        },
        "extracted_data": {
            "location": "The Drunken Poet, 65 Peel St, West Melbourne VIC 3003",
            "date": "Sun 30 Jun 2019",
            "time": "4pm",
            "price": "FREE",
            "genre": "Blues",
        },
    },
    {
        "html": """<div class="article-meta-item">
    <div class="article-meta-headline">LOCATION</div>
    <div class="article-meta-content">
    <div>
    <a href="https://www.beat.com.au/directory/the-drunken-poet/">The Drunken Poet</a>,
    				</div>
    <div>
    										65 Peel St, West Melbourne VIC 3003		</div>
    </div>
    </div>, <div class="article-meta-item">
    <div class="article-meta-headline">DATE</div>
    <div class="article-meta-content">
    				Sun 30 Jun 2019			</div>
    </div>, <div class="article-meta-item">
    <div class="article-meta-headline">Time</div>
    <div class="article-meta-content">
    <div>6.30pm</div>
    </div>
    </div>, <div class="article-meta-item">
    <div class="article-meta-headline">PRICE</div>
    <div class="article-meta-content">
    				FREE			</div>
    </div>, <div class="article-meta-item">
    <div class="article-meta-headline">Genre</div>
    <div class="article-meta-content">
    <div class="breadcrumb">
    <a href="https://www.beat.com.au/genre/country-folk/">Country/Folk</a> </div>
    </div>
    </div>""",
        "parsed_data": {
            "price": None,
            "venue_name": "The Drunken Poet",
            "artist": None,
            "genre": "FOLK",
            "starts_at": build_time(2019, 6, 30, 18, 30),
        },
        "extracted_data": {
            "location": "The Drunken Poet, 65 Peel St, West Melbourne VIC 3003",
            "date": "Sun 30 Jun 2019",
            "time": "6.30pm",
            "price": "FREE",
            "genre": "Country/Folk",
        },
    },
    {
        "html": """<div class="article-meta-item">
    <div class="article-meta-headline">LOCATION</div>
    <div class="article-meta-content">
    <div>
    <a href="https://www.beat.com.au/directory/gasometer-hotel/">Gasometer Hotel</a>,
    				</div>
    <div>
    										484 Smith St, Collingwood VIC 3066		</div>
    </div>
    </div>, <div class="article-meta-item">
    <div class="article-meta-headline">DATE</div>
    <div class="article-meta-content">
    				Sun 30 Jun 2019			</div>
    </div>, <div class="article-meta-item">
    <div class="article-meta-headline">Time</div>
    <div class="article-meta-content">
    <div>7pm</div>
    </div>
    </div>, <div class="article-meta-item">
    <div class="article-meta-headline">PRICE</div>
    <div class="article-meta-content">
    				$10.00			</div>
    </div>, <div class="article-meta-item">
    <div class="article-meta-headline">Genre</div>
    <div class="article-meta-content">
    <div class="breadcrumb">
    <a href="https://www.beat.com.au/genre/country-folk/">Country/Folk</a> </div>
    </div>
    </div>""",
        "parsed_data": {
            "price": 10,
            "venue_name": "Gasometer Hotel",
            "artist": None,
            "genre": "FOLK",
            "starts_at": build_time(2019, 6, 30, 19, 0),
        },
        "extracted_data": {
            "location": "Gasometer Hotel, 484 Smith St, Collingwood VIC 3066",
            "date": "Sun 30 Jun 2019",
            "time": "7pm",
            "price": "$10.00",
            "genre": "Country/Folk",
        },
    },
    {
        "html": """<div class="article-meta-item">
    <div class="article-meta-headline">LOCATION</div>
    <div class="article-meta-content">
    <div>
    <a href="https://www.beat.com.au/directory/gasometer-hotel/">Gasometer Hotel</a>,
    				</div>
    <div>
    										484 Smith St, Collingwood VIC 3066		</div>
    </div>
    </div>, <div class="article-meta-item">
    <div class="article-meta-headline">DATE</div>
    <div class="article-meta-content">
    				Sun 30 Jun 2019			</div>
    </div>, <div class="article-meta-item">
    <div class="article-meta-headline">Time</div>
    <div class="article-meta-content">
    <div>2pm</div>
    </div>
    </div>, <div class="article-meta-item">
    <div class="article-meta-headline">Support</div>
    <div class="article-meta-content">
    				Benzo Baby, Holly Arabella			</div>
    </div>, <div class="article-meta-item">
    <div class="article-meta-headline">PRICE</div>
    <div class="article-meta-content">
    				$10.00			</div>
    </div>, <div class="article-meta-item">
    <div class="article-meta-headline">Genre</div>
    <div class="article-meta-content">
    <div class="breadcrumb">
    <a href="https://www.beat.com.au/genre/rock/">Rock</a> </div>
    </div>
    </div>""",
        "parsed_data": {
            "price": 10,
            "venue_name": "Gasometer Hotel",
            "artist": "Benzo Baby, Holly Arabella",
            "genre": "ROCK",
            "starts_at": build_time(2019, 6, 30, 14, 0),
        },
        "extracted_data": {
            "location": "Gasometer Hotel, 484 Smith St, Collingwood VIC 3066",
            "date": "Sun 30 Jun 2019",
            "time": "2pm",
            "support": "Benzo Baby, Holly Arabella",
            "price": "$10.00",
            "genre": "Rock",
        },
    },
    {
        "html": """<div class="article-meta-item">
    <div class="article-meta-headline">LOCATION</div>
    <div class="article-meta-content">
    <div>
    <a href="https://www.beat.com.au/directory/edinburgh-castle-hotel/">Edinburgh Castle Hotel</a>,
    				</div>
    <div>
    										681 Sydney Rd, Brunswick VIC 3056		</div>
    </div>
    </div>, <div class="article-meta-item">
    <div class="article-meta-headline">DATE</div>
    <div class="article-meta-content">
    				Sun 30 Jun 2019			</div>
    </div>, <div class="article-meta-item">
    <div class="article-meta-headline">Time</div>
    <div class="article-meta-content">
    <div>4pm</div>
    </div>
    </div>, <div class="article-meta-item">
    <div class="article-meta-headline">Genre</div>
    <div class="article-meta-content">
    <div class="breadcrumb">
    <a href="https://www.beat.com.au/genre/soul-funk/">Soul/Funk</a> </div>
    </div>
    </div>""",
        "parsed_data": {
            "price": None,
            "venue_name": "Edinburgh Castle Hotel",
            "artist": None,
            "genre": "JAZZ",
            "starts_at": build_time(2019, 6, 30, 16, 0),
        },
        "extracted_data": {
            "location": "Edinburgh Castle Hotel, 681 Sydney Rd, Brunswick VIC 3056",
            "date": "Sun 30 Jun 2019",
            "time": "4pm",
            "genre": "Soul/Funk",
        },
    },
    {
        "html": """<div class="article-meta-item">
    <div class="article-meta-headline">LOCATION</div>
    <div class="article-meta-content">
    <div>
    <a href="https://www.beat.com.au/directory/the-jazzlab/">The Jazzlab</a>,
    				</div>
    <div>
    										27 Leslie St, Brunswick VIC 3056		</div>
    </div>
    </div>, <div class="article-meta-item">
    <div class="article-meta-headline">DATE</div>
    <div class="article-meta-content">
    				Sun 30 Jun 2019			</div>
    </div>, <div class="article-meta-item">
    <div class="article-meta-headline">Time</div>
    <div class="article-meta-content">
    <div>8pm</div>
    </div>
    </div>, <div class="article-meta-item">
    <div class="article-meta-headline">PRICE</div>
    <div class="article-meta-content">
    				$20.00			</div>
    </div>, <div class="article-meta-item">
    <div class="article-meta-headline">Genre</div>
    <div class="article-meta-content">
    <div class="breadcrumb">
    <a href="https://www.beat.com.au/genre/jazz/">Jazz</a> </div>
    </div>
    </div>""",
        "parsed_data": {
            "price": 20,
            "venue_name": "The Jazzlab",
            "artist": None,
            "genre": "JAZZ",
            "starts_at": build_time(2019, 6, 30, 20, 0),
        },
        "extracted_data": {
            "location": "The Jazzlab, 27 Leslie St, Brunswick VIC 3056",
            "date": "Sun 30 Jun 2019",
            "time": "8pm",
            "price": "$20.00",
            "genre": "Jazz",
        },
    },
    {
        "html": """<div class="article-meta-item">
    <div class="article-meta-headline">LOCATION</div>
    <div class="article-meta-content">
    <div>
    <a href="https://www.beat.com.au/directory/wesley-anne/">Wesley Anne</a>,
    				</div>
    <div>
    										250 High St, Northcote VIC 3070			</div>
    </div>
    </div>, <div class="article-meta-item">
    <div class="article-meta-headline">DATE</div>
    <div class="article-meta-content">
    				Sun 30 Jun 2019			</div>
    </div>, <div class="article-meta-item">
    <div class="article-meta-headline">Time</div>
    <div class="article-meta-content">
    <div>6pm</div>
    </div>
    </div>, <div class="article-meta-item">
    <div class="article-meta-headline">LINEUP</div>
    <div class="article-meta-content">
    				Anita Levy, Nick Watson			</div>
    </div>, <div class="article-meta-item">
    <div class="article-meta-headline">PRICE</div>
    <div class="article-meta-content">
    				FREE			</div>
    </div>, <div class="article-meta-item">
    <div class="article-meta-headline">Genre</div>
    <div class="article-meta-content">
    <div class="breadcrumb">
    <a href="https://www.beat.com.au/genre/pop/">Pop</a> / <a href="https://www.beat.com.au/genre/acoustic/">Acoustic</a> </div>
    </div>
    </div>""",
        "parsed_data": {
            "price": None,
            "venue_name": "Wesley Anne",
            "artist": "Anita Levy, Nick Watson",
            "genre": "EDM",
            "starts_at": build_time(2019, 6, 30, 18, 0),
        },
        "extracted_data": {
            "location": "Wesley Anne, 250 High St, Northcote VIC 3070",
            "date": "Sun 30 Jun 2019",
            "time": "6pm",
            "lineup": "Anita Levy, Nick Watson",
            "price": "FREE",
            "genre": "Pop / Acoustic",
        },
    },
    {
        "html": """<div class="article-meta-item">
    <div class="article-meta-headline">LOCATION</div>
    <div class="article-meta-content">
    <div>
    <a href="https://www.beat.com.au/directory/spotted-mallard/">Spotted Mallard</a>,
    				</div>
    <div>
    										314 Sydney Rd, Brunswick VIC 3056		</div>
    </div>
    </div>, <div class="article-meta-item">
    <div class="article-meta-headline">DATE</div>
    <div class="article-meta-content">
    				Sun 30 Jun 2019			</div>
    </div>, <div class="article-meta-item">
    <div class="article-meta-headline">Time</div>
    <div class="article-meta-content">
    <div>4pm</div>
    </div>
    </div>, <div class="article-meta-item">
    <div class="article-meta-headline">PRICE</div>
    <div class="article-meta-content">
    				$32.50			</div>
    </div>, <div class="article-meta-item">
    <div class="article-meta-headline">Genre</div>
    <div class="article-meta-content">
    <div class="breadcrumb">
    <a href="https://www.beat.com.au/genre/global/">Global</a> </div>
    </div>
    </div>""",
        "parsed_data": {
            "price": 32,
            "venue_name": "Spotted Mallard",
            "artist": None,
            "genre": "JAZZ",
            "starts_at": build_time(2019, 6, 30, 16, 0),
        },
        "extracted_data": {
            "location": "Spotted Mallard, 314 Sydney Rd, Brunswick VIC 3056",
            "date": "Sun 30 Jun 2019",
            "time": "4pm",
            "price": "$32.50",
            "genre": "Global",
        },
    },
]
