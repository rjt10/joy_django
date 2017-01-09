#!/bin/sh

BEARER_TOKEN='ya29.El_DA7kAr6XIuFq3FE1dPhO39a5don39n7Kdcu6Upd64ggxOCqqVjTTO3BFvSt89NBH8Ax3q_ibipbYGmT15983sKEH7e0Ef4nkdU2QQ4GYiP1lg2kBBXXoTNh922Emunw'

curl -k \
	-H "Content-Type: application/json" \
    -H "Authorization: Bearer $BEARER_TOKEN" \
    https://language.googleapis.com/v1/documents:analyzeEntities \
    -d @nl_req.json