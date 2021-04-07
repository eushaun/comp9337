import requests
from requests.structures import CaseInsensitiveDict
import base64

def send_qbf(qbf):
	url = "http://ec2-3-25-246-159.ap-southeast-2.compute.amazonaws.com:9000/comp4337/cbf/upload"

	headers = CaseInsensitiveDict()
	headers["Content-Type"] = "application/json"
	data = '{{QBF: {0}}}'.format(base64.b64encode(bytes(qbf, encoding="ascii")))
	resp = requests.post(url, headers=headers, data='=TExMTExMjM1MjIzcQ==K')

	return resp

def send_cbf():
	URL = "http://ec2-3-25-246-159.ap-southeast-2.compute.amazonaws.com:9000/comp4337/cbf/upload"

	headers = CaseInsensitiveDict()
	headers["Content-Type"] = "application/json"
	data = '{{CBF: {0}}}'.format(base64.b64encode(bytes(qbf, encoding="ascii")))
	resp = requests.post(url, headers=headers, data='=TExMTExMjM1MjIzcQ==K')

	return resp

# main function
if __name__ == "__main__":

	asd = "10" * 400000
	resp = send_qbf(asd)
	print(len(asd))

	print(resp.text)
