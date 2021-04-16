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
	data = '{0}'.format(str(base64.b64encode(qbf)))
	payload = {
		'QBF': data
	}
	with open('qbf.json', 'w') as f:
		json.dump(payload, f)

	resp = requests.post(url, json=payload, headers=headers)

	return resp.json()

def send_cbf(cbf):
	url = "http://ec2-3-26-37-172.ap-southeast-2.compute.amazonaws.com:9000/comp4337/cbf/upload"
	headers = CaseInsensitiveDict()
	headers["Content-Type"] = "application/json"
	# data = '{{CBF: {0}}}'.format(base64.b64encode(bytes(cbf, encoding="ascii")))
	data = '{0}'.format(str(base64.b64encode(cbf)))
	payload = {
		'CBF': data
	}
	with open('cbf.json', 'w') as f:
		json.dump(payload, f)
	resp = requests.post(url, json=payload, headers=headers)

	return resp.json()

# main function
if __name__ == "__main__":

	# asd = "10" * 400000
	# resp = send_qbf(asd)
	# print(len(asd))
	# print(resp)

	bloomf1 = BloomFilter(100000)
	word_present = [67488643248729147932]
	for item in word_present:
		bloomf1.add(item)
		
	resp = send_qbf(bloomf1.bit_array)