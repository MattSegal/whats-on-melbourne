# Whats On in Melbourne

Live at https://whatsonmelb.fun/

Resources:

- https://tomchentw.github.io/react-google-maps/
- https://developers.google.com/maps/documentation/javascript/reference/3.exp/
- https://developers.google.com/maps/documentation/geocoding/start
- https://github.com/graphql-python/graphene-django
- https://www.apollographql.com/docs/react/essentials/get-started.html

Data sources:

- http://www.beat.com.au/gig-guide
- http://www.888pl.com.au/

Potential data sources:

- https://whatson.melbourne.vic.gov.au/Whatson/ArtsandCulture/TheatreandShows/Pages/TheatreandShows.aspx?scope=Whatson&TMFromDate=2018-05-15&TMToDate=2018-05-15&start=0
- http://malthousetheatre.com.au/whats-on
- https://marrinergroup.com.au/shows
- https://www.triplejunearthed.com/discover/gigs?featured=all&field_unearthed_genre_tid=all&term_node_tid_depth=3621&field_unearthed_campaign_tid=all
- https://www.last.fm/events
- https://pbsfm.org.au/gigs

### User Stories

As a user...

I want to know...

- where gigs are on tonight in Melbourne
- what time the gig is on
- what other gigs are on at that venue
- how much the tickets cost

I want to be able to...

- filter by genre
- filter by time
- browse to the band's website / facebook
- browse to the venue website

so that I can figure out where to go out tonight

As a website owner..

I want to attribute my sources
so that I drive some traffic their way.

### Future Work

- Add list view
  - Search list
  - venue search
  - show suburb in list
  - suburb search? close to me?
- fix toolbar dropdown
- use list view display to simplify map view
  - make it easy to switch list <--> map
- change genre filters to "filter for" rather than "filter out"
- Add dates in the future (tomorrow night, etc)
- time filters
- Try improve mobile map performance
- Improve SEO
  - server side rendering
  - add event schema
  - add about page
- Improve beat scraper
  - collect supporting acts
- login + save events + my events screen
