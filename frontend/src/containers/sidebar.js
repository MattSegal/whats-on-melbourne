// @flow
import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import styled, { css } from 'styled-components'
import moment from 'moment'

import { actions } from 'state'
import type { Venue, Event, Redux } from 'types'

export const Sidebar = () => {
  const dispatch = useDispatch()
  const selected = useSelector<Venue | null, Redux>(s => s.selected)
  const onClose = () => dispatch(actions.venues.clear())
  if (!selected) return null
  return (
    <SidebarEl>
      <CloseEl onClick={onClose}>&times;</CloseEl>
      <h2>{selected.name}</h2>
      {selected.website && <a href={selected.website}>venue website</a>}
      {selected.events.map(event => (
        <EventEl key={event.id}>
          <h3>
            {event.name} ({event.event_type})
          </h3>
          {event.details_url && <a href={event.details_url}>More details</a>}
          {event.artist !== 'Unknown' && (
            <p>
              <strong>Artist:</strong> {event.artist}
            </p>
          )}
          <p>
            <strong>Start:</strong> {moment(event.starts_at).format('h:mm a')}
          </p>
          <p>
            <strong>Price:</strong> {event.price ? `$${event.price}` : 'Free?'}
          </p>
        </EventEl>
      ))}
    </SidebarEl>
  )
}

const EventEl = styled.div`
  background: #efefef;
  padding: 0.5rem;
  margin-bottom: 1rem;
`

const CloseEl = styled.div`
  cursor: pointer;
  font-size: 2.5rem;
  top: 0px;
  right: 12px;
  position: absolute;
`

const SidebarEl = styled.div`
  position: absolute;
  padding: 0.5rem;
  box-sizing: border-box;
  top: 36px;
  bottom: 0;
  width: 280px;
  background: rgba(255, 255, 255, 0.9);
`
