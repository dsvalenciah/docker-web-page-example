import React, { Component } from 'react';

import Record from './services/record';

const record = new Record();

class App extends Component {
  state = {
    data: null,
    something: '',
  }

  componentDidMount() {
    record.get(
      response => this.setState({ data: response.body }),
      error => this.setState({ data: 'Error' })
    );
  }

  handleClick() {
    const something = this.state.something;
    if (something) {
      record.post(
        { something },
        response => console.log(response),
        error => console.log(error)
      )
    } else {
      console.log('No data');
    }
  }

  handleChange(something) {
    this.setState({ something })
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
              onChange={(e) => this.handleChange(e.target.value)}
              type="text"
            />
          </div>
          <button
            onClick={() => this.handleClick()}>
            Click
          </button>
        </center>
        <pre>{JSON.stringify(this.state.data, undefined, 4)}</pre>
      </div>
    );
  }
}

export default App;
