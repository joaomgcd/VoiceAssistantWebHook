
import urllib
import requests
import json
import time
import os
import psycopg2
import urlparse
from utils import current_milli_time
urlparse.uses_netloc.append("postgres")
databaseUrl = os.getenv("DATABASE_URL")
print(databaseUrl)
url = urlparse.urlparse(databaseUrl)

conn = psycopg2.connect(
	database=url.path[1:],
	user=url.username,
	password=url.password,
	host=url.hostname,
	port=url.port
)
cur = conn.cursor()
cur.execute("select exists(select * from information_schema.tables where table_name=%s)", ('auth',))
exists = cur.fetchone()[0]
if not exists:
	cur.execute("CREATE TABLE auth (id serial PRIMARY KEY, apiName varchar, data varchar);")
conn.commit()
cur.close()


def getAuthFromFile(apiName):
	cur = conn.cursor()
	cur.execute("SELECT * FROM auth WHERE apiName = %s;",(apiName,))
	existing = cur.fetchone()
	cur.close()
	if existing is None:
		return None
	id, apiName, jsonString = existing
	return json.loads(jsonString)

def writeAuthToFile(auth):    
	apiName = auth.get("apiName")
	cur = conn.cursor()
	cur.execute("SELECT * FROM auth WHERE apiName = %s;",(apiName,))
	existing = cur.fetchone()

	if existing is None:
		cur.execute("INSERT INTO auth (apiName,data) VALUES (%s, %s);",(apiName,json.dumps(auth, indent=4),))   
	else:
		id, apiName, data = existing		
		cur.execute("UPDATE auth  SET data=(%s) WHERE id = (%s)",(json.dumps(auth, indent=4),id ,))

	conn.commit()
	cur.close()

def base64EncodeUserPass(user,password):
	import base64
	encoded = base64.b64encode(user+":"+password)
	print "password: " + encoded
	return encoded

def setAuthAccessToken(auth, response):
	auth["expiresOn"] = current_milli_time() + ((response.get("expires_in") - 300) * 1000)
	auth["accessToken"] = response.get("access_token")
	writeAuthToFile(auth)

def getAccessToken(apiName):    
	auth = getAuthFromFile(apiName)
	if auth is None:
		return None
	print(auth)
	if current_milli_time() > auth.get("expiresOn"):
		clientId = auth.get("clientId")
		clientSecret = auth.get("clientSecret")
		headers = getRefreshTokenAuthHeader(clientId, clientSecret)
		data = {"grant_type":"refresh_token","refresh_token": auth.get("refreshToken")}
		response = requests.post(auth.get("tokenUrl"), data = data, headers = headers).json()
		setAuthAccessToken(auth,response)   
	return auth.get("accessToken")

def getRefreshTokenAuthHeader(clientId, clientSecret):
	return {"Authorization": "Basic " + base64EncodeUserPass(clientId, clientSecret)}

def getRefreshToken(apiName, code): 
	auth = getAuthFromFile(apiName)
	clientId = auth.get("clientId")
	clientSecret = auth.get("clientSecret")
	headers = {"Authorization": "Basic " + base64EncodeUserPass(clientId, clientSecret)}
	data = {"grant_type":"authorization_code","code": code, "redirect_uri": auth.get("redirectUrl"), "client_id": clientId, "client_secret": clientSecret}
	print data
	response = requests.post(auth.get("tokenUrl"), data = data, headers = headers).json()
	print "REFRESH RESPONSE"
	print response
	auth["refreshToken"] = response.get("refresh_token")
	setAuthAccessToken(auth,response)
	return response