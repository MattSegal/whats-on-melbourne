import React, { Component } from 'react'
import PropTypes from 'prop-types'

import styles from 'styles/genre-pill.css'


export default class GenrePill extends Component {

  static propTypes = {
    eventType: PropTypes.string,
    disabled: PropTypes.bool,
  }

  render() {
    const { eventType, disabled } = this.props
    if (!eventType) {
      return null
    }
    let style = disabled ? styles.disabled : styles[eventType.toLowerCase()]
    const className = `${styles.genre} ${style}`
    return (
      <div className={className}>{eventType}</div>
    )
  }
}
