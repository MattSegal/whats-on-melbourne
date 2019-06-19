// @flow
import React, { useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'

import { actions } from 'state'
import { GoogleMap, VenueMarker } from 'components'
import { MAP } from 'consts'
import type { Venue, Event, Redux } from 'types'

export const Map = () => {
  const dispatch = useDispatch()
  useEffect(() => {
    actions.venues.fetch()(dispatch)
  }, [])
  const venues = useSelector<Array<Venue>, Redux>(s => s.venues)
  return (
    <GoogleMap
      defaultZoom={MAP.DEFAULT_ZOOM}
      centerLat={MAP.DEFAULT_LAT}
      centerLng={MAP.DEFAULT_LNG}
    >
      {venues.map(v => (
        <VenueMarker
          venue={v}
          key={`venue-${v.id}`}
          lat={v.latitude}
          lng={v.longitude}
        />
      ))}
    </GoogleMap>
  )
}
