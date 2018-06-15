from uuid import uuid4
import os

from views.customer import CustomerCollection, CustomerDataMiner
from views.conversation import ConversationCollection, ConversationDataMiner

from sanic.views import HTTPMethodView
import sanic.response as res
from sanic import Sanic

from sanic_cors import CORS

from pymongo import MongoClient

client = MongoClient(os.getenv('DB_HOST'), 27017)

db = client['record']

app = Sanic()

app.add_route(CustomerCollection.as_view(), '/backend/customerCollection')
app.add_route(CustomerDataMiner.as_view(), '/backend/customerDataMiner')

app.add_route(
    ConversationCollection.as_view(), '/backend/conversationCollection'
)
app.add_route(
    ConversationDataMiner.as_view(), '/backend/conversationDataMiner'
)

CORS(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)