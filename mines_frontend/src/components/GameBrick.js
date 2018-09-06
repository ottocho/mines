import React from 'react';

export default class GameBrick extends React.Component {
  helper() {
    const { brick, status } = this.props;

    /// playing
    if (status === 10) {
      if (!brick.isDug) {
        if (brick.isFlagged) {
          return {
            value: '🚩',
            className: ' is-flagged not-dug'
          }
        } else {
          return {
            value: '',
            className: ' not-dug'
          }
        }
      } else {
        if (brick.nNearbyMines === 0) {
          return {
            value: '',
            className: ''
          }
        } else {
          return {
            value: brick.nNearbyMines,
            className: ''
          }
        }
      }
    }

    /// win
    if (status === 20) {
      if (brick.isMine) {
        if (brick.isDug) {
          return {
            value: '🚩',
            className: ' is-flagged not-dug'
          }
        }
        return {
          value: '🚩',
          className: ' is-flagged'
        }
      } else if (brick.nNearbyMines === 0) {
        return {
          value: '',
          className: ' '
        }
      } else {
        return {
          value: brick.nNearbyMines,
          className: ' '
        }
      }
    }

    /// lost
    if (status === 30) {
      if (!brick.isDug) {
        if (brick.isMine) {
          if (brick.isFlagged) {
            return {
              value: '🚩',
              className: ' is-flagged'
            }
          }
          return {
            value: '💣',
            className: ' is-mine'
          }
        } else {
          if (brick.isFlagged) {
            return {
              value: '❌',
              className: ' is-mine'
            }
          } else {
            return {
              value: '',
              className: ' not-dug'
            }
          }
        }
      } else {
        if (brick.isMine) {
          return {
            value: '🔥',
            className: ' is-mine'
          }
        } else if (brick.nNearbyMines === 0) {
          return {
            value: '',
            className: ' '
          }
        } else {
          return {
            value: brick.nNearbyMines,
            className: ' '
          }
        }
      }
    }
  }

  render() {
    const { onLeftClick, onRightClick} = this.props;
    const tpl = this.helper();
    const v = tpl.value;
    const className = "game-brick " + tpl.className;
    return (
      <div
        className={className}
        onClick={onLeftClick}
        onContextMenu={onRightClick}
      >
        {v}
      </div>
    );
  }
}
