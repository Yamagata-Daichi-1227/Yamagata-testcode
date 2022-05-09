"""
Datadogのユーザーを作成し、作成したユーザーのroleを追加するためのモジュール
TODO:
    契約種別・部門により作成したユーザーを適切なroleに割り当てる
    現在はdatadog standard roleに割り当てたい
    ユーザー招待メールを送信する
"""
import os
import sys
import json
import ast

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from onelogin.main import OneLoginUser

from util.general import random_string
import util.get_credential as credentials_store

import requests

# from saas.onelogin.main import OneLoginUser

# sys.path.append('../')
# import util.get_credential as credentials_store

# import requests

class Datadog:
    """
    Datadogのユーザーを作成し、作成したユーザーをグループに追加
    Args:
        いろいろ
        user_info(dict): ユーザー情報
    """
    def __init__(self, api_key, application_key, user_info):
        self.saas_name = 'datadog'
        self.api_key = api_key
        self.application_key = application_key

        self.session = requests.Session()
        self.base_url = 'https://api.datadoghq.com/api/v2'
        self.session.headers = {
            'DD-API-KEY':self.api_key,
            'DD-APPLICATION-KEY':self.application_key,
            "Accept": "application/json",
            'Content-Type': 'application/json'
        }
        self.contract_type = user_info['contract_type']
        self.onelogin_role =user_info['onelogin_role_id']
        
        self.user_info = self.__process_user_info(user_info)
        self.user_id = None
        self.roles_id_info = self.__user_roles_id_info()
        self.roles_id_list = self.__process_user_roles_info()[1]
    

    def __process_user_info(self, user_info):
        """
        ユーザー作成のためにユーザー情報を整形
        Args:
            user_info(dict): ユーザー情報
        Returns:
            (dict) 整形されたユーザー情報
        """
        ret_user_info = {
            'data': {
                'type': 'users',
                'attributes':{
                 'name': f"{user_info['firstname']} {user_info['lastname']}",
                 'email': f"{user_info['email']}"
                },         
            }
        }        
        return ret_user_info

    def __user_roles_id_info(self):
        """
        roles ID情報
        Returns:
            (dict) roles ID情報
        """
        try: 
            endpoint = '/roles?page[size]=10&page[number]=0&sort=name'
            url = self.base_url + endpoint
            r = self.session.get(url) #流用できる
            if r.status_code == 200:
                res = r.json()
                for val in res['data']:
                    if val['attributes']['name'] == 'Datadog Standard Role':
                        res = val['id']
                return res 
            else:
                return {
                    'ok': False,
                    'saas_name': self.saas_name,
                    'status_code': r.status_code
               
                }
        except Exception: 
            err_msg = 'Error: Create User' 
            return { 
                'ok': False, 
                'saas_name': self.saas_name, 
                'err_msg': err_msg
            } 
            
    def __process_user_roles_info(self):
        """
        ユーザーをrolesに追加するためにユーザー情報を整形
        Args:
            user_id(str): ユーザーID
        Returns:
            (dict): 整形されたユーザー情報
        """
        ret_user_info = {
              "data": {
                    #user_idが必須  
                     "id": self.user_id,
                     "type": "users"
         }
        }

        roles_id_list = []
        if self.contract_type in ['正社員', 'インターン','業務委託']:
            roles_id_list.append(self.roles_id_info)
        
        return ret_user_info, roles_id_list

    def create_user(self):
        """
        ユーザー作成
        Returns:
            (dict)　ユーザー情報
        """
        try:
            endpoint = '/users'
            url = self.base_url + endpoint
            
            r = self.session.post(url, json=self.user_info) 
            
            if r.status_code in (200, 201, 409):
                res = r.json()
                res['ok'] = True
                self.user_id = res['data']['id']
                return res
            else:
                return {
                    'ok': False,
                    'err_msg': r.json()['details'],
                    'saas_name': self.saas_name,
                    'status_code': r.status_code
                }

        except Exception:
            err_msg = 'Error: Create User'
            return {
                'ok': False,
                'saas_name': self.saas_name,
                'err_msg': err_msg
            }

    def add_user_roles(self, roles_id):
        """
        ユーザーのrolesを追加
        Args:
            roles_id(str): roles_ID
        Returns:
            (dict) roles情報
        """
        try: 
            user_info = self.__process_user_roles_info()[0]
            endpoint = f'/roles/{roles_id}/users'
            url = self.base_url + endpoint
            r = self.session.post(url, json=user_info) #流用できる
            if r.status_code in (200, 201, 204, 409):
                res = r.json()
                res['ok'] = True
                res['saas_name'] = self.saas_name
                return res 
            else:
                return {
                    'ok': False,
                    'saas_name': self.saas_name,
                    'status_code': r.status_code
                }

        except Exception:
            err_msg = 'Error: Create Roles'
            return {
                'ok': False,
                'saas_name': self.saas_name,
                'err_msg': err_msg
            }

    def invite_user(self,user_info):
        """
        新規ユーザにメールを送信する
        Args:
            roles_id(str): roles_ID
        Returns:
            (dict) roles情報
        """
        try: 
            endpoint = '/user_invitations'
            url = self.base_url + endpoint
            r = self.session.post(url, json=user_info) #流用できる
            if r.status_code in (200, 201, 409):
                res = r.json()
                res['ok'] = True
                res['saas_name'] = self.saas_name
                return res 
            else:
                return {
                    'ok': False,
                    'saas_name': self.saas_name,
                    'status_code': r.status_code
                }

        except Exception:
            err_msg = 'Error: Create Roles'
            return {
                'ok': False,
                'saas_name': self.saas_name,
                'err_msg': err_msg
            }


