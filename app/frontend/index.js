import ReactDOM from 'react-dom'
import React, { Component } from 'react'
import { Provider } from 'react-redux'
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';

import { store } from 'state'
import MapContainer from 'containers/map'
import AboutContainer from 'containers/about'
import ListContainer from 'containers/list'
import HeaderMenu from 'components/header-menu'

class App extends Component {
  render() {
    return (
      <Provider store={store}>
        <div>
          <Router>
            <div>
              <HeaderMenu />
              <Switch>
                <Route exact path="/" component={MapContainer} />
                <Route path="/list" component={ListContainer} />
                <Route path="/about" component={AboutContainer} />
                <Route component={() => <div><h1>Not Found</h1></div>} />
              </Switch>
            </div>
          </Router>
        </div>
      </Provider>
    )
  }
}


ReactDOM.render(<App/>, document.getElementById('app'))
