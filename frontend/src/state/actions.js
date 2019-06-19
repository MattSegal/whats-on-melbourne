// @flow
import { api } from './api'
import type { Venue, Event, Dispatch } from 'types'

export const actions = {
  venues: {
    set: (venue: Venue) => ({ type: 'SELECT_VENUE', venue }),
    clear: () => ({ type: 'SELECT_VENUE', venue: null }),
    fetch: () => (dispatch: Dispatch) =>
      api.venues.list().then(venues => {
        dispatch({ type: 'RECEIVE_VENUES', venues })
      }),
  },
}
