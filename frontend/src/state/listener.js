// @flow
// Listen for events that occur outside of React and dispatch actions to store
import { actions } from './actions'
import type { Dispatch, GetState } from 'types'

export const listener = (dispatch: Dispatch, getState: GetState) => {
  // Close sidebar on escape keypress
  // @noflow
  document.onkeydown = e => {
    const isEscape =
      'key' in e ? e.key == 'Escape' || e.key == 'Esc' : e.keyCode == 27
    if (isEscape) {
      const state = getState()
      if (state.selected) {
        dispatch(actions.venues.clear())
      }
    }
  }
}
