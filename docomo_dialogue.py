#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
from datetime import datetime

class DocomoZatsudan:
    REGISTER_KEY = '【取得したAPI】'

    def __init__(self, sex="", t=""):
        # オプション指定（口調）
        self.set_option(sex, t)

        # ユーザ登録
        self.register_user()

    def register_user(self):
        # エンドポイントの設定
        r_url = 'https://api.apigw.smt.docomo.ne.jp/naturalChatting/v1/registration?APIKEY=REGISTER_KEY'
        d_url = 'https://api.apigw.smt.docomo.ne.jp/naturalChatting/v1/dialogue?APIKEY=REGISTER_KEY'
        self.r_url = r_url.replace('REGISTER_KEY', DocomoZatsudan.REGISTER_KEY)
        self.d_url = d_url.replace('REGISTER_KEY', DocomoZatsudan.REGISTER_KEY)

        # ユーザ登録のパラメータを代入
        payload = {'botId':'Chatting', 'appKind':'Chat'} #appKindは任意の文字列
        headers = {'Content-type' : 'application/json;charset=UTF-8'}

        # 送信
        r = requests.post(self.r_url, data=json.dumps(payload), headers=headers)
        data = r.json()
        self.appId = data['appId']  # appIdを取得

    def chat(self, user_input):
        # 日付を取得
        # ※サンプルなので現在の時刻を指定している。
        now_datetime = datetime.now().strftime("%Y-$m-$d %H:%M:%S")

        # 自然対話のパラメータを代入
        payload = {'language':'ja-JP', 'botId':'Chatting', 'appId':self.appId,
            'voiceText':user_input, 'appRecvTime':now_datetime, 'appSendTime':now_datetime,
            'clientData':self.option}
        headers = {'Content-type': 'application/json'}

        # 送信
        r = requests.post(self.d_url, data=json.dumps(payload), headers=headers)
        data = r.json()

        # jsonの解析
        response = data['systemText']['expression']

        # 表示
        print("response: %s" %(response))

    def set_option(self, sex="", t=""):
        self.option = {'option': {'sex':sex, 't':t}}

if __name__ == '__main__':
    docomo_zatsudan = DocomoZatsudan()
#   docomo_zatsudan = DocomoZatsudan(sex="女", t="kansai")

    print("【Enterでプログラム終了】")

    while True:
        # 会話の入力
        user_input = input('>> ')
        if user_input is not '':
            docomo_zatsudan.chat(user_input)
        else:
            exit()
