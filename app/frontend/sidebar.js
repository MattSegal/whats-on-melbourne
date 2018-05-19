import React, { Component } from 'react'
import PropTypes from 'prop-types'
import dayjs from 'dayjs'

import styles from './styles/sidebar.css'
import Event from './event.js'

export default class Sidebar extends Component {

  static contextTypes = {
    activeVenue: PropTypes.object,
    unsetActiveVenue: PropTypes.func,
  }

  handleCloseClick = e => {
    e.preventDefault()
    this.context.unsetActiveVenue()
  }

  logVisitVenueWebsite = venue => e => {
    ga('send', {
      hitType: 'event',
      eventCategory: 'Venue',
      eventAction: 'website',
      eventLabel: venue.name,
      eventValue: venue.website,
    })
  }

  render() {
    const { activeVenue } = this.context
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
                  <a
                    href={activeVenue.website}
                    onClick={this.logVisitVenueWebsite(activeVenue)}
                  >
                    venue website
                  </a>
                </p>
              )}
            </div>
          </div>
          {activeVenue.events.map((event, idx) => <Event key={idx} event={event}/>)}
        </div>
      </div>
    )
  }
}
