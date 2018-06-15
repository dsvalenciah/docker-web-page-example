import json
import os

from sanic.views import HTTPMethodView
import sanic.response as res

from pymongo import MongoClient

from kustomer_api.customer import CustomerApi

client = MongoClient(os.getenv('DB_HOST'), 27017)

db = client['kustomer-api']
customers = db['customers']

customer_api = CustomerApi()

class CustomerCollection(HTTPMethodView):
    def post(self, request):
        # customer = request.json
        customer_info = customer_api.create_customer()
        customer = customer_info.get('data')
        customer['_id'] = customer.get('id')
        customers.insert_one(customer)
        return res.json({'data': customer})

    def get(self, request):
        return res.json({'data': list(customers.find().sort(
            [('attributes.updatedAt', -1)]
        ))})

    def options(self, request):
        return res.json({ })

class CustomerDataMiner(HTTPMethodView):
    def post(self, request):
        last_customer_modifyied = list(customers.find(
            {}, {'attributes.updatedAt': 1}
        ).sort(
            [('attributes.updatedAt', -1)]
        ))

        if not len(last_customer_modifyied):
            last_customer_modified_date = None
        else:
            last_customer_modified_date = (
                last_customer_modifyied[0].get(
                    'attributes', {}
                ).get('updatedAt')
            )

        new_customers = (
            customer_api.get_customers(newer_than=last_customer_modified_date)
        )

        for new_customer in new_customers:
            new_customer['_id'] = new_customer.get('id')
            customers.update_one(
                {'_id': new_customer['_id']},
                {"$set": new_customer},
                upsert=True
            )

        return res.json(len(new_customers))

    def options(self, request):
        return res.json({ })
