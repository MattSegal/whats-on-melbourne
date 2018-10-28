import React from 'react'

import ToolbarWrapper from 'components/display/toolbar-wrapper'
import styles from 'styles/toolbar.css'


module.exports = () => (
  <div>
    <ToolbarWrapper></ToolbarWrapper>
    <div className="container" style={{marginTop: '1rem'}}>
      <h2>About WOM</h2>
      <p>
        This website was built to answer the question "what's going on in Melbourne tonight"?
      </p>
      <p>
        It's a side-project of <a href="https://github.com/MattSegal">mine</a> that I developed because
        I spent of lot of time searching for gigs online.
      </p>
      <p>
        I get event data from the following sources:
      </p>
      <ul>
        <li>
          <a href="http://www.beat.com.au/gig-guide">
            Beat Magazine Gig Guide
          </a>
        </li>
        <li>
          <a href="https://whatson.melbourne.vic.gov.au/Whatson/Pages/Whatson.aspx">
            What's On - City of Melbourne
          </a>
        </li>
        <li>
          <a href="http://www.888pl.com.au/">
            888 Poker League
          </a>
        </li>
      </ul>
      <p>
        You can contact me at <a href="mailto:mattdsegal@gmail.com">mattdsegal@gmail.com</a>.
        Let me know if you have any comments or ideas.
      </p>
    </div>
  </div>
)
