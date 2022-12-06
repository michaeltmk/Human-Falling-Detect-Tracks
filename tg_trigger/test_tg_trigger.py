from tg_trigger.tg_trigger import TelegramTrigger
import yaml

def test_send_fall_down_alert():
    with open("config.yaml",'r') as f:
        config = yaml.safe_load(f)
        tg_conf = config.get("telegram")
    trigger = TelegramTrigger(tg_conf.get('token'),tg_conf.get('chat_id'))
    result = trigger.send_fall_down_alert()
    assert result
