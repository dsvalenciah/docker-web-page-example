import request from 'superagent';


class Record {
  constructor() {
    // Dev mode prefix = 'http://localhost'
    // Build mode prefix = ''
    this.url = `${process.env.NODE_ENV === 'production' ? '' : 'http://localhost'}/backend`;
  }

  get(response, error) {
    request
      .get(this.url + '/collection')
      .end((err, res) => {
        if (!err) {
          response(res);
        } else {
          error(err);
        }
      });
  }

  delete(id, response, error) {
    request
      .delete(`${this.url}/_/${id}`)
      .end((err, res) => {
        if (!err) {
          response(res);
        } else {
          error(err);
        }
      });
  }

  post(data, response, error) {
    request
      .post(this.url + '/collection')
      .send(data)
      .end((err, res) => {
        if (!err) {
          response(res);
        } else {
          error(err);
        }
      });
  }
}

export default Record;