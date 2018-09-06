import React from 'react';
import axios from 'axios'

import GameBrick from './GameBrick';
import GameHeader from './GameHeader';

// TODO fix to dev/prod
const apiServer = 'http://v.com:8000'

/*
const gameStatusMap = {
  10: 'playing',
  20: 'win',
  30: 'lost'
}
*/

export default class GameBoard extends React.Component {
  state = {
    gameId: this.props.gameId,
    nMinesAll: 0,
    nMinesLeft: 0,
    status: 10,
    bricks: [],
  };

  componentDidMount() {
    const gameId = this.state.gameId;
    const getUrl = `${apiServer}/api/game/get/${gameId}`;
    axios.get(getUrl)
    .then(res => {
      const result = res.data;
      if (result.ret !== 0) {
        console.log('error ' + result.ret);
        return;
      }
      const {bricks, nMinesAll, nMinesLeft, status} = res.data.value;
      this.setState({
        bricks, nMinesAll, nMinesLeft, status
      });
    })
  }

  onLeftClick(x, y) {
    const brick = this.state.bricks[x][y];
    if (brick.isDug || brick.isFlagged || this.state.status !== 10) {
      return;
    }
    const gameId = this.state.gameId;
    const postUrl = `${apiServer}/api/game/${gameId}/left_click/${x}/${y}`;
    axios.post(postUrl)
    .then(res => {
      const result = res.data;
      if (result.ret !== 0) {
        console.log(`error ${result.ret}: ${result.text}`);
        return;
      }
      const newStatus = res.data.value.game.status;
      const newBricks = this.state.bricks.slice();
      res.data.value.bricks.map((brickInfo) => {
        const nx = brickInfo.x;
        const ny = brickInfo.y;
        newBricks[nx][ny].isDug = true;
        return null;
      });
      this.setState({
        status: newStatus,
        bricks: newBricks
      });
    })

  }

  onRightClick(e, x, y) {
    e.preventDefault();
    const brick = this.state.bricks[x][y];
    if (brick.isDug || this.state.status !== 10) {
      return;
    }
    const gameId = this.state.gameId;
    const postUrl = `${apiServer}/api/game/${gameId}/right_click/${x}/${y}`;
    axios.post(postUrl)
    .then(res => {
      const result = res.data;
      if (result.ret !== 0) {
        console.log(`error ${result.ret}: ${result.text}`);
        return;
      }
      const newNMinesLeft = res.data.value.game.nMinesLeft;
      const newBricks = this.state.bricks.slice();
      newBricks[x][y].isFlagged = res.data.value.brick.isFlagged;
      this.setState({
        nMinesLeft: newNMinesLeft,
        bricks: newBricks
      });
    })
  }

  render_brick(brickRow, brick) {
    const { status } = this.state;
    return (
      <div key={brick.x * brickRow.length + brick.y}>
        <GameBrick
          key={brick.x * brickRow.length + brick.y}
          onLeftClick={() => this.onLeftClick(brick.x, brick.y)}
          onRightClick={(e) => this.onRightClick(e, brick.x, brick.y)}
          brick={brick}
          status={status}
        />
      </div>
    )
  }

  render_row(brickRow) {
    return brickRow.map((brick) => {
      return (
          this.render_brick(brickRow, brick)
      )
    })
  }

  render_board(bricks) {
    return (
      bricks.map((brickRow) => {
        return (
         <div className="game-brick-row">
            {this.render_row(brickRow)}
         </div>
        )
      })
    )
  }

  render() {
    const { nMinesAll, nMinesLeft, status } = this.state;
    return (
      <div>
        <GameHeader nMinesAll={nMinesAll} nMinesLeft={nMinesLeft} status={status} />
        <div className="game-board">
          { this.render_board(this.state.bricks) }
        </div>
      </div>
    );
  }
}
