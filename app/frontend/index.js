import ReactDOM from 'react-dom'
import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { Provider } from 'react-redux'

import GoogleMap from 'map'
import VenueMap from 'venue-map'
import Sidebar from 'sidebar'

import {store} from 'state'


class App extends Component {
  render() {
    return (
      <Provider store={store}>
        <div className='map-wrapper'>
          <Sidebar/>
          <GoogleMap><VenueMap/></GoogleMap>
        </div>
      </Provider>
    )
  }
}


ReactDOM.render(<App/>, document.getElementById('app'))
