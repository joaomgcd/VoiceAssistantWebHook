#!/usr/bin/env python

import urllib
import requests
import json
import os
import authutils
import handlerutils

from flask import Flask, url_for
from flask import request
from flask import make_response
from assistanthandlerbase import AssistantHandler
from os import listdir




# Flask app should start in global layout
app = Flask(__name__, static_url_path='/static')

@app.errorhandler(Exception)
def handle_bad_request(e):
    return 'Error: ' + str(e)

@app.route('/webhook', methods=['POST'])
def webhook():
	req = request.get_json(silent=True, force=True)

	print("Request:")
	print(json.dumps(req, indent=4))

	res = None
	for assistanHandlerClass in handlerutils.assistanHandlerClasses:
		#print assistanHandlerClass
		assistantHandler = assistanHandlerClass()
		if assistantHandler.shouldHandle(req):
			result = req.get("result")
			parameters = result.get("parameters")	  
			res = assistantHandler.handle(parameters)

			break
			# print(res)
	if res is None:
		res = {}
	res = json.dumps(res, indent=4)
	r = make_response(res)
	r.headers['Content-Type'] = 'application/json'
	return r

@app.route('/auth', methods=['POST'])
def storeauth():
	auth = request.get_json(silent=True, force=True)
	authutils.writeAuthToFile(auth)   
	return make_response(json.dumps({"status":"ok"}, indent=4))

@app.route('/auth', methods=['GET'])
def getauth():
	apiName = request.args.get('apiName')
	auth = authutils.getAuthFromFile(apiName)
	return make_response(json.dumps(auth, indent=4))




@app.route('/authtest', methods=['GET'])
def getAuthTest():
	apiName = request.args.get('apiName')
	accessToken = authutils.getAccessToken(apiName)
	return make_response(accessToken)

@app.route('/authrefresh', methods=['POST'])
def setAuthRefreshToken():
	req = request.get_json(silent=True, force=True)
	code = req.get("code")
	apiName = req.get("apiName")
	response = authutils.getRefreshToken(apiName,code)
	responseJson = json.dumps(response, indent=4)
	print responseJson
	return make_response(responseJson)

if __name__ == '__main__':
	port = int(os.getenv('PORT', 5000))

	print "Starting app on port %d" % port
	app.run(debug=False, port=port, host='0.0.0.0',threaded=True)
