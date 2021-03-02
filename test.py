import requests

print(requests.get("https://api.github.com/orgs/Connection-Software").json())