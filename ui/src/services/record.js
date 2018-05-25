import request from 'superagent';


class Record {
  constructor() {
    // Dev mode prefix = 'http://localhost'
    // Build mode prefix = ''
    this.url = 'http://localhost/backend';
  }

  get(response, error) {
    request
      .get(this.url)
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
      .post(this.url)
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