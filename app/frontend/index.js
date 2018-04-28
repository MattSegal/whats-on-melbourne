import React from 'react'
import ReactDOM from 'react-dom'
import { Marker, OverlayView } from 'react-google-maps'

import GoogleMap from './map'

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


const getPixelPositionOffset = (width, height) => ({
  x: width / 6,
  y: -(height / 2),
})

class VenueMap extends React.Component {
  // TODO: Proptypes

  openNewTab(e, url) {
    e.preventDefault()
    window.open(url, '_blank')
  }

  renderVenueOverlay(venue) {
    return <div className="venue-overlay">
      <h1 onClick={e => this.openNewTab(e, venue.website)}>
        {venue.name}
      </h1>
    </div>
  }

  renderVenue() {
    return <div>
      <Marker position={mockVenue.location} />
      <OverlayView
        position={mockVenue.location}
        mapPaneName={OverlayView.OVERLAY_MOUSE_TARGET}
        getPixelPositionOffset={getPixelPositionOffset}
      >
        {this.renderVenueOverlay(mockVenue)}
      </OverlayView>
    </div>
  }

  render() {
    const props = this.props
    return <div>{this.renderVenue()}</div>
  }
}


class App extends React.Component {
  render() {
    return (
      <div className="map-wrapper">
        <GoogleMap>
          <VenueMap/>
        </GoogleMap>
      </div>
    )
  }
}


ReactDOM.render(
  <App/>,
  document.getElementById('app')
);
