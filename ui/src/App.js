import React, { Component } from 'react';

import ConversationsService from './services/conversation';

import { BootstrapTable, TableHeaderColumn } from 'react-bootstrap-table';
import '../node_modules/react-bootstrap-table/dist/react-bootstrap-table-all.min.css';

const conversationsService = new ConversationsService();

class App extends Component {
  constructor(props) {
    super(props)
  }

  state = {}

  handlerClickCleanFiltered() {
    this.refs.name1.cleanFiltered();
    this.refs.name2.cleanFiltered();
    this.refs.quality.cleanFiltered();
    this.refs.price.cleanFiltered();
    this.refs.satisfaction.cleanFiltered();
    this.refs.inStockDate.cleanFiltered();
  }

  componentDidMount() {
    conversationsService.get(
      (res) => this.setState({ conversations: res.body.data}),
      (err) => console.log(err)
    )
  }

  render() {
    return (
      <div className="App">
      <BootstrapTable ref='table' data={ this.state.conversations }>
        <TableHeaderColumn isKey dataField='id'>
          Product ID
          <br/>
            <a
              onClick={ this.handlerClickCleanFiltered.bind(this) }
              style={ { cursor: 'pointer' } }
            >
            clear filters
          </a>
        </TableHeaderColumn>
        <TableHeaderColumn
          dataField='name'
          filter={ { type: 'TextFilter', placeholder: 'Please enter a value' } }
        >
          Name
        </TableHeaderColumn>
        <TableHeaderColumn
          dataField='channels'
          filter={ { type: 'RegexFilter', placeholder: 'Please enter a regex' } }
        >
          Channels
        </TableHeaderColumn>
        <TableHeaderColumn
          dataField='status'
          filter={ { type: 'RegexFilter', placeholder: 'Please enter a regex' } }
        >
          Status
        </TableHeaderColumn>
        <TableHeaderColumn
          dataField='messageCount'
          filter={ { type: 'RegexFilter', placeholder: 'Please enter a regex' } }
        >
          MessageCount
        </TableHeaderColumn>
        <TableHeaderColumn
          dataField='preview'
          filter={ { type: 'RegexFilter', placeholder: 'Please enter a regex' } }
        >
          Preview
        </TableHeaderColumn>
      </BootstrapTable>
      </div>
    );
  }
}

export default App;
