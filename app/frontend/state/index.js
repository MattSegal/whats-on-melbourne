import { applyMiddleware, createStore } from 'redux'
import thunkMiddleware from 'redux-thunk'
import { createLogger }  from 'redux-logger'

import reducer from './reducer'
import actions from './actions'
import listener from './listener';

const loggerMiddleware = createLogger()
const middleware = applyMiddleware(thunkMiddleware, loggerMiddleware)

const initialState = {
  activeVenue: null,
  toolbarOpen: null,
  loading: false,
  filteredGenres: [],
  venues: [],
  visibleVenues: [],
}

const store = createStore(reducer, initialState, middleware)

// Initialize event listener
listener(store.dispatch, store.getState)

module.exports = { store, actions }
