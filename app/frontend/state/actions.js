import { logVenueClose, logVenueOpen, logToolbarOpen } from 'analytics'
import { fetchDataList } from './utils'


// Actions affecting filters
const filters = {
  add: (type, value) => ({ type: 'ADD_FILTER', filterType: type, value }),
  remove: (type, value) => ({ type: 'REMOVE_FILTER', filterType: type, value }),
};


const selections = {
  venue: {
    set: venue => {
      logVenueOpen(venue)
      return {type: 'SET_VENUE', venue: venue}
    },
    clear: () => {
      logVenueClose()
      return {type: 'SET_VENUE', venue: null}
    }
  },
  toolbar: {
    close: () =>
      ({type: 'CLOSE_TOOLBAR'}),
    open: selected => {
      logToolbarOpen(selected)
      return {type: 'OPEN_TOOLBAR', selected: selected}
    }
  }
}


const venue = {
  fetchList: fetchDataList('venue')
}


const event = {
  fetchList: fetchDataList('event'),
}


module.exports = {
  filters,
  selections,
  venue,
  event,
}
