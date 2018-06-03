// Reducers0
const reducers = {
  ADD_GENRE_FILTER: (state, action) => {
    const filteredGenres = [
      ...state.filteredGenres,
      action.genre,
    ]
    return {
      ...state,
      filteredGenres: filteredGenres,
      visibleVenues: filterVenues(state.venues, filteredGenres),
    }
  },
  REMOVE_GENRE_FILTER: (state, action) => {
    const filteredGenres = state.filteredGenres.filter(g => g != action.genre)
    return {
      ...state,
      filteredGenres: filteredGenres,
      visibleVenues: filterVenues(state.venues, filteredGenres),
    }
  },
  FETCH_DATA_REQUEST: (state, action) => ({
    ...state,
    loading: true
  }),
  FETCH_DATA_RESPONSE: (state, action) => ({
    ...state,
    venues: action.venues,
    visibleVenues: filterVenues(action.venues, state.filteredGenres),
    loading: false
  }),
  CLEAR_VENUE: (state, action) => ({
    ...state,
    activeVenue: null
  }),
  SET_VENUE: (state, action) => ({
    ...state,
    activeVenue: action.venue,
    toolbarOpen: null,
  }),
  OPEN_TOOLBAR: (state, action) => ({
    ...state,
    toolbarOpen: action.selected,
    activeVenue: null,
  }),
  CLOSE_TOOLBAR:(state, action) => ({
    ...state,
    toolbarOpen: null
  }),
}

const filterVenues = (venues, filteredGenres) => venues
  .map(v => ({
    ...v,
    events: v.events.filter(e => !filteredGenres.includes(e.eventType))
  }))
  .filter(v => v.events.length > 0)

module.exports =  (state, action) => {
  const func = reducers[action.type]
  if (!func) return {...state}
  return func(state, action)
}
