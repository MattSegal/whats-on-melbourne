import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { Marker } from 'react-google-maps'
import { MarkerClusterer } from 'react-google-maps/lib/components/addons/MarkerClusterer'
import { connect } from 'react-redux'


import styles from 'styles/venue-map.css'
import { actions } from 'state'


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


class VenueMap extends Component {

  componentDidMount() {
    this.props.fetchVenueList()
    this.props.fetchEventList()
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
    const { zoom, setVenue } = this.props
    return (
      <Marker
        key={idx}
        cursor="pointer"
        icon={this.getIcon(venue)}
        onClick={() => setVenue(venue)}
        position={{lat: venue.latitude, lng: venue.longitude}}
      />
    )
  }

  render() {
    const { venueData, eventData } = this.props
    if (venueData.loading || eventData.loading) {
      return <div className="loading">Loading venues...</div>
    }
    const venues = venueData.list.map(v =>
      ({...v, events: eventData.list.filter(e => e.venue === v.id )})
    )
    return (
      <MarkerClusterer
        averageCenter={true}
        enableRetinaIcons={true}
        gridSize={60}
        maxZoom={12}
        minimumClusterSize={10}
      >
        {venues.map(this.renderVenueMarker)}
      </MarkerClusterer>
    )
  }
}


const mapStateToProps = state => ({
  venueData: state.data.venue,
  eventData: state.data.event,
})
const mapDispatchToProps = dispatch => ({
  fetchVenueList: () => dispatch(actions.venue.fetchList(true)),
  fetchEventList: () => dispatch(actions.event.fetchList(true)),
  setVenue: venue => dispatch(actions.selections.venue.set(venue)),
})
module.exports = connect(mapStateToProps, mapDispatchToProps)(VenueMap)
