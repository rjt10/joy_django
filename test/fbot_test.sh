#!/bin/sh

BEARER_TOKEN='ya29.El_AA-RRwWXmbpCLHzn3BD3_p6fpYy2eRLlCAwS0o5C2hlgWgeHK2ugZB6fLuoIdm3FU9jc3-5P2j_37qIVwrofONILOOH3epuxIl103r7Fsqm0TluCkCg2eTRLiBCfPGw'

curl -k \
	-H 'Content-Type: application/json' \
	-H "Authorization: Bearer $BEARER_TOKEN" \
	http://localhost:8000/webhook -d @fbot_req.json