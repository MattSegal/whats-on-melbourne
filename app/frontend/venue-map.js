import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { Query } from "react-apollo"
import { Marker } from 'react-google-maps'
import { MarkerClusterer } from 'react-google-maps/lib/components/addons/MarkerClusterer'


import styles from './styles/venue-map.css'
import { venuesQuery } from './queries'


// Colors blue brown darkgreen green orange paleblue pink purple red yellow
// Letters A-Z
const getMarkerUrl = (color, letter) => `/static/img/markers/${color}_Marker${letter}.png`
const genreMap = {
  UNKNOWN: getMarkerUrl('green', 'unknown'),
  JAZZ: getMarkerUrl('red', 'J'),
  ARTS: getMarkerUrl('purple', 'A'),
  TRIVIA: getMarkerUrl('pink', 'T'),
  HIPHOP: getMarkerUrl('orange', 'H'),
  EDM: getMarkerUrl('darkgreen', 'E'),
  ROCK: getMarkerUrl('blue', 'R'),
  FOLK: getMarkerUrl('paleblue', 'F'),
  COMEDY: getMarkerUrl('yellow', 'C'),
  POKER: getMarkerUrl('brown', 'P'),
}


export default class VenueMap extends Component {

  static contextTypes = {
    setActiveVenue: PropTypes.func,
  }

  handleVenueClick = venue => e => {
    this.context.setActiveVenue(venue)
  }

  getIcon = venue => {

    const eventTypes = venue.events.filter(e => e.eventType)
    const eventType = eventTypes.length > 0 ? eventTypes.slice(-1)[0].eventType : 'UNKNOWN'
    return {
      url: genreMap[eventType],
      labelOrigin: new google.maps.Point(15, 45),
    }
  }

  getLabel = venue => ({
    fontSize: '18px',
    text: venue.name,
  })

  renderVenueMarker = (venue, idx) => {
    if (!venue.latitude || !venue.longitude) {
      console.error(`Bad coordinates for ${venue.name}. lat, lng: ${venue.latitude}, ${venue.longitude}`)
      return null
    }
    const { zoom } = this.props
    return (
      <Marker
        key={idx}
        cursor="pointer"
        icon={this.getIcon(venue)}
        label={zoom > 15 ? this.getLabel(venue) : ''}
        onClick={this.handleVenueClick(venue)}
        position={{lat: venue.latitude, lng: venue.longitude}}
      />
    )
  }


  renderVenueQuery = result => {
    const { loading, error, data } = result
    if (error || loading) {
      return null
    }
    return (
      <MarkerClusterer
        averageCenter={true}
        enableRetinaIcons={true}
        gridSize={60}
        maxZoom={12}
        minimumClusterSize={5}
      >
      {data.venues.map(this.renderVenueMarker)}
      </MarkerClusterer>
    )
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
