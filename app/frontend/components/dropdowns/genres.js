import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'

import { actions } from 'state'
import styles from 'styles/dropdowns/genres.css'
import GenrePill from 'components/genre-pill'

const genres = [
  'JAZZ',
  'ARTS',
  'TRIVIA',
  'HIPHOP',
  'EDM',
  'ROCK',
  'FOLK',
  'COMEDY',
  'POKER',
]


export default class GenreDropDown extends Component {

  static propTypes = {
    filteredGenres: PropTypes.array,
    addGenreFilter: PropTypes.func,
    removeGenreFilter: PropTypes.func,
  }

  isDisabled = g => this.props.filteredGenres.includes(g)

  getAction = g => this.isDisabled(g)
    ? (() => this.props.removeGenreFilter(g))
    : (() => this.props.addGenreFilter(g))

  render() {
    return (
      <div className={styles.dropdown}>
        <div className="container">
          <div className={styles.genreList}>
            {genres.map((g, idx) =>
              <div key={idx} className={styles.genre} onClick={this.getAction(g)}>
                <GenrePill disabled={this.isDisabled(g)} genre={g}/>
              </div>
            )}
          </div>
        </div>
      </div>
    )
  }
}



const mapStateToProps = state => ({
  filteredGenres: state.filteredGenres,
})
const mapDispatchToProps = dispatch => ({
  addGenreFilter: g => dispatch(actions.filters.add('GENRE', g)),
  removeGenreFilter: g => dispatch(actions.filters.remove('GENRE', g)),
})
module.exports = connect(mapStateToProps, mapDispatchToProps)(GenreDropDown)
