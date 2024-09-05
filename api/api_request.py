
import requests as rq
from requests.auth import HTTPBasicAuth

USERNAME = ""
PASSWORD = ""

URL = "https://dahauni.ir/api/users"

response = rq.get(URL, auth=HTTPBasicAuth(username=USERNAME, password=PASSWORD))
print(response.json())
