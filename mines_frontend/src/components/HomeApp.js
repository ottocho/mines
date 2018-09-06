
import React from 'react';
import { Redirect } from 'react-router'

import axios from 'axios';

export default class HomeApp extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      userName: 'anonymous',
      width: 10,
      height: 10,
      nMinesAll: 8,
      newGame: false,
      gameId: 0
    };
  }

  changeUserName(event) {
    this.setState({
      userName: event.target.value
    });
  }

  changeWidth(event) {
    this.setState({
      width: event.target.value
    });
  }

  changeHeight(event) {
    this.setState({
      height: event.target.value
    });
  }

  changeMines(event) {
    this.setState({
      nMinesAll: event.target.value
    });
  }

  onSubmit(event) {
    event.preventDefault();
    const {userName,width,height,nMinesAll} = this.state;
    const postBody = {
      userName: userName,
      height: height,
      width: width,
      nMinesAll: nMinesAll
    };
    const postUrl = 'http://v.com:8000/api/game/new';
    console.log(postUrl);
    console.log(postBody);
    axios.post(postUrl, postBody)
    .then(res => {
      console.log(res);
      const result = res.data;
      if (result.ret !== 0) {
        alert('error ' + result.ret);
        return;
      }
      const requestValue = res.data.value;
      const gameId = requestValue.gameId;
      this.setState({
        newGame: true,
        gameId: gameId
      })
    })
  }

  render() {
    if (this.state.newGame) {
      // had start new game; redirect to game page
      const toUrl = '/game/' + this.state.gameId;
      return <Redirect to={toUrl} />
    }

    // main page
    return (
      <section className="section">

        <div className="columns">
        <div className="column is-one-third is-offset-one-third">
        <div className="box">

          <h1 className="title">
            Minesweeper
          </h1>
          <p className="subtitle">
            Enjoy <i className="far fa-smile-wink"></i> <i className="fas fa-gamepad"></i>
          </p>

          <form onSubmit={(e)=>{this.onSubmit(e)}}>
            <div className="field">
              <label className="label">Your Name</label>
              <div className="control is-expanded has-icons-left">
                <input className="input" type="text" value={this.state.userName} onChange={(e)=>{this.changeUserName(e)}} placeholder="Nickname" />
                <span className="icon is-small is-left">
                  <i className="fas fa-user"></i>
                </span>
              </div>
            </div>
            <div className="field is-horizontal">
              <div className="field-body">
                <div className="field">
                  <label className="label">Width</label>
                  <p className="control is-expanded has-icons-left">
                    <input className="input" type="number" value={this.state.width} onChange={(e)=>{this.changeWidth(e)}}/>
                    <span className="icon is-small is-left">
                      <i className="fas fa-text-width"></i>
                    </span>
                  </p>
                </div>
                <div className="field">
                  <label className="label">Height</label>
                  <p className="control is-expanded has-icons-left has-icons-right">
                    <input className="input" type="number" value={this.state.height} onChange={(e)=>{this.changeHeight(e)}}/>
                    <span className="icon is-small is-left">
                      <i className="fas fa-text-height"></i>
                    </span>
                  </p>
                </div>
                <div className="field">
                  <label className="label">Mines</label>
                  <p className="control is-expanded has-icons-left has-icons-right">
                    <input className="input" type="number" value={this.state.nMinesAll} onChange={(e)=>{this.changeMines(e)}}/>
                    <span className="icon is-small is-left">
                      <i className="fas fa-bomb"></i>
                    </span>
                  </p>
                </div>
              </div>
            </div>
            <div className="field is-grouped is-right" style={{'margin-top': '1.5rem'}}>
              <div className="control">
                <button className="button is-medium is-success" type="submit" >Play</button>
              </div>
            </div>
          </form>
        </div>
        </div>
        </div>
      </section>
    );
  }
}
