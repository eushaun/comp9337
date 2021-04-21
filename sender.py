import requests
from requests.structures import CaseInsensitiveDict
import base64
import json
from bloom import *

def send_qbf(qbf):
	url = "http://ec2-3-26-37-172.ap-southeast-2.compute.amazonaws.com:9000/comp4337/qbf/query"
	headers = CaseInsensitiveDict()
	headers["Content-Type"] = "application/json"
	# data = '{{QBF: {0}}}'.format(base64.b64encode(bytes(qbf, encoding="ascii")))
	data = '{0}'.format(base64.b64encode(qbf).decode())
	payload = {
		'QBF': data
	}

	# dump qbf json file
	with open('qbf.json', 'w') as f:
		json.dump(payload, f)

	resp = requests.post(url, json=payload, headers=headers)

	return resp.json()

def send_cbf(cbf):
	url = "http://ec2-3-26-37-172.ap-southeast-2.compute.amazonaws.com:9000/comp4337/cbf/upload"
	headers = CaseInsensitiveDict()
	headers["Content-Type"] = "application/json"
	# data = '{{CBF: {0}}}'.format(base64.b64encode(bytes(cbf, encoding="ascii")))
	data = '{0}'.format(base64.b64encode(cbf).decode())
	payload = {
		'CBF': data
	}

	# dump cbf json file
	with open('cbf.json', 'w') as f:
		json.dump(payload, f)

	resp = requests.post(url, json=payload, headers=headers)

	return resp.json()

# main function
if __name__ == "__main__":

	bloomf1 = BloomFilter(800000)
	word_present = [67488643248729147932]
	for item in word_present:
		bloomf1.add(item)
		
	resp = send_cbf(bloomf1.bit_array)
	print(resp)