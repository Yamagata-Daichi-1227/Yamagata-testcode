"""
ユーザー作成APIレスポンスをSlackに送信する

NOTE:
    Slack Tokenの権限はBot Tokenのchat:writeを付与
"""
import os
import json

import sys
sys.path.append('../saas')

import saas.dev.user as dev
import saas.util.get_credential as credentials_store

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

class Notification:
    def __init__(self, token):
        self.token = token
        self.client = WebClient(token=self.token)  

    def send_msg(self, channel_id, json_data):
        json_dump = json.dumps(json_data, ensure_ascii=False, indent=4)

        try:
            if json_data['action'] == 'create_user':
                message = f'ユーザーが作成されました。\n\n```{json_dump}```'
            elif json_data['action'] == 'delete_user':
                message = f'ユーザーが削除されました。\n\n```{json_dump}```'
            elif json_data['action'] == 'add_role':
                message = f'ユーザーにロールが割り当てられました。\n\n```{json_dump}```'
            elif json_data['action'] == 'remove_role':
                message = f'ユーザーのロールが削除されました。\n\n```{json_dump}```'
            res = self.client.chat_postMessage(
                channel = channel_id, 
                text = message
            )
        except SlackApiError as e:
            print(f"Error uploading file: {e}")
        pass

def send_msg(event, context=''):
    user_info = event

    slack_channel_id = credentials_store.get_secret('slack_channel_id')
    slack_token = credentials_store.get_secret('slack_token')
    slack = Notification(slack_token)
    slack.send_msg(slack_channel_id, user_info)

if __name__ == '__main__':
    send_msg({})
