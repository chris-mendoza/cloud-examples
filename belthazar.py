#!/usr/bin/env python

import time, os, zipfile, os, pyrax, random, struct
import pyrax.exceptions as exc
from Crypto.Cipher import AES

timestamp = time.strftime('%m-%d-%Y_%H:%M')

def compress_dir(path, outpath):
    os.chdir(outpath)
    fname = path.split("/")[2]
    file_name = "%s%s.zip" % (fname, timestamp)
    zip = zipfile.ZipFile(file_name, 'w',
                          compression=zipfile.ZIP_DEFLATED,)

    for root, dirs, files in os.walk(path):
        for file in files:
            zip.write(os.path.join(root, file))

    return (path + "/" + file_name, outpath+"/"+file_name)

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

def encrypt_file(key, in_filename, out_filename=None, chunksize=64*1024):
    if not out_filename:
        out_filename = in_filename + '.enc'
    iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)
    with open(in_filename, 'rb') as infile:
         with open(out_filename, 'wb') as outfile:
             outfile.write(struct.pack('<Q', filesize))
             outfile.write(iv)
             while True:
                 chunk = infile.read(chunksize)
                 if len(chunk) == 0:
                     break
                 elif len(chunk) % 16 != 0:
                     chunk += ' ' * (16 - len(chunk) % 16)
                 outfile.write(encryptor.encrypt(chunk))

def decrypt_file(key, in_filename, out_filename=None, chunksize=24*1024):
    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]
    with open(in_filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)
        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))
            outfile.truncate(origsize)



if __name__ == "__main__":
    print "meh"
