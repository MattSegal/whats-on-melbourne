import ReactDOM from 'react-dom'
import React, { Component } from 'react'
import PropTypes from 'prop-types'
import ApolloClient from 'apollo-boost';
import { ApolloProvider } from 'react-apollo';

import GoogleMap from './map'
import VenueMap from './venue-map'
import Sidebar from './sidebar'


const client = new ApolloClient({uri: '/graphql/'})


class App extends Component {

  static childContextTypes = {
    activeVenue: PropTypes.object,
    activeEvent: PropTypes.object,
    setActiveVenue: PropTypes.func,
    unsetActiveVenue: PropTypes.func,
    setActiveEvent: PropTypes.func,
    unsetActiveEvent: PropTypes.func,
  }

 constructor(props, context) {
    super(props, context)
    this.state = {
      activeVenue: null,
      activeEvent: null
    }

  }

  getChildContext() {
    return {
      activeEvent: this.state.activeEvent,
      activeVenue: this.state.activeVenue,
      setActiveVenue: this.setActiveVenue,
      unsetActiveVenue: this.unsetActiveVenue,
      setActiveEvent: this.setActiveEvent,
      unsetActiveEvent: this.unsetActiveEvent,
    }
  }

  setActiveVenue = venue => {
    ga('send', {
      hitType: 'event',
      eventCategory: 'Venue',
      eventAction: 'click',
      eventLabel: venue.name
    })
    this.setState({activeVenue: venue, activeEvent: null})
  }

  unsetActiveVenue = () => {
    ga('send', {
      hitType: 'event',
      eventCategory: 'Venue',
      eventAction: 'close',
    })
    this.setState({activeVenue: null, activeEvent: null})
  }

  setActiveEvent = event => e => {
    ga('send', {
      hitType: 'event',
      eventCategory: 'Event',
      eventAction: 'click',
      eventLabel: event.name
    })
    this.setState({activeEvent: event})
  }

  unsetActiveEvent = e => {
    ga('send', {
      hitType: 'event',
      eventCategory: 'Event',
      eventAction: 'close',
    })
    this.setState({activeEvent: null})
  }

  render() {
    return <ApolloProvider client={client}>
      <div className='map-wrapper'>
        <Sidebar/>
        <GoogleMap>
          <VenueMap/>
        </GoogleMap>
      </div>
    </ApolloProvider>
  }
}


ReactDOM.render(
  <App/>,
  document.getElementById('app')
);
