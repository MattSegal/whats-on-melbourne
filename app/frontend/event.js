import React, { Component } from 'react'
import PropTypes from 'prop-types'
import dayjs from 'dayjs'

import styles from './styles/event.css'

export default class Event extends Component {

  static propTypes = {
    event: PropTypes.shape({
      name: PropTypes.string,
      artist: PropTypes.string,
      startsAt: PropTypes.string,
      price: PropTypes.number,
      showSearch: PropTypes.bool,
      eventType: PropTypes.string,
    })
  }

  constructor(props) {
    super(props)
    this.state = { hasError: false };
  }

  componentDidCatch(error, info) {
    console.error(error)
    this.setState({ hasError: true });
  }

  renderDetail(label, value) {
    return <div className={styles.detail}>
      <span className={styles.detailLabel}>{label}</span>
      <span>{ value }</span>
    </div>
  }

  renderArtist() {
    const { name, artist } = this.props.event
    return artist && name !== artist && this.renderDetail('Artist', artist)
  }

  renderStartTime() {
    const { startsAt } = this.props.event
    return startsAt && this.renderDetail('Start', dayjs(startsAt).format('H:mm'))
  }

  renderPrice() {
    const { price } = this.props.event
    if (price && price > 0) {
      return this.renderDetail('Price', '$' + price)
    }
  }

  render() {
    if (this.state.hasError) {
      return <h5>Something went wrong.</h5>;
    }
    const { showSearch, name, detailsUrl } = this.props.event
    return (
      <div className={`${styles.event} ${styles.clickable}`}>
        <h5>{ name }</h5>
        <GenrePill event={this.props.event} />
        {detailsUrl && (
            <div className={ styles.website }>
              <a href={detailsUrl}>more details</a>
            </div>
        )}
        {this.renderArtist()}
        {this.renderStartTime()}
        {this.renderPrice()}
        {showSearch &&
          <SearchBox event={event} logSearchClick={this.logSearchClick}/>
        }
      </div>
    )
  }
}


class SearchBox extends Component {

  static propTypes = {
    event: PropTypes.shape({
      artist: PropTypes.string,
      name: PropTypes.string,
    }),
  }

  constructor(props) {
    super(props)
    this.state = { clicked: false };
  }

  handleClick = e => {
    this.setState({clicked: true})
  }

  logSearchClick = (site, term) => e => {
    ga('send', {
      hitType: 'event',
      eventCategory: 'Search Event',
      eventAction: 'click',
      eventLabel: site,
      eventValue: term,
    })
  }

  renderItem = (name, query, url) => (
    <div>
      <a
        onClick={this.logSearchClick(name, query)}
        href={url + query}
      >
        search {name}
      </a>
    </div>
  )

  render() {
    const { clicked } = this.state
    const { artist, name } = this.props.event
    const searchTerm = event.artist || event.name
    const query = encodeURIComponent(searchTerm)
    if (clicked) {
      return (
        <div className={styles.searchBox}>
          {this.renderItem('YouTube', query, 'https://www.youtube.com/results?search_query=')}
          {this.renderItem('SoundCloud', query, 'https://soundcloud.com/search/sets?q=')}
          {this.renderItem('BandCamp', query, 'https://bandcamp.com/search?q=')}
        </div>
      )
    } else {
      return <div onClick={this.handleClick} className={styles.searchBtn}>search</div>
    }
  }
}


class GenrePill extends Component {
  render() {
    const { event } = this.props
    if (!event.eventType) {
      return
    }
    const className = `${styles.genre} ${styles[event.eventType.toLowerCase()]}`
    return (
      <div className={className}>{event.eventType}</div>
    )
  }
}
