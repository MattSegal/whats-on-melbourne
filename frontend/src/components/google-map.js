// @flow
import React from 'react'
import styled from 'styled-components'
import GoogleMapReact from 'google-map-react'
import type { Node } from 'react'

type Props = {
  defaultZoom: number,
  centerLat: number,
  centerLng: number,
  children: Node,
}

// https://github.com/google-map-react/google-map-react#readme
export const GoogleMap = ({
  defaultZoom,
  centerLat,
  centerLng,
  children,
}: Props) => (
  <MapEl>
    <GoogleMapReact
      bootstrapURLKeys={{ key: MAPS_API_KEY }}
      defaultCenter={{ lat: centerLat, lng: centerLng }}
      defaultZoom={defaultZoom}
    >
      {children}
    </GoogleMapReact>
  </MapEl>
)
const MapEl = styled.div`
  height: calc(100vh - 36px);
  width: 100%;
`
