import ReactDOM from 'react-dom'
import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { Provider } from 'react-redux'

import GoogleMap from 'components/google-map'
import VenueMap from 'components/venue-map'
import Sidebar from 'components/sidebar'
import Toolbar from 'components/toolbar'

import { store } from 'state'
import styles from 'styles/generic/wrapper.css'


class App extends Component {
  render() {
    return (
      <Provider store={store}>
        <div className={styles.wrapper}>
          <div><Toolbar/></div>
          <div className={styles.wrapperChild}>
            <Sidebar/>
            <GoogleMap><VenueMap/></GoogleMap>
          </div>
        </div>
      </Provider>
    )
  }
}


ReactDOM.render(<App/>, document.getElementById('app'))
