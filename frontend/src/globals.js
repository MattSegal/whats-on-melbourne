// @flow
import * as React from 'react'
import type { Action, Redux, Dispatch, Store } from 'types'

// Global variables from build system
declare var STATIC_URL: string
declare var SERVER: string
declare var MAPS_API_KEY: string

declare module 'react-redux' {
  declare export function Provider(props: {
    store: Store,
    children: React.Node,
  }): React$Element<any>
  declare export var shallowEqual: Function
  declare export function useDispatch(): Dispatch
  declare export function useSelector<T, State>((State) => T, Function): T
}
