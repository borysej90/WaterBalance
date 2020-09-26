import os
import datetime
from collections import defaultdict

import requests
from telegram.ext import BasePersistence

BASE_URL = os.environ['API_URL']


class ApiPersistence(BasePersistence):
    """
    ApiPersistence used to save different bot data in database using WaterBalanceAPI endpoints.
    """

    def get_chat_data(self):
        pass

    def update_chat_data(self, chat_id, data):
        pass

    def get_bot_data(self):
        pass

    def update_bot_data(self, data):
        pass

    def get_conversations(self, name):
        pass

    def update_conversation(self, name, key, new_state):
        pass

    def __init__(self):
        super().__init__(store_user_data=True, store_bot_data=False, store_chat_data=False)

    def get_user_data(self):
        data = defaultdict(dict)

        response = requests.get(BASE_URL + 'bot/user/load/all')
        result = response.json()

        for user in result:
            del user['has_reminding']

            if {'start_silence', 'end_silence'} <= set(user):
                user['start_silence'] = datetime.time.fromisoformat(user['start_silence'])
                user['end_silence'] = datetime.time.fromisoformat(user['end_silence'])

            user_id = user.pop('id')
            data[user_id] = user

        # print(data)
        return data

    def update_user_data(self, user_id, data):
        if data.get('changed', False):
            del data['changed']
            user = self._convert_user_dict_keys(data)

            requests.post(BASE_URL + f'bot/user/save/{user_id}', json=user,
                          headers={'Content-type': 'application/json'})

            data['changed'] = False

    @staticmethod
    def _convert_user_dict_keys(data):
        """
        Modifies dictionary keys names to use in API. Function **DOES NOT** modify the original dictionary.

        Args:
            data(dict): dictionary containing user data.
        """

        user = data.copy()

        if 'start_silence' in user:
            user['start_silence'] = user['start_silence'].isoformat()

        if 'end_silence' in user:
            user['end_silence'] = user['end_silence'].isoformat()

        if 'job' in user:
            user['has_reminding'] = True
            del user['job']
        else:
            user['has_reminding'] = False

        return user
