import React from 'react'
import PropTypes from 'prop-types'
import { Query } from "react-apollo"
import { Marker, OverlayView } from 'react-google-maps'

import styles from './styles/venue-map.css'
import { venuesQuery } from './queries'


const getPixelPositionOffset = (width, height) => ({
  x: -(width / 2),
  y: 3,
})

export default class VenueMap extends React.Component {

  static contextTypes = {
    setActiveVenue: PropTypes.func,
  }

  handleVenueClick = venue => e => {
    this.context.setActiveVenue(venue)
  }

  renderVenueOverlay = venue => {
    return <div className={styles.overlay}>
      <h1 onClick={this.handleVenueClick(venue)}>
        {venue.name}
      </h1>
    </div>
  }

  renderVenueQuery = result => {
    const { zoom } = this.props
    const { loading, error, data } = result
    if (error || loading) {
      return null
    }
    return data.venues.map((venue, idx) => (
      <div key={idx}>
        <Marker
          onClick={this.handleVenueClick(venue)}
          position={{lat: venue.latitude, lng: venue.longitude}}
        />
        {zoom > 14 &&
          <OverlayView
            position={{lat: venue.latitude, lng: venue.longitude}}
            mapPaneName={OverlayView.OVERLAY_MOUSE_TARGET}
            getPixelPositionOffset={getPixelPositionOffset}
          >
            {this.renderVenueOverlay(venue)}
          </OverlayView>
        }
      </div>
    ))
  }

  render() {
    return (
      <div>
        <Query query={venuesQuery}>
          {this.renderVenueQuery}
        </Query>
      </div>
    )
  }
}
