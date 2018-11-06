import React, { Component } from 'react'
import { connect } from 'react-redux'
import moment from 'moment'

import GenrePill from './genre-pill'
import { filterOutGenres } from 'utils'
import { actions } from 'state'
import styles from 'styles/event-list.css'


const formatTitle = title => {
  let items
  if (title.length < 35) return <span>{ title }</span>
  if (title.includes('–')) {
    items = title.split('–').map(s => s.trim())
  } else if (title.includes('(')) {
    items = title.split('(').map(s => s.trim().replace(')', ''))
  } else {
    const words = title.split(' ')
    items = [
      words.slice(0, -2).join(' '),
      words.slice(-2).join(' '),
    ]
  }
  return (
    <span>
      {items.slice(0, -1).join(' ')}
      <br />
      {items.slice(-1).join(' ')}
    </span>
  )
}

class Event extends Component {

  constructor(props) {
    super(props)
    this.state = { isOpen: false }
  }

  toggleOpen = () =>
    this.setState({ isOpen: !this.state.isOpen })

  render() {
    const { isOpen } = this.state
    const { name, startsAt, venue, eventType } = this.props
    return (
      <div
        className={styles.event}
        style={{ borderColor: GenrePill.getColor(eventType) }}
        >
        <div className={styles.title}>{formatTitle(name)}</div>
        <div className={styles.subtitle}>{moment(startsAt).format('h:mma')} at {venue.name}</div>
        <div className={styles.genre}>
          <GenrePill genre={eventType} />
        </div>
        {!isOpen && (
          <div onClick={this.toggleOpen} className={styles.openBtn}>more</div>
        )}
        {isOpen && (
          <div onClick={this.toggleOpen} className={styles.openBtn}>open!</div>
        )}
      </div>
    );
  }
}

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
