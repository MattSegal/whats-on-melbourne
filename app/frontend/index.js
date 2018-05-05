import ReactDOM from 'react-dom'
import React from 'react'
import PropTypes from 'prop-types'
import ApolloClient from 'apollo-boost';
import { ApolloProvider } from 'react-apollo';

import GoogleMap from './map'
import VenueMap from './venue-map'
import Sidebar from './sidebar'


const client = new ApolloClient({uri: '/graphql/'})


class App extends React.Component {

  static childContextTypes = {
    activeVenue: PropTypes.object,
    setActiveVenue: PropTypes.func,
    unsetActiveVenue: PropTypes.func,
  }

 constructor(props, context) {
    super(props, context)
    this.state = {
      activeVenue: null,
    }

  }

  getChildContext() {
    return {
      activeVenue: this.state.activeVenue,
      setActiveVenue: this.setActiveVenue,
      unsetActiveVenue: this.unsetActiveVenue,
    }
  }

  setActiveVenue = venue => {
    this.setState({activeVenue: venue})
  }

  unsetActiveVenue = () => {
    this.setState({activeVenue: null})
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
