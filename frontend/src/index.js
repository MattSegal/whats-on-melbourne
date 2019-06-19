// @flow
import React from 'react'
import ReactDOM from 'react-dom'
import { Provider } from 'react-redux'
import styled from 'styled-components'

import { Layout } from 'components'
import { Map, Sidebar } from 'containers'
import { store } from 'state'

import './styles.css'

const App = () => (
  <Provider store={store}>
    <React.Fragment>
      <Header>What's On Melbourne</Header>
      <Layout>
        <Map />
      </Layout>
      <Sidebar />
    </React.Fragment>
  </Provider>
)

const Header = styled.h1`
  height: 36px;
  box-sizing: border-box;
  padding: 1rem;
  margin: 0;
  line-height: calc(36px - 2rem);
  font-size: 20px;
  color: #fff;
  background: #333;
`

const root = document.getElementById('app')
if (root) ReactDOM.render(<App />, root)
