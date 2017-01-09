#!/bin/env python

import http.client, urllib.request, urllib.parse, urllib.error, base64

apiKey = '2130ac086c2d4d62b1ac1deb2f173910'
profileId = 'f33d9cf2-3a4c-4c5e-b611-18d3ff9f6af8'

headers = {
    # Request headers
    'Content-Type': 'multipart/form-data',
    'Ocp-Apim-Subscription-Key': apiKey,
}

params = urllib.parse.urlencode({
    # Request parameters
    'shortAudio': 'false',
})

try:
    conn = http.client.HTTPSConnection('api.projectoxford.ai')
    conn.request("POST", "/spid/v1.0/identificationProfiles/{identificationProfileId}/enroll?%s" % params, "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))