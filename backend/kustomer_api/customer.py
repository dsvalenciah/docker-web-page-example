import json
import sys

from kustomer_api.exceptions.base import RequestError
from kustomer_api.utils.random_customer import random_customer

import requests as req


class CustomerApi():
    """Deal with Kustomer API."""
    def __init__(self):
        self.load_config()

    def load_config(self):
        try:
            with open('kustomer_api/config.json') as config_file:
                config = json.load(config_file)
                self.api_key = config.get('api_key')
                self.api_url = config.get('api_url')
        except (OSError, IOError) as e:
            raise e
            sys.exit(0)

    def request(self, method, endpoint, data={}):
        """Does a request to Kustomer API."""
        url = f'{self.api_url}{endpoint}'
        data = json.dumps(data)
        headers = {
            'content-type': 'application/json',
            'Authorization': f'Bearer {self.api_key}',
        }
        return req.request(method, url, data=data, headers=headers)

    def create_customer(self, customer_data=None):
        """Create a new customer."""
        if not customer_data:
            customer_data = random_customer()

        res = self.request('POST', '/customers', data=customer_data)

        if res.status_code != 201:
            raise RequestError(['Error when request customer creation.'])
        return res.json()

    def get_customers(self, newer_than=None):
        """Get all customers."""
        res = {"data": True}
        page = 1
        customers = list()
        while res.get('data'):
            res = self.request(
                'GET', f'/customers?pageSize=50&page={page}'
            ).json()
            if newer_than:
                for new_customer in res.get('data'):
                    new_customer_updated_date = (
                        new_customer.get('attributes', {}).get('updatedAt')
                    )
                    if new_customer_updated_date <= newer_than:
                        res = {"data": False}
                        break
                    customers.append(new_customer)
            else:
                customers.extend(res.get('data'))
            page += 1

        return customers
