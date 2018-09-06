import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter as Router, Route } from "react-router-dom";

import GameApp from './components/GameApp';
import HomeApp from './components/HomeApp';

import './index.css'

const IndexApp = () => (
  <Router>
    <div>
      <Route exact path="/" component={HomeApp} />
      <Route exact path="/game/:id" component={GameApp} />
    </div>
  </Router>
);


ReactDOM.render(
  <IndexApp />,
  document.getElementById("app")
);
