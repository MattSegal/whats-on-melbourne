import ReactDOM from 'react-dom'
import React, { Component } from 'react'
import { Link } from 'react-router-dom';

import styles from 'styles/header.css'


const Portal = ({ children, domNode }) =>
  ReactDOM.createPortal(children, domNode)


export default class HeaderMenu extends Component {

  constructor(props) {
    super(props)
    this.headerNode = document.getElementById('header-root')
  }

  render() {
    return (
      <Portal domNode={this.headerNode}>
        <div className={styles.header}>
          <Link to="/">Map</Link>
          <Link to="/list">List</Link>
          <Link to="/about">About</Link>
        </div>
      </Portal>
    )
  }
}
