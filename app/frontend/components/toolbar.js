import React, { Component } from 'react'
import { connect } from 'react-redux'

import styles from 'styles/toolbar.css'
import { TOOLBAR } from 'consts'
import { actions } from 'state'
import ToolbarWrapper from 'components/display/toolbar-wrapper'
import GenreDropDown from './dropdowns/genres'

const dropdowns = {
  [TOOLBAR.GENRES]: GenreDropDown,
}


class Toolbar extends Component {

  render() {
    const { openToolbar, closeToolbar, toolbarSelection } = this.props
    const DropDown = dropdowns[toolbarSelection]
    const action = toolbarSelection ? closeToolbar : openToolbar
    return (
     <ToolbarWrapper>
        <div className={styles.options}>
          <span
            className={styles.option}
            onClick={() => action(TOOLBAR.GENRES)}>Genres</span>
        </div>
        <div className={`${styles.dropdown} ${toolbarSelection && styles.open}`}>
            {toolbarSelection && <DropDown/>}
        </div>
      </ToolbarWrapper>
    )
  }
}


const mapStateToProps = state => ({
  toolbarSelection: state.selected.toolbar,
})
const mapDispatchToProps = dispatch => ({
  closeToolbar: () => dispatch(actions.selections.toolbar.close()),
  openToolbar: s => dispatch(actions.selections.toolbar.open(s)),
})
module.exports = connect(mapStateToProps, mapDispatchToProps)(Toolbar)