class OneloginRole:
    """
    Datadogのユーザーを作成し、作成したユーザーをグループに追加
    Args:
        いろいろ
        user_info(dict): ユーザー情報
    """
    def __init__(self,user_info):
        self.contract_type = user_info['contract_type']
        self.onelogin_role_id = user_info['onelogin_role_id']
        self.datadog_apikey_id = credentials_store.get_secret('datadog_apikey_json')
        self.datadog_appkey_id= credentials_store.get_secret('datadog_appkey_json')
        self.datadog_apikey_id_info = ast.literal_eval(self.datadog_apikey_id)   
        self.datadog_appkey_id_info = ast.literal_eval(self.datadog_appkey_id) 
        self.datadog_key_list = self.__datadog_key_info()
        self.datadog_apikey_list = self.datadog_key_list[0]
        self.datadog_appkey_list = self.datadog_key_list[1]
 

    
    def __datadog_key_info(self):
        """
        ユーザーが入るべきDatadogの環境のkeyを追加する情報を返す
        """
        datadog_apikey_list = []
        datadog_appkey_list = []
        if self.contract_type in ['正社員', 'インターン','業務委託']:
            MICIN_onelogin_role_id = '491562'
            Iriko_onelogin_role_id = '514750'
            MiROHA_onelogin_role_id = '502233'
            pspfollowup_onelogin_role_id = '502451'
            Sandbox_onelogin_role_id = '520655'
            Sui_onelogin_role_id = '503114'
            VideoCall_onelogin_role_id = '1693068'

            if self.onelogin_role_id in ['491562']:
                datadog_apikey_list.append(self.datadog_apikey_id_info[MICIN_onelogin_role_id])
                datadog_appkey_list.append(self.datadog_appkey_id_info[MICIN_onelogin_role_id])
            if self.onelogin_role_id in ['514750']:
                datadog_apikey_list.append(self.datadog_apikey_id_info[Iriko_onelogin_role_id])
                datadog_appkey_list.append(self.datadog_appkey_id_info[Iriko_onelogin_role_id])
            if self.onelogin_role_id in ['502233']:
                datadog_apikey_list.append(self.datadog_apikey_id_info[MiROHA_onelogin_role_id])
                datadog_appkey_list.append(self.datadog_appkey_id_info[MiROHA_onelogin_role_id])
            if self.onelogin_role_id in ['502451']:
                datadog_apikey_list.append(self.datadog_apikey_id_info[pspfollowup_onelogin_role_id])
                datadog_appkey_list.append(self.datadog_appkey_id_info[pspfollowup_onelogin_role_id])
            if self.onelogin_role_id in ['520655']:
                datadog_apikey_list.append(self.datadog_apikey_id_info[Sandbox_onelogin_role_id])
                datadog_appkey_list.append(self.datadog_appkey_id_info[Sandbox_onelogin_role_id])
            if self.onelogin_role_id in ['503114']:
                datadog_apikey_list.append(self.datadog_apikey_id_info[Sui_onelogin_role_id])
                datadog_appkey_list.append(self.datadog_appkey_id_info[Sui_onelogin_role_id])
            if self.onelogin_role_id in ['1693068']:
                datadog_apikey_list.append(self.datadog_apikey_id_info[VideoCall_onelogin_role_id])
                datadog_appkey_list.append(self.datadog_appkey_id_info[VideoCall_onelogin_role_id])

        return datadog_apikey_list,datadog_appkey_list



def create_user(event, context=''):
    """
    ユーザー作成
    Args:
        event(dict): ユーザー情報
        context(obj): オブジェクト
    Returns:
        (dict) APIレスポンス（グループIDリストを追加している）
    """
    user_info = event
    onelogin_role_id = OneloginRole(user_info)
    datadog_api_key = onelogin_role_id.datadog_apikey_list[0]
    datadog_application_key = onelogin_role_id.datadog_appkey_list[0]

    datadog = Datadog(datadog_api_key,datadog_application_key,user_info)
    res = datadog.create_user()

    for roles_id in datadog.roles_id_list:
        datadog.add_user_roles(roles_id) 
   
    if res['ok']:
        res['roles_ids'] = datadog.roles_id_list
    
    #datadogの環境のoneloginボタンの作成 
    onelogin_client_id = credentials_store.get_secret('onelogin_client_id')
    onelogin_client_secret = credentials_store.get_secret('onelogin_client_secret')
    onelogin_user = OneLoginUser(onelogin_client_id, onelogin_client_secret, user_info)
    user_info['user_id'] = onelogin_user.get_user_id(1)['id']
    user_info['role_id'] = user_info['onelogin_role_id']
    datadog.invite_user(user_info)
    res = onelogin_user.add_role()

    return res

def process_result(res):
    """
    レスポンスを整形
    Args:
        res(dict): レスポンス
    Returns:
        (dict) 整形後のレスポンス
    """
    if res['ok']:
        return {
            'ok': res['ok'],
        }
    else:
        return res

if __name__ == '__main__':
# create_user({},'')
 create_user({'firstname':'taro','lastname':'test',"email":"daichi_yamagata@micin.jp","contract_type": "インターン",'onelogin_role_id':'491562'})
