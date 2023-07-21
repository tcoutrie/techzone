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
def postattributemap():
  uri = "/api/fdm/v6/object/ldapattributemaps"
  ad_url = protocol+url+uri


  name = input('Object name> ')
  group_policy = input('Group-Policy> ')
  base = input('LDAP DN> ')

  headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization":"Bearer {}".format(token)
  }

  payload = {
  "name": name,
  "ldapAttributeMaps": [
    {
      "ldapName": "memberOf",
      "ciscoName": "GROUP_POLICY",
      "valueMappings": [
        {
          "ldapValue": base,
          "ciscoValue": group_policy,
          "type": "ldaptociscovaluemapping"
        }
      ],
      "type": "ldapattributemapping"
    }
  ],
    "type": "ldapattributemap"
  }
  data = json.dumps(payload)

  response = requests.post(ad_url, headers=headers, data=data, verify=False)

  if response.status_code == 200:
    print(response.status_code)
    print("Created LDAP attribute map")
    map = response.json
    return map
  else:
    print(response.status_code)
    pprint(response.content)
    pass



postattributemap()



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

