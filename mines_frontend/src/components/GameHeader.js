import React from 'react';
import { Link } from "react-router-dom";

export default class GameHeader extends React.Component {
  helper() {
    const { status } = this.props;
    let msg;
    if (status === 10) {
      msg = ':)';
    }
    else if (status === 20) {
      msg = 'You win!';
    }
    else if (status === 30) {
      msg = 'You lost ;(';
    }
    return msg;
  }

  render() {
    /*
    const gameStatusMap = {
      10: 'playing',
      20: 'win',
      30: 'lost'
    }
    */
    const { nMinesAll, status } = this.props;
    const msg = this.helper();
    return (
      <div className="game-header">
        <h1 class="title">{msg}</h1>

        <h2 class="subtitle">{nMinesAll} Mines</h2>

        {(status!==10?<Link to='/'><span className="tag is-warning is-medium">Play again?</span></Link>:'')}
        </div>
    );
  }
}
