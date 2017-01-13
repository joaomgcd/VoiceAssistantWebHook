
import urllib
import requests
import json
import time

current_milli_time = lambda: int(round(time.time() * 1000))

def getAuthFromFile(apiName):
    f = open('./auth/' + apiName + ".js", 'r')
    jsonString = f.read() 
    f.close()
    return json.loads(jsonString)

def writeAuthToFile(auth):
    f = open('./auth/' + auth.get("apiName") + ".js", 'w+')
    f.write(json.dumps(auth, indent=4))  # python will convert \n to os.linesep
    f.close()

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