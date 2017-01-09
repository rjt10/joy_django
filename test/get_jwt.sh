#!/bin/sh

#curl -H "Content-Type: application/json" -X POST -d '{"username":"xyz","password":"xyz"}' http://localhost:3000/api/login
#curl -k \
#	-H "Content-Type: application/json" \
#    -H "Authorization: Bearer $BEARER_TOKEN" \
#    https://speech.googleapis.com/v1beta1/speech:syncrecognize \
#    -d @voice_to_text.json

curl -k \
	-X POST \
	-H 'Content-Length: 0' \
	-H 'Ocp-Apim-Subscription-Key: ee1219c80aa54085998acffb69ac0525' \
    https://api.cognitive.microsoft.com/sts/v1.0/issueToken
