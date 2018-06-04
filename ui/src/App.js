import React, { Component } from 'react';

import Record from './services/record';
import io from "socket.io-client";

const recordService = new Record();
const socket = io(
  `${process.env.NODE_ENV === 'production' ? '' : 'http://localhost'}`,
  {path: '/backend/socket.io'}
);

socket.on('connect', () =>{
  console.log('Socket id ' + socket.id);
});

class App extends Component {
  constructor(props) {
    super(props)
    socket.on('recordsChanged', (records)=> this.setState({ records }))
  }

  state = {
    data: null,
    record: '',
    records: [],
  }

  handleButtonClick() {
    const record = this.state.record;
    if (record) {
      recordService.post(
        { record },
        response => {
          socket.emit('recordsChange');
          this.setState({record: ''});
        },
        error => console.log(error)
      );
    } else {
      console.log('No data');
    }
  }

  componentDidMount() {
    recordService.get(
      response => this.setState({ records: response.body.data }),
      error => this.setState({ records: [] })
    );
  }

  handleInputChange(record) {
    this.setState({ record })
  }

  handleRecordClick(id) {
    recordService.delete(
      id,
      response => socket.emit('recordsChange'),
      error => console.log(error)
    );
  }

  render() {
    return (
      <div className="App">
        <center>
          <div style={{ display: 'inline-block' }}>
            <p>Something: </p>
          </div>
          <div style={{ display: 'inline-block' }}>
            <input 
              onChange={(e) => this.handleInputChange(e.target.value)}
              type="text"
              onKeyPress={(e) => e.key === 'Enter' && this.handleButtonClick()}
              value={this.state.record}
            />
          </div>
          <button
            onClick={() => this.handleButtonClick()}>
            Click
          </button>
        </center>
        <ul>
          {this.state.records.map(r => (
            <li
              key={r._id}
              onClick={() => this.handleRecordClick(r._id)}>
              {r.record}
            </li>
          ))}
        </ul>
      </div>
    );
  }
}

export default App;
