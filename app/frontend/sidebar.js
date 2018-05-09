import React from 'react'
import PropTypes from 'prop-types'
import dayjs from 'dayjs'

import styles from './styles/sidebar.css'


export default class Sidebar extends React.Component {

  static contextTypes = {
    activeEvent: PropTypes.object,
    activeVenue: PropTypes.object,
    unsetActiveVenue: PropTypes.func,
  }

  handleCloseClick = e => {
    e.preventDefault()
    this.context.unsetActiveVenue()
  }

  render() {
    const { activeVenue, activeEvent } = this.context
    if (!activeVenue) {
      return null
    }
    return (
      <div className={styles.sidebar}>
        <div
          className={styles.close}
          onClick={this.handleCloseClick}
        >&times;</div>
        <div className="container">
          <div className="row">
            <div className="col">
              <h4 className={styles.title}>
                { activeVenue.name }
              </h4>
              {activeVenue.website && (
                <p className={ styles.website }>
                  <a href={`${activeVenue.website}?utm_source=whatsonmelb.fun`}>
                    venue website
                  </a>
                </p>
              )}
            </div>
          </div>
          {!activeEvent && <EventList events={activeVenue.events}/>}
          {activeEvent && <ActiveEvent event={activeEvent}/>}
        </div>
      </div>
    )
  }
}

class EventList extends React.Component {

  render() {
    const { events } = this.props
    if (events.length > 1) {
      return <div>{events.map((event, idx) => <Event key={idx} event={event}/>)}</div>
    } else if (events.length === 1) {
      return <ActiveEvent event={events[0]}/>
    }
  }
}


class Event extends React.Component {

  static propTypes = {
    event: PropTypes.shape({
      name: PropTypes.string,
      artist: PropTypes.string,
      startsAt: PropTypes.string,
      price: PropTypes.number,
    })
  }

  static contextTypes = {
    setActiveEvent: PropTypes.func,
  }

  render() {
    const { event } = this.props
    const { setActiveEvent } = this.context
    const artistEl = event.name !== event.artist &&
      <p><strong>Artist:</strong> { event.artist }</p>

    const startEl = event.startsAt &&
      <p><strong>Starts:</strong> { dayjs(event.startsAt).format('H:mm') }</p>

    let priceEl
    if (event.price && event.price > 0) {
      priceEl = <p><strong>Price:</strong> ${ event.price }</p>
    }
    return (
      <div className="row">
        <div className="col">
          <div
            className={`${styles.event} ${styles.clickable}`}
            onClick={setActiveEvent(event)}
          >
            <h5>{ event.name }</h5>
            {artistEl}
            {startEl}
            {priceEl}
            <div className={styles.cta}>Click for search</div>
          </div>
        </div>
      </div>
    )
  }
}


class ActiveEvent extends React.Component {

  static propTypes = {
    event: PropTypes.shape({
      name: PropTypes.string,
      artist: PropTypes.string,
      startsAt: PropTypes.string,
      price: PropTypes.number,
    })
  }

  static contextTypes = {
    activeEvent: PropTypes.object,
    unsetActiveEvent: PropTypes.func,
  }

  renderSoundCloudSearch() {
    const { event } = this.props
    const query = encodeURIComponent(event.artist || event.name)
    const search = `https://soundcloud.com/search/sets?q=${query}`
    return <div><a href={search}>search SoundCloud</a></div>
  }

  renderBandCampSearch() {
    const { event } = this.props
    const query = encodeURIComponent(event.artist || event.name)
    const search = `https://bandcamp.com/search?q=${query}`
    return <div><a href={search}>search BandCamp</a></div>
  }

  renderYoutubeSearch() {
    const { event } = this.props
    const query = encodeURIComponent(event.artist || event.name)
    const search = `https://www.youtube.com/results?search_query=${query}`
    return <div><a href={search}>search YouTube</a></div>
  }

  render() {
    const { event } = this.props
    const { unsetActiveEvent } = this.context
    const artistEl = event.name !== event.artist &&
      <p><strong>Artist:</strong> { event.artist }</p>

    const startEl = event.startsAt &&
      <p><strong>Starts:</strong> { dayjs(event.startsAt).format('H:mm') }</p>

    let priceEl
    if (event.price && event.price > 0) {
      priceEl = <p><strong>Price:</strong> ${ event.price }</p>
    }
    return (
      <div className="row">
        <div className="col">
          <div className={styles.event}>
            <h5>{ event.name }</h5>
            {artistEl}
            {startEl}
            {priceEl}
            <div className={styles.searchBox}>
              {this.renderYoutubeSearch()}
              {this.renderSoundCloudSearch()}
              {this.renderBandCampSearch()}
            </div>
            {this.context.activeEvent &&
              <p className={styles.closeEvent} onClick={unsetActiveEvent}>close</p>
            }
          </div>
        </div>
      </div>
    )
  }
}

