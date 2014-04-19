#!/usr/bin/env python

'''
Create any amount of servers, with whichever distro and flavor. Injects files as well.
'''

import pyrax
import pyrax.exceptions as exc
import time
import os
import sys
from M2Crypto import RSA
import base64


#Tell the program where to find our login credentials.
creds_file= os.path.expanduser("~/.rackspace_cloud_credentials")

#Use our own authentication script, because it looks ugly otherwise
try:
        pyrax.set_setting("identity_type", "rackspace")
        pyrax.set_credential_file(creds_file)
except exc.AuthenticationFailed:
        print "Problem with credential file ~./rackspace_cloud_credentials"
print "Authenticated =", pyrax.identity.authenticated
print

#Grab each library and put it into a variable for easier reference.
cs = pyrax.cloudservers
dns = pyrax.cloud_dns
cf = pyrax.cloudfiles

#Create a function to generate an RSA key pair if needed


#Take some input from the user, and store it in variables.
serv_pre = raw_input("Server Prefix:\n")
ssh_usr = raw_input("Which user's key are we going to export?(Press enter to use your current users key)")

usr_home = "~"+ssh_usr


srv_host = os.uname()[1]

if ssh_usr == "":
        ssh_usr = os.getlogin()

pub_path = os.path.expanduser("~/.ssh")+"/id_rsa.pub"
priv_path = os.path.expanduser("~/.ssh")+"/id_rsa"

if os.path.isfile(pub_path) is False:
                print "The keys to the user: "+ssh_usr+" does not exist"
                print "Creating a key pair now..."
                rsa_key = RSA.gen_key(2048, 65537)
                pub_key = 'ssh-rsa %s %s@%s' % (base64.b64encode('\0\0\0\7ssh-rsa%s%s ' % (rsa_key.pub()[0], rsa_key.pub()[1])), ssh_usr, srv_host)


                print pub_key

                f = open(pub_path, "a")
                f.write(pub_key)
                f.close()

                rsa_key.save_key(priv_path, cipher=None)


print "Saved SSH Key To local System: \n", pub_path

ssh_key = open(pub_path).read()

random_txt = "meh"

#Specify where the ssh key is going to be uploaded on the created server,
#and give it the data to upload
files = {"/root/.ssh/authorized_keys": ssh_key,"/root/randomexecute.sh":random_txt}

#Interactively specify which image we're going to use
i = 1
while i:
        img_in = raw_input("Type in Image Name:\n")

        search_image = [img for img in cs.images.list()
         if img_in in img.name]

        print search_image


        if "use:" in img_in:
             img_out = img_in.strip("use:")
             saved_img = [img for img in cs.images.list()
                             if img_out in img.name][0]
             print "Using image: ", saved_img
             i = 0


#Interactively specify which flavor to use

i = 1
while i:
        flv_in = raw_input("Choose flavor by Name(I.E.: 512):\n")

        search_flavor = [flv for flv in cs.flavors.list()]
        print search_flavor

        if "use:" in flv_in:
                flv_out = flv_in.strip("use:")
                saved_flv = [flv for flv in cs.flavors.list()
                           if flv_out in str(flv.ram)][0]

                print "Using flavor: ", saved_flv
                i = 0

#Create Servers
print "How many servers would you like to create?"
servernum = int(raw_input())

srv_names = []

for i in xrange(1, servernum+1, 1):

        #append the prefix to a number so all the names aren't the same
        name = serv_pre + str(i)

        #add the name to the list ever iteration.
        srv_names.extend([name])

        #grab the last server on the list, always.
        server_name = (max(srv_names))

        #Create the server, using the user specified data
        new_server = cs.servers.create(server_name, saved_img, saved_flv, files=files)

        #print out server information.
        print "-"*30, "\nName:", new_server.name, "\nID:", new_server.id,\
        "\nStatus:", new_server.status, "\nAdmin Password:", new_server.adminPass

        #used in the while loop to refresh the variable every iteration.
        new_serverid = new_server.id

        #Wait for networking to populate before moving on.
        while not (new_server.networks):
                #wait 30 seconds before moving on
                time.sleep(60)
        #refreshes the new_server value to be tested on next iteration
                new_server = cs.servers.get(new_serverid)
                #Print out networking information
                ipv4_ip = new_server.networks["public"][1]
                ipv6_ip = new_server.networks["public"][0]
                priv_ip = new_server.networks["private"][0]


                print "IPv4:", ipv4_ip, \
                "\nIPv6:", ipv6_ip, \
                "\nPrivate IP", priv_ip

