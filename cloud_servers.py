#!/usr/bin/env python

import os, pyrax
import pyrax.exceptions as exc
from itertools import chain

def cloud_connect():
  creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
  try:
    pyrax.set_setting("identity_type", "rackspace")
    pyrax.set_credential_file(creds_file)
  except exc.AuthenticationFailed:
    print "Problem with credential file ~/.rackspace_cloud_credentials"

def list_servers(dc):
  cs = pyrax.connect_to_cloudservers(region=dc)
  for server in cs.servers.list():
    print "Server Name: ", server.name
    print "Server Status: ", server.status
    print "Server ID: ", server.id
    print "Public IP: ", server.accessIPv4
    print "Private IP: ", server.addresses['private'][0]['addr']
  

def list_images():
  cs = pyrax.cloudservers
  for image in cs.images.list():
    print image   

def list_flavors():
  cs = pyrax.cloudservers
  for flavor in cs.flavors.list():
  	print flavor


if __name__ == "__main__":
  cloud_connect()
  list_servers("DFW")