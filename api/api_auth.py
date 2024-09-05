
from api.api import user_auth
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    if ((f'{username}',) in user_auth.get("email")) and ((f'{password}',) in user_auth.get("password")):
        return username
