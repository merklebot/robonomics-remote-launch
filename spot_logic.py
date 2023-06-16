import requests
import bosdyn.client
res = requests.get('google.com')
print(res.text)