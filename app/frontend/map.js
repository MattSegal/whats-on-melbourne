import React from 'react'
import { withScriptjs, withGoogleMap, GoogleMap } from 'react-google-maps'
import { compose, withProps } from 'recompose'

// See map options here
// https://developers.google.com/maps/documentation/javascript/reference/3/#MapOptions
module.exports = compose(
  withProps({
    googleMapURL: "https://maps.googleapis.com/maps/api/js?v=3.exp&libraries=geometry,drawing,places",
    loadingElement: <div style={{ height: `100%` }} />,
    containerElement: <div style={{ height: `100%` }} />,
    mapElement: <div style={{ height: `100%` }} />,
  }),
  withScriptjs,
  withGoogleMap
)(props =>
  <GoogleMap
    defaultZoom={13}
    defaultCenter={{ lat: -37.812292, lng: 144.962281 }}
    onZoomChanged={() => console.log('what do now?')}
    options={{
      fullscreenControl: false,
      streetViewControl: false,
      clickableIcons: false,
    }}
  >
    {props.children}
  </GoogleMap>
)
