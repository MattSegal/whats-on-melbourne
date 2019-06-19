// @flow
import type {
  Store as ReduxStore,
  Reducer as ReduxReducer,
  DispatchAPI,
} from 'redux'

export type Data = { [string]: any }

export type Event = {
  id: number,
  name: string,
  slug: string,
  starts_at: string,
  artist: string,
  price: number,
  event_type: string,
  details_url: string,
  show_search: boolean,
}

export type Venue = {
  id: number,
  name: string,
  slug: string,
  address: string,
  latitude: number,
  longitude: number,
  website: string,
  events: Array<Event>,
}

export type Action =
  | { type: 'SELECT_VENUE', venue: Venue | null }
  | { type: 'RECEIVE_VENUES', venues: Array<Venue> }

export type Redux = {
  venues: Array<Venue>,
  selected: Venue | null,
}

export type GetState = () => Redux
export type Thunk = (dispatch: Dispatch, getState: GetState) => void
export type Dispatch = DispatchAPI<Action | Thunk>
export type Store = ReduxStore<Redux, Action, Dispatch>
export type Reducer = ReduxReducer<Redux, Action>
