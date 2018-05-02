import React from 'react'
import PropTypes from 'prop-types'
import dayjs from 'dayjs'

export default class Sidebar extends React.Component {

  static contextTypes = {
    activeVenue: PropTypes.object,
    unsetActiveVenue: PropTypes.func,
  }

  handleCloseClick = e => {
    e.preventDefault()
    this.context.unsetActiveVenue()
  }

  openNewTab = url => e => {
    e.preventDefault()
    window.open(url, '_blank')
  }

  render() {
    const { activeVenue } = this.context
    console.log(activeVenue)
    if (!activeVenue) {
      return null
    }
    return <div className="sidebar">
      <div className="container">
        <div className="row">
          <div className="col">
            <h3 onClick={this.openNewTab(activeVenue.website)}>
              { activeVenue.name }
            </h3>
          </div>
        </div>
        <div className="row">
          <div className="col">
              <button onClick={this.handleCloseClick}>
                close
              </button>
          </div>
        </div>
        {activeVenue.events.map((e, idx) => (
          <div key={idx} className="row">
            <div className="col">
              <h5>{ e.name }</h5>
              {e.name !== e.artist && <h5>{ e.artist }</h5>}
              <h5>{ dayjs(e.startsAt).format('H:mm') }</h5>
              {e.price && e.price > 0 && <h5>${ e.price }</h5>}
            </div>
          </div>
        ))}
      </div>
    </div>
  }
}
