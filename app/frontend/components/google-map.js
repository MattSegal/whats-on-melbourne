import React, { cloneElement } from 'react'
import { withScriptjs, withGoogleMap, GoogleMap } from 'react-google-maps'
import { compose, withProps, withState, withHandlers } from 'recompose'

// See map options here
// https://developers.google.com/maps/documentation/javascript/reference/3/#MapOptions
module.exports = compose(
  withProps({
    googleMapURL: GOOGLE_MAPS_JS_URL,
    loadingElement: <div style={{ height: `100%` }} />,
    containerElement: <div style={{ height: `100%` }} />,
    mapElement: <div style={{ height: `100%` }} />,
  }),
  withState('zoom', 'onZoomChange', 13),
  withHandlers(() => {
    const refs = {
      map: undefined,
    }

    return {
      onMapMounted: () => ref => {
        refs.map = ref
      },
      onZoomChanged: ({ onZoomChange }) => () => {
        onZoomChange(refs.map.getZoom())
      }
    }
  }),

  withScriptjs,
  withGoogleMap
)(props =>
  <GoogleMap
    zoom={props.zoom}
    ref={props.onMapMounted}
    onZoomChanged={props.onZoomChanged}
    defaultCenter={{ lat: -37.812292, lng: 144.962281 }}
    options={{
      zoomControl: false,
      fullscreenControl: false,
      streetViewControl: false,
      clickableIcons: false,
      mapTypeControl: false,
      maxZoom: 17,
    }}
  >
    {cloneElement(props.children, { zoom: props.zoom })}
  </GoogleMap>
)
