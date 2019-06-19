// @flow
import type { Venue } from 'types'
export const api = {
  venues: {
    list: (): Promise<Array<Venue>> =>
      fetch(`${SERVER}/api/venue/`, { credentials: 'include' }).then(r =>
        r.json()
      ),
  },
}
