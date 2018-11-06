import React, { Component } from 'react'
import PropTypes from 'prop-types'

import styles from 'styles/genre-pill.css'

const COLORS = {
  jazz: '#FF776B',
  arts: '#C89BFF',
  trivia: '#FDABFF',
  hiphop: '#FD8D08',
  edm: '#01BF00',
  rock: '#6B98FF',
  folk: '#BCE3FF',
  comedy: '#FFED5C',
  poker: '#cb9d7c',
}

export default class GenrePill extends Component {

  static propTypes = {
    genre: PropTypes.string,
    disabled: PropTypes.bool,
  }

  static getColor(genre){
    return COLORS[genre.toLowerCase()]
  }

  render() {
    const { genre, disabled } = this.props
    if (!genre) {
      return null
    }
    let disabledStyle = disabled ? styles.disabled : ''
    const className = `${styles.genre} ${disabledStyle}`
    return (
      <div
        style={{ backgroundColor: GenrePill.getColor(genre) }}
        className={className}
      >
        {genre}
      </div>
    )
  }
}
