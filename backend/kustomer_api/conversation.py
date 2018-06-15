import json

from kustomer_api.exceptions.base import RequestError
from kustomer_api.utils.random_conversation import random_conversation

import requests as req

class ConversationApi():
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

    def create_conversation(self, customer_id, conversation_data=None):
        """reate a new conversation for an a customer."""
        if not conversation_data:
            conversation_data = random_conversation()

        endpoint = f'/customers/{customer_id}/conversations'
        res = self.request('POST', endpoint)
        conversation_id = res.json().get('data', {}).get('id')

        if res.status_code != 201:
            raise RequestError(['Error when request empty conversation create.'])

        endpoint = f'/conversations/{conversation_id}/messages'
        res = self.request('POST', endpoint, data=conversation_data)

        if res.status_code != 201:
            raise RequestError(['Error when request conversation create.'])
        return res.json()

    def get_conversations(self, newer_than):
        """Get all conversations."""
        res = {"data": True}
        page = 1
        conversations = list()
        while res.get('data'):
            res = self.request(
                'GET', f'/conversations?pageSize=50&page={page}'
            ).json()
            if newer_than:
                for new_conversation in res.get('data'):
                    new_conversation_updated_date = (
                        new_conversation.get('attributes', {}).get('updatedAt')
                    )
                    if new_conversation_updated_date <= newer_than:
                        res = {"data": False}
                        break
                    conversations.append(new_conversation)
            else:
                conversations.extend(res.get('data'))
            page += 1

        return conversations

