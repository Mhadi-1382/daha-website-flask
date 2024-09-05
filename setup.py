
'''
SETUP DAHA PACKAGES
'''

from time import sleep
import os

alert = '''
 Setup Daha Packages...

'''
for i in alert:
    print(f"{i}", end="", flush=True)
    sleep(0.05)

os.system('pip install -r requirements.txt')
