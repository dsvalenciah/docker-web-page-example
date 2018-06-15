import request from 'superagent';


class ConversationsService {
  constructor() {
    // Dev mode prefix = 'http://localhost'
    // Build mode prefix = ''
    this.url = `${process.env.NODE_ENV === 'production' ? '' : 'http://localhost'}/backend`;
  }

  get(response, error) {
    request
      .get(this.url + '/conversationCollection')
      .end((err, res) => {
        if (!err) {
          response(res);
        } else {
          error(err);
        }
      });
  }
}

export default ConversationsService;