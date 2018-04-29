const mockVenue = {
  name: 'Workers Club',
  location: {lat: -37.812292, lng: 144.962281},
  website: 'http://www.theworkersclub.com.au/',
  events: [
    {
      name: 'A.U.D.I.O',
      type: 'music',
      genres: ['rock'],
      time: '13:00',
      venueLink: 'http://www.theworkersclub.com.au/audio.html',
      facebook: 'https://www.facebook.com/events/351867378631515/',
    },
    {
      name: 'Morning Maxwell',
      type: 'music',
      genres: ['jazz', 'hip-hop'],
      time: '20:00',
      venueLink: 'http://www.theworkersclub.com.au/morning-maxwell.html',
      facebook: 'https://www.facebook.com/events/148261812663723/',
    }
  ]
}

module.exports = mockVenue
