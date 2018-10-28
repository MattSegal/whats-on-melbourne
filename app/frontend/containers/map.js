import React, { Component } from 'react'
import { connect } from 'react-redux'

import { actions } from 'state'
import GoogleMap from 'components/google-map'
import VenueMap from 'components/venue-map'
import Sidebar from 'components/sidebar'
import Toolbar from 'components/toolbar'

import styles from 'styles/generic/wrapper.css'


export default class MapContainer extends Component {
  componentDidMount() {
    this.props.fetchVenueList()
    this.props.fetchEventList()
  }

  render() {
    return (
      <div className={styles.wrapper}>
        <Toolbar />
        <div className={styles.wrapperChild}>
          <Sidebar/>
          <GoogleMap><VenueMap/></GoogleMap>
        </div>
      </div>
    )
  }
}

const mapStateToProps = state => ({})
const mapDispatchToProps = dispatch => ({
  fetchVenueList: () => dispatch(actions.venue.fetchList(true)),
  fetchEventList: () => dispatch(actions.event.fetchList(true)),
})
module.exports = connect(mapStateToProps, mapDispatchToProps)(MapContainer)
