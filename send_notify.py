
import requests

TOKEN = '21b1354772f837c04fea55c5b7149b6b7d1f626b'
APP_ID = 'uni.treasure.wasal'

def config_notify(title, content, image):
    # set header
    headers = {
        'Authorization': 'Token ' + TOKEN,
        'Content-Type': 'application/json'
    }

    # data & config
    data = {
        'app_ids': [APP_ID,],
        'data': {
            'title': f'{title}',
            'content': f'{content}',

            'wake_screen': True,
            'action': {
                'action_type': 'A',
                'url': '',
            },
            'image': f'{image}',
        },
    }

    # send request
    requests.post(
        'https://api.push-pole.com/v2/messaging/notifications/',
        json=data,
        headers=headers,
    )
