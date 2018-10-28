import React, { Component } from 'react'
import { connect } from 'react-redux'

import { actions } from 'state'
import Toolbar from 'components/toolbar'
import EventList from 'components/event-list'


export default class ListContainer extends Component {
  componentDidMount() {
    this.props.fetchVenueList()
    this.props.fetchEventList()
  }

  render() {
    return (
      <div >
        <Toolbar />
        <div className="container">
          <EventList />
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
module.exports = connect(mapStateToProps, mapDispatchToProps)(ListContainer)
