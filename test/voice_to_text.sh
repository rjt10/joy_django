#!/bin/sh

BEARER_TOKEN='ya29.El_DA7kAr6XIuFq3FE1dPhO39a5don39n7Kdcu6Upd64ggxOCqqVjTTO3BFvSt89NBH8Ax3q_ibipbYGmT15983sKEH7e0Ef4nkdU2QQ4GYiP1lg2kBBXXoTNh922Emunw'
BEARER_TOKEN='ya29.El_DA3rKcGRm8NeyAGphB4yFGZCBwo8NtS1McmxxgXD5_jFSNIt1PZ9RWX7FsPkLT-mbwHMu-aRM31dPzULBlfeP_Tr1-GhcWk2vJwZq6OKzNrBpW_aM2jQSPPmpCBp7uw'

curl -k \
	-H "Content-Type: application/json" \
    -H "Authorization: Bearer $BEARER_TOKEN" \
    https://speech.googleapis.com/v1beta1/speech:syncrecognize \
    -d @voice_to_text.json