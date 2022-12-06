import requests
import threading
import time

class TelegramTrigger(object):
    def __init__(self, token, chat_id, cooldown=0):
        self.token = token
        self.chat_id = chat_id
        self.cooldown = cooldown
        self.last_event_time = 0
        self.url = f"https://api.telegram.org/bot{self.token}/"

    def send_msg(self, msg):
        self.set_last_event_time(time.time())
        url = self.url + "sendMessage?chat_id={}&text={}".format(self.chat_id, msg)
        return requests.get(url,timeout=10).status_code

    def send_photo(self, photo):
        self.set_last_event_time(time.time())
        url = self.url + "sendPhoto?chat_id={}".format(self.chat_id)
        files = {'photo': open(photo, 'rb')}
        return requests.post(url, files=files,timeout=10).status_code
    
    def send_fall_down_alert(self):
        self.set_last_event_time(time.time())
        msg_status = self.send_msg("Fall Down Alert!")
        photo_status = self.send_photo("tg_trigger/fall_down.jpg")
        return msg_status == 200 and photo_status == 200
    
    def get_last_event_time(self):
        return self.last_event_time

    def set_last_event_time(self, last_event_time):
        self.last_event_time = last_event_time

    def alert_trigger_gateway(self):
        last_event_time = self.get_last_event_time()
        if time.time() - last_event_time < self.cooldown:
            print(f'Alert is on cooldown, last event time: {last_event_time}, time difference: {time.time() - last_event_time}')
            return None
        else:
            thread = SendingAlertThread(time.time(), str(time.time()), self)
            thread.start()
            return True

class SendingAlertThread (threading.Thread):
    def __init__(self, threadID, name, tg_obj):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.TelegramTrigger = tg_obj

    def run(self):
        return self.TelegramTrigger.send_fall_down_alert()
