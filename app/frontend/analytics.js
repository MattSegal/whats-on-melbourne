const logVisitVenueWebsite = venue =>
  ga('send', {
    hitType: 'event',
    eventCategory: 'Venue',
    eventAction: 'website',
    eventLabel: venue.name,
    eventValue: venue.website,
  })

const logVenueClose = () =>
  ga('send', {
    hitType: 'event',
    eventCategory: 'Venue',
    eventAction: 'close'
  })

const logVenueOpen = venue =>
   ga('send', {
    hitType: 'event',
    eventCategory: 'Venue',
    eventAction: 'click',
    eventLabel: venue.name
  })

const logToolbarOpen = selected =>
   ga('send', {
    hitType: 'event',
    eventCategory: 'Toolbar',
    eventAction: 'click',
    eventLabel: selected
  })

const logSearchClick = (site, term) =>
  ga('send', {
    hitType: 'event',
    eventCategory: 'Search Event',
    eventAction: 'click',
    eventLabel: site,
    eventValue: term,
  })


module.exports = {
  logVisitVenueWebsite,
  logVenueClose,
  logVenueOpen,
  logSearchClick,
  logToolbarOpen,
}
