import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'

import styles from 'styles/toolbar.css'

import { actions } from 'state'
import GenreDropDown from './dropdowns/genres'

const options = {
  GENRES: 'GENRES',
}

const dropdowns = {
  GENRES: GenreDropDown,
}


class Toolbar extends Component {

  static propTypes = {
    openToolbar: PropTypes.func,
    closeToolbar: PropTypes.func,
    toolbarOpen: PropTypes.string,
  }

  render() {
    const { openToolbar, closeToolbar, toolbarOpen } = this.props
    const DropDown = dropdowns[toolbarOpen]
    const action = toolbarOpen ? closeToolbar : openToolbar
    return (
     <div className={styles.toolbar}>
        <div className={styles.options}>
          <span
            className={styles.option}
            onClick={() => action(options.GENRES)}>Genres</span>
        </div>
        <div className={`${styles.dropdown} ${toolbarOpen && styles.open}`}>
            {toolbarOpen && <DropDown/>}
        </div>
      </div>
    )
  }
}




const mapStateToProps = state => ({
  toolbarOpen: state.toolbarOpen,
})
const mapDispatchToProps = dispatch => ({
  closeToolbar: () => dispatch(actions.closeToolbar()),
  openToolbar: s => dispatch(actions.openToolbar(s)),
})
module.exports = connect(mapStateToProps, mapDispatchToProps)(Toolbar)
