# pylint: disable=import-error
from pynput import keyboard
import requests

URL = 'http://192.168.100.129:5000'
FORWARD = '/forward'
BACKWARD = '/backward'
LEFT = '/left'
RIGHT = '/right'
STOP = '/stop'

REQUEST_TIMEOUT = 1.5

def post_method(method:str, power:int):
    """method: like '/LEFT', '/RIGHT' ...
       power:  0 - 10 where 10 is 100%"""
    data = {'power': power}
    try:
        res = requests.post(url=URL+method, json = data, timeout=REQUEST_TIMEOUT)
    except (TimeoutError, requests.ConnectTimeout, requests.ConnectionError) as error:
        print('timeout error', error)
        return error
    return res

keys_linked_post_methods = dict(zip(('a', 's', 'd', 'w'),(LEFT, BACKWARD, RIGHT, FORWARD)))
def status_key_flag():
    """set key flag. return dic[key] if statsu is not given"""
    key_status = {i: False for i in ('a', 's', 'd', 'w')}
    def check(key, status=None):
        if key not in key_status.keys():
            return None
        if status is None:
            return key_status[key]
        key_status[key] = status
        return None
    return check

key_flags = status_key_flag()

def on_press(event):
    """event: event from keyboard linstener"""
    try:
        event_key = event.char
    except AttributeError:
        event_key = event

    for key, method in keys_linked_post_methods.items():
        if event_key == key and not key_flags(key) :
            key_flags(key, True)
            post_method(method, 3)


def on_release(event):
    """event: event from keyboard linstener"""
    try:
        event_key = event.char
    except AttributeError:
        event_key = event
    if key_flags(event_key):
        post_method(STOP, 0)
        key_flags(event_key, False)

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
