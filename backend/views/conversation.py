from random import randint
import json
import os

from sanic.views import HTTPMethodView
import sanic.response as res

from pymongo import MongoClient

from kustomer_api.conversation import ConversationApi

client = MongoClient(os.getenv('DB_HOST'), 27017)

db = client['kustomer-api']
conversations = db['conversations']

customers = db['customers']

conversation_api = ConversationApi()

def get_random_customer_id():
    customers_list = list(customers.find())
    if customers_list:
        random_index = randint(0, len(customers_list) - 1)
        selected_customer = customers_list[random_index]
        return selected_customer.get('id')

class ConversationCollection(HTTPMethodView):
    def post(self, request):
        # conversation = request.json
        random_customer_id = get_random_customer_id()
        if random_customer_id:
            conversation_info = conversation_api.create_conversation(
                random_customer_id
            )
            conversation = conversation_info.get('data')
            conversation['_id'] = conversation.get('id')
            conversations.insert_one(conversation)
            return res.json({'data': conversation})
        return res.json({'data': ['Could not find customers.']})

    def get(self, request):
        conversation_list = list(conversations.find(
            {},
            {
                'attributes.name': 1,
                'attributes.channel': 1,
                'attributes.status': 1,
                'attributes.messageCount': 1,
                'attributes.preview': 1,
            }
        ).sort(
            [('attributes.updatedAt', -1)]
        ))

        conversation_filtered = list()
        for i, conv in enumerate(conversation_list):
            conv['attributes']['id'] = i
            conversation_filtered.append(conv.get('attributes'))

        return res.json({'data': conversation_filtered})

    def options(self, request):
        return res.json({ })

class ConversationDataMiner(HTTPMethodView):
    def post(self, request):
        last_conversation_modifyied = list(conversations.find(
            {}, {'attributes.updatedAt': 1}
        ).sort(
            [('attributes.updatedAt', -1)]
        ))

        if not len(last_conversation_modifyied):
            last_conversation_modified_date = None
        else:
            last_conversation_modified_date = (
                last_conversation_modifyied[0].get(
                    'attributes', {}
                ).get('updatedAt')
            )

        new_conversations = (
            conversation_api.get_conversations(
                newer_than=last_conversation_modified_date
            )
        )

        for new_conversation in new_conversations:
            new_conversation['_id'] = new_conversation.get('id')
            conversations.update_one(
                {'_id': new_conversation['_id']},
                {"$set": new_conversation},
                upsert=True
            )

        return res.json(len(new_conversations))

    def options(self, request):
        return res.json({ })
