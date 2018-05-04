import React from 'react'
import { withScriptjs, withGoogleMap, GoogleMap } from 'react-google-maps'
import { compose, withProps, withState, withHandlers } from 'recompose'

// See map options here
// https://developers.google.com/maps/documentation/javascript/reference/3/#MapOptions
module.exports = compose(
  withProps({
    googleMapURL: "https://maps.googleapis.com/maps/api/js?v=3.exp&libraries=geometry,drawing,places",
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
      fullscreenControl: false,
      streetViewControl: false,
      clickableIcons: false,
    }}
  >
    {React.cloneElement(props.children, { zoom: props.zoom })}
  </GoogleMap>
)
