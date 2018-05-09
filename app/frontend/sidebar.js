import React from 'react'
import PropTypes from 'prop-types'
import dayjs from 'dayjs'

import styles from './styles/sidebar.css'


export default class Sidebar extends React.Component {

  static contextTypes = {
    activeVenue: PropTypes.object,
    unsetActiveVenue: PropTypes.func,
  }

  handleCloseClick = e => {
    e.preventDefault()
    this.context.unsetActiveVenue()
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
                    href={ `${activeVenue.website}?utm_source=whatsonmelb.fun` }
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    website
                  </a>
                </p>
              )}
            </div>
          </div>
          {activeVenue.events.map((e, idx) => <Event key={idx} {...e}/>)}
        </div>
      </div>
    )
  }
}


class Event extends React.Component {

  render() {
    const { name, artist, startsAt, price} = this.props
    const artistEl = name !== artist &&
      <p><strong>Artist:</strong> { artist }</p>

    const startEl = startsAt &&
      <p><strong>Starts:</strong> { dayjs(startsAt).format('H:mm') }</p>

    let priceEl
    if (price && price > 0) {
      priceEl = <p><strong>Price:</strong> ${ price }</p>
    }
    return (
      <div className="row">
        <div className="col">
          <div className={styles.event}>
            <h5>{ name }</h5>
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
