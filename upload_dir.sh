#!/bin/bash

FILES=`ls`
TOKEN="AUTH_TOKEN"
ENDPOINT="https://snet-storage101.ord1.clouddrive.com/v1/{ENDPOINT}/{CONTAINER}"

#for f in $FILES
ls | while read f; 
do
    MIME=$(file --mime ${f} | awk '{print $2}')
    echo "Uploading ${f}"
    curl -X PUT ${ENDPOINT}/${f} -T ${f} -H "Content-Type: ${MIME}" -H "X-Auth-Token: ${TOKEN}"
done