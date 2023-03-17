import requests
import json

class telegrambot():
    
    def __init__(self):
        self.token = ""
        self.url = "https://api.telegram.org/bot{self.token}"

    def get_updates(self,offset=None):
        url = self.url+"/getUpdates?timeout=100"    # In 100 seconds if user input query then process that, use it as the read timeout from the server
        if offset:
            url = url+"&offset={offset+1}"
        url_info = requests.get(url)
        return json.loads(url_info.content)

    def send_message(self,msg,chat_id):
        url = self.url + "/sendMessage?chat_id={chat_id}&text={msg}"
        if msg is not None:
            requests.get(url)

    def grab_token(self):
        return tokens
