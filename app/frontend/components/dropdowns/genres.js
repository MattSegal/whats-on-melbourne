import React, { Component } from 'react'
import { connect } from 'react-redux'

import { GENRES, FILTERS } from 'consts'
import { actions } from 'state'
import styles from 'styles/dropdowns/genres.css'
import GenrePill from 'components/genre-pill'



export default class GenreDropDown extends Component {

  isDisabled = genre =>
   this.props.filters[FILTERS.GENRE].includes(genre)

  getAction = genre => this.isDisabled(genre)
    ? (() => this.props.removeGenreFilter(genre))
    : (() => this.props.addGenreFilter(genre))

  render() {
    return (
      <div className={styles.dropdown}>
        <div className="container">
          <div className={styles.genreList}>
            {GENRES.map((genre, idx) =>
              <div key={idx} className={styles.genre} onClick={this.getAction(genre)}>
                <GenrePill disabled={this.isDisabled(genre)} genre={genre}/>
              </div>
            )}
          </div>
        </div>
      </div>
    )
  }
}



const mapStateToProps = state => ({
  filters: state.filters,

})
const mapDispatchToProps = dispatch => ({
  addGenreFilter: g => dispatch(actions.filters.add('GENRE', g)),
  removeGenreFilter: g => dispatch(actions.filters.remove('GENRE', g)),
})
module.exports = connect(mapStateToProps, mapDispatchToProps)(GenreDropDown)
