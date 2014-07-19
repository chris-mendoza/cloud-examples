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

def list_lb():
    clb = pyrax.cloud_loadbalancers
    print clb.list()

def update_timeout(clb_id, tval):
    clb = pyrax.cloud_loadbalancers
    clb_obj = clb.get(clb_id)
    clb_obj.update(timeout=tval)

if __name__ == "__main__":
    cloud_connect()
    list_lb()