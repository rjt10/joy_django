#!/bin/sh

JWT_TOKEN='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzY29wZSI6Imh0dHBzOi8vc3BlZWNoLnBsYXRmb3JtLmJpbmcuY29tIiwic3Vic2NyaXB0aW9uLWlkIjoiZjNmMGQ0OTdmN2E5NDA2NmFjMDkxMTk0NzZjZDlmZjgiLCJwcm9kdWN0LWlkIjoiQmluZy5TcGVlY2guUHJldmlldyIsImNvZ25pdGl2ZS1zZXJ2aWNlcy1lbmRwb2ludCI6Imh0dHBzOi8vYXBpLmNvZ25pdGl2ZS5taWNyb3NvZnQuY29tL2ludGVybmFsL3YxLjAvIiwiYXp1cmUtcmVzb3VyY2UtaWQiOiIiLCJpc3MiOiJ1cm46bXMuY29nbml0aXZlc2VydmljZXMiLCJhdWQiOiJ1cm46bXMuc3BlZWNoIiwiZXhwIjoxNDgzMDQ2OTU3fQ.Qo59lu_IxoYURt8Q3p7XcesXv3_QzdMEkAK8CJuH4jY'

curl -k \
	-X POST \
    -H "Authorization: Bearer $JWT_TOKEN" \
    -H 'Content-Type: audio/wav; samplerate=8000' \
    -H 'X-Microsoft-OutputFormat: riff-8khz-8bit-mono-mulaw' \
    https://speech.platform.bing.com/synthesize \
    -d@text_to_speech.xml


