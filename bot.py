import requests
import datetime
import re
import praw
import random


class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def send_photo(self, chat_id, photo):
        params = {'chat_id': chat_id, 'photo': photo}
        method = 'sendPhoto'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = get_result[len(get_result)]

        return last_update


chat_bot = BotHandler("787581576:AAGyXE5he-9Kbl-OLqlyaw_pDJ8Gu1OvCB4")
now = datetime.datetime.now()
mem = re.compile(r'/m')

def main():
    new_offset = None
    reddit = praw.Reddit(client_id='OtAiIcbZFDiqlg',
                         client_secret='p8X4iCNoG6yziwHdXxGfkTtMWSs',
                         user_agent='testmemesbot')

    while True:
        chat_bot.get_updates(new_offset)

        last_update = chat_bot.get_last_update()

        last_update_id = last_update['update_id']
        last_chat_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']
        last_chat_name = last_update['message']['chat']['first_name']
        if mem.match(last_chat_text):
            last_chat_text = mem.sub('', last_chat_text)
            if(last_chat_text == ''):
                subreddit = 'dankmemes'
            else:
                subreddit = last_chat_text.strip()
            subs = [k for k in reddit.subreddit(subreddit).top()]
            nums = [i for i in range(len(subs))]
            while True:
                i = random.choice(nums)
                try:
                    subs[i].preview
                    break
                except Exception:
                    nums.remove(i)
            s = subs[i]
            chat_bot.send_message(last_chat_id, s.preview['images'][0]['source']['url'])
        new_offset = last_update_id + 1


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
