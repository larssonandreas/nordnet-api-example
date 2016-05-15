from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
import http.client
import urllib
import base64
import time
import json

"""
Read credentials form file since credentials and configuration should allways be keept separate from application logic
and can vary depending on running the code in dev, test or prod envoiroment and for security reasons sensitive
information like API keys should not be checked into source control.
"""
print("Reading credentials from file...")
file = open('config/credentials.json', 'r')
data = file.read()
file.close()
credentials = json.loads(data)

print("Initiating connection params...")
username = credentials['username']
password = credentials['password']
service = 'NEXTAPI'
URL = 'api.test.nordnet.se'
API_VERSION = '2'
connection = http.client.HTTPSConnection(URL)

"""
The following section sets up the authentication params and encrypts them in different stages. The encryption process
does also make use of the provided public key in the assets folder, which is a copy of the files provided from the
Nordnet developer resource forums(https://api.test.nordnet.se/api-docs/), the keys have been downloaded on: 2016-05-13.
"""
print("Preparation and encryption of params...")
timestamp = int(round(time.time() * 1000))
timestamp = str(timestamp)

b64_username = base64.b64encode(username.encode('utf-8')).decode("utf-8")
b64_password = base64.b64encode(password.encode('utf-8')).decode("utf-8")
b64_timestamp = base64.b64encode(timestamp.encode('utf-8')).decode("utf-8")
buf = b64_username + ":" + b64_password + ":" + b64_timestamp

print("b64_username: {b64_username}\n"
      "b64_password: {b64_password}\n"
      "b64_timestamp: {b64_timestamp}\n"
      "Message buffer: {buf}".format(b64_username=b64_username,
                                     b64_password=b64_password,
                                     b64_timestamp=b64_timestamp,
                                     buf=buf)
      )

key_file = open('assets/NEXTAPI_TEST_public.pem', 'r')
rsa = RSA.importKey(key_file.read())
cipher = PKCS1_v1_5.new(rsa)
enc = cipher.encrypt(str.encode(buf))
b4_hash = base64.b64encode(enc).decode("utf-8")

print("Raw cipher encryption: \n {enc}\n"
      "Base64 encoded cipher: \n {b4_hash}".format(enc=enc,
                                                   b4_hash=b4_hash)
      )

"""
The code below initiates a login request passing the encoded login credentials as params and upon succesfully connection
it will receive a session key(and some other data as well) to be used by subseqent calls.
"""
print("Making login request with params...")
headers = {'Accept': 'application/json'}
params = urllib.parse.urlencode({'service': service, 'auth': b4_hash})
connection.request('POST', '/next/' + API_VERSION + '/login', params, headers)
resp = connection.getresponse()
print("Response metadata from call HTTP Status code: {status} Reason: {reason}".format(status=resp.status,
                                                                                       reason=resp.reason)
      )
print("Response data as indented JSON:")
response = resp.read()
json_data = json.loads(response.decode("utf-8"))
print(json.dumps(json_data,
                 sort_keys=True,
                 indent=4)
      )

"""
The code below retrieves account information from the account associated with the provided credentials in order to
verify that the connection was successfully established and the sessionkey is valid.

Send sessionkey:sessionkey as base64 encoded basic auth with all calls after login call in order to execute API calls
over REST
"""
session_key = json_data['session_key'] + ':' + json_data['session_key']
b64_auth = base64.b64encode(bytes(session_key, encoding='utf-8')).decode("utf-8")
headers['Authorization'] = 'Basic ' + b64_auth
print("Making REST request to get Account data")
connection.request('GET', '/next/' + API_VERSION + '/accounts', '', headers)
resp = connection.getresponse()
print("Response metadata from call HTTP Status code: {status} Reason: {reason}".format(status=resp.status,
                                                                                       reason=resp.reason)
      )
print("Response data as indented JSON:")
response = resp.read()
json_data = json.loads(response.decode("utf-8"))
print(json.dumps(json_data,
                 sort_keys=True,
                 indent=4)
      )
