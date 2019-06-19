// @flow
import React from 'react'
import { useDispatch } from 'react-redux'

import { actions } from 'state'
import type { Venue } from 'types'

type Props = {
  venue: Venue,
}

export const VenueMarker = ({ venue }: Props) => {
  const dispatch = useDispatch()
  const onClick = () => dispatch(actions.venues.set(venue))
  if (!venue.latitude || !venue.longitude) {
    const msg = `Bad coordinates for ${venue.name}. lat, lng: ${venue.latitude}, ${venue.longitude}`
    console.error(msg)
    return null
  }
  const eventTypes = venue.events.map(e => e.event_type).filter(et => et)
  const eventType = eventTypes.length > 0 ? eventTypes[0] : 'UNKNOWN'
  const imgUrl = genreMap[eventType]
  return <img src={imgUrl} onClick={onClick} />
}

const getMarkerUrl = (color, letter) =>
  `/static/img/markers/${color}_Marker${letter}.png`

const genreMap = {
  UNKNOWN: getMarkerUrl('green', 'unknown'),
  JAZZ: getMarkerUrl('red', 'J'),
  ARTS: getMarkerUrl('purple', 'A'),
  TRIVIA: getMarkerUrl('pink', 'T'),
  HIPHOP: getMarkerUrl('orange', 'H'),
  EDM: getMarkerUrl('darkgreen', 'E'),
  ROCK: getMarkerUrl('blue', 'R'),
  FOLK: getMarkerUrl('paleblue', 'F'),
  COMEDY: getMarkerUrl('yellow', 'C'),
  POKER: getMarkerUrl('brown', 'P'),
}
