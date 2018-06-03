import ApolloClient from 'apollo-boost';

import { logVenueClose, logVenueOpen, logToolbarOpen } from 'analytics'
import { venuesQuery } from './queries'

const client = new ApolloClient({uri: '/graphql/'})

// Actions
module.exports = {
  addGenreFilter: genre => {
    return {type: 'ADD_GENRE_FILTER', genre: genre}
  },
  removeGenreFilter: genre => {
    return {type: 'REMOVE_GENRE_FILTER', genre: genre}
  },
  clearVenue: () => {
    logVenueClose()
    return {type: 'CLEAR_VENUE'}
  },
  setVenue: venue => {
    logVenueOpen(venue)
    return {type: 'SET_VENUE', venue: venue}
  },
  closeToolbar: () => {
    return {type: 'CLOSE_TOOLBAR'}
  },
  openToolbar: selected => {
    logToolbarOpen(selected)
    return {type: 'OPEN_TOOLBAR', selected: selected}
  },
  fetchData: () => dispatch => {
    dispatch({type: 'FETCH_DATA_REQUEST'})
    client.query({query: venuesQuery })
    .then(resp => {
      const { loading, error, data } = resp
      // TODO - handle errors more gracefully
      if (error) {
        console.error(resp)
      } else {
        dispatch({type: 'FETCH_DATA_RESPONSE', venues: data.venues })
      }
    })
    .catch(e => console.error(e))
  },
}
