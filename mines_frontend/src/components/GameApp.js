import React from 'react';

import GameBoard from './GameBoard';

export default class GameApp extends React.Component {
  render() {
    const gameId = this.props.match.params.id;
    return (
      <section className="section">
        <div className="columns">
        <div className="column is-6 is-offset-3">
        <div className="box">
          <GameBoard gameId={gameId}/>
        </div>
        </div>
        </div>
      </section>
    );
  }
}
