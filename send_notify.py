
'''
API CONNECTION TO NOTIFICATIONS.
'''

from pusher_push_notifications import PushNotifications

INSTANCE_ID = ''
SECRET_KEY = ''

def config_notify(title, content, icon, link):
    beams_client = PushNotifications(
        instance_id=INSTANCE_ID,
        secret_key=SECRET_KEY,
    )
    
    response = beams_client.publish_to_interests(
      interests=['daha'],
      publish_body={
        'web': {
          'notification': {
            'title': f'{title}',
            'body': f'{content}',
            'icon': f'{icon}',
            'deep_link': f'{link}',
          },
        },
      },
    )
    
    print(response['publishId'])
