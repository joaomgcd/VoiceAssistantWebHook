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
#import os
#import psycopg2
#import urlparse
#
#urlparse.uses_netloc.append("postgres")
#databaseUrl = os.getenv("DATABASE_URL")
#print(databaseUrl)
#url = urlparse.urlparse(databaseUrl)
#
#conn = psycopg2.connect(
#    database=url.path[1:],
#    user=url.username,
#    password=url.password,
#    host=url.hostname,
#    port=url.port
#)
#cur = conn.cursor()
#cur.execute("select exists(select * from information_schema.tables where table_name=%s)", ('auth',))
#exists = cur.fetchone()[0]
#if not exists:
#	cur.execute("CREATE TABLE auth (id serial PRIMARY KEY, apiName varchar, data varchar);")
#cur.execute("INSERT INTO auth (apiName,data) VALUES (%s, %s);",("test",json.dumps({"ola":"adeus"}, indent=4),))
#cur.execute("SELECT * FROM auth WHERE apiName = %s;",('test',))
#row = cur.fetchone()
#print(cur.fetchone())
#if row is not None:
#	id, apiName, data = row
#	cur.execute("UPDATE auth  SET data=(%s) WHERE id = (%s)",(json.dumps({"whaaaa":"hoooo"}, indent=4),id ,))
#	print(str(id))
#	print(apiName)
#conn.commit()
#cur.close()
#conn.close()

# Flask app should start in global layout
app = Flask(__name__, static_url_path='/static')

@app.errorhandler(Exception)
def handle_bad_request(e):
	import traceback
	print str(traceback.format_exc())
	print str(e)
	return make_response(json.dumps({"error":str(e),"trace":str(traceback.format_exc())}, indent=4))

@app.route('/webhook', methods=['POST'])
def webhook():
	req = request.get_json(silent=True, force=True)

	if req is None:
		print "No request received"
		return
	print("Request:")
	print(json.dumps(req, indent=4))
	
	res = None
	result = req.get("result")
	if result is None:
		print "No result received"
		return
	parameters = result.get("parameters")
	for assistanHandlerClass in handlerutils.assistanHandlerClasses:
		#print assistanHandlerClass
		assistantHandler = assistanHandlerClass()
		if assistantHandler.shouldHandle(req, parameters):
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
	print(auth)
	apiName = auth.get("apiName")
	urls = handlerutils.getAuthAndTokenUrls(apiName)
	if urls is not None:
		authUrl, tokenUrl, scopes = urls
		auth["authUrl"] = authUrl
		auth["tokenUrl"] = tokenUrl
		auth["scopes"] = " ".join([scope for scope in scopes])
	authutils.writeAuthToFile(auth)
	return make_response(json.dumps(auth, indent=4))

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

@app.route('/apinames', methods=['GET'])
def getAuthApiNames():
	return make_response(json.dumps({"apiNames":handlerutils.getApiNames()}))

@app.route('/api', methods=['GET'])
def getApiDetails():
	apiName = request.args.get('apiName')
	result = {}
	urls = handlerutils.getAuthAndTokenUrls(apiName)
	if urls is not None:
		authUrl, tokenUrl, scopes = urls
		result["authUrl"] = authUrl
		result["tokenUrl"] = tokenUrl
		result["scopes"] = scopes
	return make_response(json.dumps(result))

if __name__ == '__main__':
	port = int(os.getenv('PORT', 5000))

	print "Starting app on port %d" % port
	app.run(debug=False, port=port, host='0.0.0.0',threaded=True)
