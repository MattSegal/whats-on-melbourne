import React, { Component } from 'react'
import { connect } from 'react-redux'
import moment from 'moment'

import GenrePill from './genre-pill'
import { filterOutGenres } from 'utils'
import { actions } from 'state'
import styles from 'styles/event-list.css'


const Event = ({name, startsAt, venue, eventType}) => (
  <div className={styles.event}>
    <div>{name}</div>
    <div>at {venue.name}</div>
    <div>starts {moment(startsAt).format('H:mma')} - {moment(startsAt).fromNow()}</div>
    <GenrePill genre={eventType} />
  </div>
)

class EventList extends Component {

  render() {
    const { venueData, eventData, filters } = this.props
    if (venueData.loading || eventData.loading) {
      return (
        <div className="loading">Loading venues...</div>
      )
    }
    const events = eventData.list.filter(filterOutGenres(filters))
    const venues = venueData.list
      .map(v => ({...v, events: events.filter(e => e.venue === v.id )}))
      .filter(v => v.events.length > 0)
    return (
      <div className={styles.eventList}>
        {events
          .sort((a, b) => new Date(a.startsAt) - new Date (b.startsAt))
          .map(e => ({...e, venue: venueData.lookup[e.venue]}))
          .map(e => <Event key={e.id} {...e} />)
        }
      </div>
    )
  }
}


const mapStateToProps = state => ({
  venueData: state.data.venue,
  eventData: state.data.event,
  filters: state.filters,
})
const mapDispatchToProps = dispatch => ({})
module.exports = connect(mapStateToProps, mapDispatchToProps)(EventList)
