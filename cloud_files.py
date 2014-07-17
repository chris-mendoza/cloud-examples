#!/usr/bin/env python

import time, os, zipfile, pyrax, random, struct
import pyrax.exceptions as exc

def cloud_connect():
    creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
    try:
        pyrax.set_setting("identity_type", "rackspace")
        pyrax.set_credential_file(creds_file)
    except exc.AuthenticationFailed:
        print "Problem with credential file ~/.rackspace_cloud_credentials"

def upload_file(path, cont, dc):
    datacenter = dc
    cf = pyrax.connect_to_cloudfiles(datacenter)
    chksum = pyrax.utils.get_checksum(path)
    obj = cf.upload_file(cont, path, etag=chksum)

def dlcont(c, dc):
    datacenter = dc
    cf = pyrax.connect_to_cloudfiles(datacenter)
    cont = cf.get_container(c)
    objs = cont.get_objects()
    for i in objs:
        print "Downloading", i
        f_gen = cont.fetch_object(i, chunk_size=1024)
        with open(i.name, "w") as dl_file:
             dl_file.write("".join(f_gen))