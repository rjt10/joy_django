#!/bin/sh

KEY='2130ac086c2d4d62b1ac1deb2f173910'
PROFILE_ID="f33d9cf2-3a4c-4c5e-b611-18d3ff9f6af8"

#curl -X POST \
#	 "https://api.projectoxford.ai/spid/v1.0/identificationProfiles" \
#	-H "Content-Type: application/json" \
#	-H "Ocp-Apim-Subscription-Key: $KEY" \
#	-d @profile_id.json

#curl -v -X GET \
#	"https://api.projectoxford.ai/spid/v1.0/identificationProfiles" \
#	-H "Ocp-Apim-Subscription-Key: $KEY" \
#	-H 'Content-Length: 0'
#	--data-ascii "{body}"


curl -v -X POST \
	"https://api.projectoxford.ai/spid/v1.0/identificationProfiles/$PROFILE_ID/enroll?shortAudio=true" \
	-H "Content-Type: multipart/form-data" \
	-H "Ocp-Apim-Subscription-Key: $KEY" \
	--data-ascii @speaker_rj.aifc

# {
#  "identificationProfileId": "f33d9cf2-3a4c-4c5e-b611-18d3ff9f6af8"
#}