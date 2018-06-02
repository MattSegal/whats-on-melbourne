import ApolloClient from 'apollo-boost';
import { applyMiddleware, createStore } from 'redux'
import thunkMiddleware from 'redux-thunk'
import { createLogger }  from 'redux-logger'

import { logVenueClose, logVenueOpen } from 'analytics'
import { venuesQuery } from 'queries'

const client = new ApolloClient({uri: '/graphql/'})
const loggerMiddleware = createLogger()
const middleware = applyMiddleware(thunkMiddleware, loggerMiddleware)

const initialState = {
  activeVenue: null,
  venues: [],
}

const reducer = (state, action) => {
  switch(action.type) {
    case 'FETCH_DATA': return fetchDataReducer(state, action)
    case 'CLEAR_VENUE': return clearVenueReducer(state, action)
    case 'SET_VENUE': return openSidebarReducer(state, action)
    default: return {...state}
  }
}

// Actions
const actions = {
  clearVenue: () => {
    logVenueClose()
    return {type: 'CLEAR_VENUE'}
  },
  setVenue: venue => {
    logVenueOpen(venue)
    return {type: 'SET_VENUE', venue: venue}
  },
  fetchData: () => dispatch => {
    client.query({query: venuesQuery })
    .then(resp => {
      const { loading, error, data } = resp
      // TODO - handle errors more gracefully
      if (error) {
        console.error(resp)
      } else {
        dispatch({type: 'FETCH_DATA', venues: data.venues })
      }
    })
    .catch(e => console.error(e))
  },
}

// Reducers
const clearVenueReducer = (state, action) => ({...state, activeVenue: null})
const openSidebarReducer = (state, action) => ({...state, activeVenue: action.venue})
const fetchDataReducer = (state, action) => ({...state, venues: action.venues})

module.exports = {
  store: createStore(reducer, initialState, middleware),
  actions,
}
