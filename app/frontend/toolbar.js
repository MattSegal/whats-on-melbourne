import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'

import styles from 'styles/toolbar.css'

import { actions } from 'state'


class Toolbar extends Component {

  static propTypes = {
    xxx: PropTypes.func,
  }

  render() {
    const { xxx } = this.props
    return (
      <div className={styles.toolbar}>
        <span className={styles.option}>Earliest: 5pm</span>
        <span className={styles.option}>Latest: 11pm</span>
        <span className={styles.option}>Genres</span>
      </div>
    )
  }
}


const mapStateToProps = state => ({
  xxx: state.xxx,
})
const mapDispatchToProps = dispatch => ({
  xxx: () => dispatch(actions.clearVenue()),
})
module.exports = connect(mapStateToProps, mapDispatchToProps)(Toolbar)
