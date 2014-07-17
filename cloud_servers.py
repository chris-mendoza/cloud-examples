#!/usr/bin/env python

import os, pyrax, time
import pyrax.exceptions as exc

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
  
def server_info(id, dc):
    cs = pyrax.connect_to_cloudservers(region=dc)
    server = cs.servers.get(id)
    print "Server Name: ", server.name
    print "Server ID: ", server.id
    print "Public IP: ", server.accessIPv4
    print "Private IP :", server.addresses['private'][0]['addr']

def base_images():
    cs = pyrax.cloudservers
    img = cs.list_base_images()
    for i in img:
  	    print i.name
  	    print i.id

def snapshots(dc):
    cs = pyrax.connect_to_cloudservers(region=dc)
    img = cs.list_snapshots()
    for i in img:
  	    print i.name
  	    print i.id

def list_all_images(dc):	
    cs = pyrax.connect_to_cloudservers(region=dc)
    for image in cs.images.list():
        print "Name:",image.name, "\nID:", image.id

def list_flavors():
    cs = pyrax.cloudservers
    for flavor in cs.flavors.list():
        print "Name:", flavor.name, "-- ID:", flavor.id

def hard_reboot(id, dc):
    cs = pyrax.connect_to_cloudservers(region=dc)
    server = cs.servers.get(id)
    server.reboot("hard")
    after_reboot = cs.servers.get(active.id)
    print "Server Status: ", after_reboot.status

def soft_reboot(id, dc):
    cs = pyrax.connect_to_cloudservers(region=dc)
    server = cs.servers.get(id)
    server.reboot("hard")
    after_reboot = cs.servers.get(active.id)
    print "Server Status: ", after_reboot.status

def create_image(name, id, dc):
    cs = pyrax.connect_to_cloudservers(region=dc)
    server = cs.servers.get(id)
    print "Image ID: ", server.create_image(name)

def create_server(name, img_id, flv_id, dc):
    cs = pyrax.connect_to_cloudservers(region=dc)
    new_server = cs.servers.create(name, img_id, flv_id)
    print "-"*30, "\nName:", new_server.name, "\nID:", new_server.id, \
    "\nStatus:", new_server.status, "\nAdmin Password:", new_server.adminPass
    
    new_serverid = new_server.id
    while not (new_server.networks):
    	time.sleep(50)
    	new_server = cs.servers.get(new_serverid)
    	print "IPv6:", new_server.networks["public"][1], \
        "\nIPv4:", new_server.networks["public"][0], \
        "\nPrivate IP", new_server.networks["private"][0]

def delete_server(id, dc):
	cs = pyrax.connect_to_cloudservers(region=dc)
	server = cs.servers.get(id)
	print "Deleting Server:" server.delete()

if __name__ == "__main__":
    dc = "DFW"
    name = "test12345"
#  srv_id = ""
    img_id = ""
    flv_id = "performance1-1"

    cloud_connect()
#    create_server(name, img_id, flv_id, dc)
