import requests
import os
import json

class JsonDb():
	def __init__(self):
		self.baseurl="https://jsonbin.org/me"
		self.auth_token=os.environ['JSON_AUTH_TOKEN']
		self.headers={"content-type":"application/json","authorization":self.auth_token}
		
	def get(self,key):
		url=self.baseurl+"/"+key
		print url
		r=requests.get(url,headers=self.headers)
		if r.status_code==404:
			return None
		return r.text

	def post(self,data):
		url=self.baseurl
		r=requests.post(url,data=data,headers=self.headers)
		return (r.status_code,r.text)

	def patch(self,data):
		url=self.baseurl
		r=requests.patch(url,data=data,headers=self.headers)
		return (r.status_code,r.text)

	def delete(self,rpath):
		url=self.baseurl+"/"+rpath
		r=requests.delete(url)
		return r.status_code
