import React from 'react'
import styles from 'styles/toolbar.css'


module.exports = ({ children }) => (
  <div className={styles.toolbar}>
    <div className="container">
      { children }
    </div>
  </div>
)
