import React, { Component } from 'react'
import PropTypes from 'prop-types'

import styles from 'styles/genre-pill.css'


export default class GenrePill extends Component {

  static propTypes = {
    genre: PropTypes.string,
    disabled: PropTypes.bool,
  }

  render() {
    const { genre, disabled } = this.props
    if (!genre) {
      return null
    }
    let style = disabled ? styles.disabled : styles[genre.toLowerCase()]
    const className = `${styles.genre} ${style}`
    return (
      <div className={className}>{genre}</div>
    )
  }
}
