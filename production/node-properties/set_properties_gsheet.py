'''
Quick script to generate the production YAML file from a google sheet and
update the properties in LDAP.
'''

import logging
import urllib2
import csv
import getpass
import yaml
from d1_admin_tools import d1_node_properties as d1np

def pushProperties(data):
  print('''
Make sure you have an LDAP connection on port 3890 by doing something like:

  ssh -L3890:localhost:389 cn-dev-ucsb-1.test.dataone.org
  ''')
  passwd = getpass.getpass("What's the LDAP password: ")
  con = d1np.getLDAPConnection(password=passwd)
  d1np.setNodesProperties(con, data)
  print( yaml.dump(d1np.listAllNodeProperties(con), default_flow_style=False, explicit_start=True) )
  

def mergeContent(new_data):
  original = {}
  with file("production_mn_properties.yaml","rb") as inf:
    original = yaml.load(inf)
  for id in original.keys():
    try:
      new_entry = new_data[id]
      for k in d1np.ALLOWED_PROPERTIES:
        try:
          original[id][k] = new_entry[k]
        except KeyError:
          pass
    except KeyError:
      pass
  return original


def loadFromGoogleSheet(sheetid):
  url = "https://docs.google.com/spreadsheets/d/"+sheetid+"/export?format=csv"
  doc = urllib2.urlopen(url)
  sheet = csv.DictReader(doc, delimiter=",")
  data = {}
  for row in sheet:
    node_id = row['NodeIdentifier']
    entry = {}
    for k in d1np.ALLOWED_PROPERTIES:
      try:
        v = row[k]
        if v == '':
          v = None
        entry[k] = v
      except KeyError:
        pass
    data[node_id] = entry
  return data


if __name__ == "__main__":
  logging.basicConfig(level=logging.DEBUG)
  data = loadFromGoogleSheet("1eDy5IhUUmzu3CT5-jdZlGF97sFS4FprMU3eF8aJxkqU")
  data = mergeContent(data)
  print(yaml.dump(data,  default_flow_style=False, explicit_start=True) )  
  #pushProperties(data)