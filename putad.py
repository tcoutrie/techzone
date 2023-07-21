import requests
import json
import certifi
import urllib3
from pprint import pprint
from getpass import getpass

urllib3.disable_warnings() 

#Data collection
u = input ('Input username: ')
p = getpass(prompt='Input password: ')
url = input('Input Hostname or IP address: ')
protocol = 'https://'

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def auth():

  uri = '/api/fdm/v6/fdm/token'
  token_url = protocol+url+uri

  payload = {
        'grant_type' : 'password',
        'username' : u,
        'password': p
        }

  response = requests.post(token_url, data=payload, verify=False)
  
  #WARNING ONLY USE "verify=False" in a lab setting!

#Error Checking
  if response.status_code == 400:
    raise Exception("Error Received: {}".format(response.content))
  else:
    access_token = response.json()['access_token']
    return access_token

token = auth()
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def put():
  objId = input('object id> ')
  uri = "/api/fdm/v6/object/realms/"
  ad_url = protocol+url+uri+objId

  headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization":"Bearer {}".format(token)
  }
#Place the GET response from the active directory here in "payload" along with the added "ldapAttributeMap", "id" and ""type": "ldapattributemap"" 
  payload = {
  "version": "p6ueo2w2aulkf",
  "name": "Test",
  "directoryConfigurations": [
    {
      "hostname": "172.18.108.34",
      "port": 389,
      "encryptionProtocol": "NONE",
      "encryptionCert": None,
      "interface": { 
        "version": "mjvylmnd52agk",
        "name": "diagnostic",
        "hardwareName": "Management0/0",
        "id": "a46ef70c-06ca-11ee-9be1-bd712e622992",
        "type": "physicalinterface"
      },
      "type": "directoryconfiguration"
    }
  ],
  "enabled": True,
  "realmId": 3,
  "dirUsername": "cisco",
  "dirPassword": "*********",
  "baseDN": "dc=cisco,dc=com",
  "ldapAttributeMap": {
    "id": "2c7b3f25-26fd-11ee-a635-fd06258c4ec8",
    "type": "ldapattributemap"
  },
  "adPrimaryDomain": "cisco.com",
  "id": "5957a304-2662-11ee-a635-a5df7d28e8c4",
  "type": "activedirectoryrealm"
  }

  data = json.dumps(payload)


  response = requests.put(ad_url, headers=headers, data=data, verify=False)

  if response.status_code == 200:
    print("Updated Object")
  else:
    pprint("Error Received: {}".format(response.content))
    pass

put()



#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def revoke():

  uri = '/api/fdm/v6/fdm/token'
  token_url = protocol+url+uri

  headers = {
      "Content-Type": "application/json",
      "Accept": "application/json",
      "Authorization":"Bearer"
  }
  payload = {
        'grant_type' : 'revoke_token',
        "access_token": token,
        "token_to_revoke": token,
        }

  response = requests.post(token_url, data=payload, verify=False)

  if response.status_code == 200:
    print("Access token revoked")
  else:
    print(response.status_code)


revoke()









