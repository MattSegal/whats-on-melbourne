import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'

import styles from 'styles/sidebar.css'
import genericStyles from 'styles/generic/sidebar.css'

import Event from './event.js'
import { logVisitVenueWebsite } from 'analytics'
import { actions } from 'state'


class Sidebar extends Component {

  static propTypes = {
    activeVenue: PropTypes.object,
    handleClose: PropTypes.func,
  }

  render() {
    const { activeVenue, handleClose } = this.props
    if (!activeVenue) {
      return null
    }
    return (
      <div className={genericStyles.sidebar}>
        <div className={genericStyles.close} onClick={handleClose} >&times;</div>
        <div className="container">
          <div className="row">
            <div className="col">
              <div className={styles.pill}>
                <h4 className={styles.title}>{ activeVenue.name }</h4>
                {activeVenue.website && (
                  <p className={ styles.link }>
                    <a href={activeVenue.website} onClick={() => logVisitVenueWebsite(activeVenue)}>
                      venue website
                    </a>
                  </p>
                )}
              </div>
            </div>
          </div>
          {activeVenue.events.map((event, idx) => <Event key={idx} event={event}/>)}
        </div>
      </div>
    )
  }
}


const mapStateToProps = state => ({
  activeVenue: state.activeVenue,
})
const mapDispatchToProps = dispatch => ({
  handleClose: () => dispatch(actions.clearVenue()),
})
module.exports = connect(mapStateToProps, mapDispatchToProps)(Sidebar)
