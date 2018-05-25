from uuid import uuid4
import os

from sanic.views import HTTPMethodView
import sanic.response as res
from sanic import Sanic
import socketio

from sanic_cors import CORS

from pymongo import MongoClient

client = MongoClient(os.getenv('DB_HOST'), 27017)

db = client['record']

sio = socketio.AsyncServer()
app = Sanic()
sio.attach(app, socketio_path='/backend/socket.io')

@sio.on('recordsChange')
async def add_item(sid):
    await sio.emit('recordsChanged', list(db.records.find()))

class RecordCollection(HTTPMethodView):

    def post(self, request):
        record = request.json
        record['_id'] = str(uuid4())
        _id = db.records.insert_one(request.json)
        return res.json({'id': str(_id)})

    def options(self, request):
        return res.json({ })

    def get(self, request):
        return res.json({'data': list(db.records.find())})

class Record(HTTPMethodView):

    def get(self, request, _id):
        return res.text('I am get method and i\'m not implemented yet')

    def patch(self, request, _id):
        return res.text('I am patch method and i\'m not implemented yet')

    def delete(self, request, _id):
        deleted_id = db.records.find_one_and_delete({'_id': _id})
        return res.json({'id': str(deleted_id)})

    def options(self, request, _id):
        return res.json({ })

@app.route("/backend")
async def socket_connection(request):
    return json({ })

app.add_route(RecordCollection.as_view(), '/backend/collection')
app.add_route(Record.as_view(), '/backend/_/<_id>')

CORS(app, resources={
    r"/backend/collection": {"origins": "*"},
    r"/backend/_/*": {"origins": "*"}
})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)