import React, { Component } from 'react'

import styles from 'styles/genre-pill.css'


export default class GenrePill extends Component {
  render() {
    const { event } = this.props
    if (!event.eventType) {
      return
    }
    const className = `${styles.genre} ${styles[event.eventType.toLowerCase()]}`
    return (
      <div className={className}>{event.eventType}</div>
    )
  }
}
