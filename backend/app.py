from uuid import uuid4
import os

from sanic.views import HTTPMethodView
from sanic import response
from sanic import Sanic

from sanic_cors import CORS

from pymongo import MongoClient

client = MongoClient(os.getenv('DB_HOST'), 27017)

db = client['record']

app = Sanic()

class Record(HTTPMethodView):

    def get(self, request):
        return response.json({'data': list(db.records.find())})

    def post(self, request):
        record = request.json
        record['_id'] = str(uuid4())
        _id = db.records.insert_one(request.json)
        return response.json({'id': str(_id)})

    def options(self, request):
        return response.json({ })

    def put(self, request):
        # db.records.find_one_and_update()
        raise NotImplemented()

    def delete(self, request):
        # db.records.find_one_and_delete()
        raise NotImplemented()

app.add_route(Record.as_view(), '/backend')

CORS(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)