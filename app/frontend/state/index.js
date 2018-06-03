import { applyMiddleware, createStore } from 'redux'
import thunkMiddleware from 'redux-thunk'
import { createLogger }  from 'redux-logger'

import reducer from './reducer'
import actions from './actions'

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


module.exports = {
  store: createStore(reducer, initialState, middleware),
  actions,
}
