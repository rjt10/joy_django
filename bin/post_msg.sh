
curl -X POST -H "Content-Type: application/json" -d '{
    "recipient":{
        "id":"1074431152632259"
    }, 
    "message":{
        "text":"hello, world!"
    }
}' "https://graph.facebook.com/v2.6/me/messages?access_token=CAAYhjFBc8g0BAEpHgVFfNjzrNkhgzEej6KShC5TcFKU03L1NMXp1r333AmfaFG7CxzoFQUuCoRX60GwerMgEo7JR21SEoLN2Tp58cLqkZAqdxU0Jp1KqMADzufxmQ4h1N0xqD0SD094gIAiKNdP89lLWae9LYpajMoVt23OU1CGVXjZAEzdF2eby79o1EZD"
