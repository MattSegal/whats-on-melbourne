// @flow
import type { Redux, Action } from 'types'

export const reducer = (state: Redux, action: Action): Redux => {
  switch (action.type) {
    case 'SELECT_VENUE':
      return {
        ...state,
        selected: action.venue,
      }
    case 'RECEIVE_VENUES':
      return {
        ...state,
        venues: action.venues,
      }
  }
  return state
}
