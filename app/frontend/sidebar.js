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

  openNewTab = url => e => {
    e.preventDefault()
    window.open(url, '_blank')
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
              <h4 onClick={this.openNewTab(activeVenue.website)}>
                { activeVenue.name }
              </h4>
            </div>
          </div>
          {activeVenue.events.map((e, idx) => <Event key={idx} {...e}/>)}
        </div>
      </div>
    )
  }
}

const Event = props => {
  const { name, artist, startsAt, price} = props

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
        </div>
      </div>
    </div>
  )
}
