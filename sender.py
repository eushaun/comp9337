import requests
from requests.structures import CaseInsensitiveDict

url = "http://ec2-3-25-246-159.ap-southeast-2.compute.amazonaws.com:9000/comp4337/cbf/upload"

headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/json"

data = '{"qbf": "asdad"}'


resp = requests.post(url, headers=headers, data=data)

print(resp.status_code)
