#!/usr/bin/env python
import http.client, urllib.parse, json

apiKey = "ee1219c80aa54085998acffb69ac0525"

params = ""
headers = {"Ocp-Apim-Subscription-Key": apiKey}

#AccessTokenUri = "https://api.cognitive.microsoft.com/sts/v1.0/issueToken";
AccessTokenHost = "api.cognitive.microsoft.com"
path = "/sts/v1.0/issueToken"

# Connect to server to get the Access Token
print ("Connect to server to get the Access Token")
conn = http.client.HTTPSConnection(AccessTokenHost)
conn.request("POST", path, params, headers)
response = conn.getresponse()
print(response.status, response.reason)

data = response.read()
conn.close()

accesstoken = data.decode("UTF-8")
print ("Access Token: " + accesstoken)

body = "<speak version='1.0' xml:lang='en-us'><voice xml:lang='en-us' xml:gender='Female' name='Microsoft Server Speech Text to Speech Voice (en-US, ZiraRUS)'>This is a demo to call microsoft text to speach service in python.</voice></speak>"

headers = {"Content-type": "application/ssml+xml",
			"X-Microsoft-OutputFormat": "riff-16khz-16bit-mono-pcm",
			"Authorization": "Bearer " + accesstoken,
			"X-Search-AppId": "07D3234E49CE426DAA29772419F436CA",
			"X-Search-ClientID": "1ECFAE91408841A480F00935DC390960",
			"User-Agent": "TTSForPython"}

#Connect to server to synthesize the wave
print ("\nConnect to server to synthesize the wave")
conn = http.client.HTTPSConnection("speech.platform.bing.com")
conn.request("POST", "/synthesize", body, headers)
response = conn.getresponse()
print(response.status, response.reason)

data = response.read()
conn.close()
print("The synthesized wave length: %d" %(len(data)))

target = open("speech.dat", 'wb')
target.write(data)
target.close()

#
#import pyaudio
#import wave

#define stream chunk
#chunk = 1024

#open a wav format music
#f = wave.open(r"/usr/share/sounds/alsa/Rear_Center.wav","rb")  
#instantiate PyAudio  
#p = pyaudio.PyAudio()  
#open stream  
#stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                channels = f.getnchannels(),  
                rate = f.getframerate(),  
                output = True)  
#read data  
#data = f.readframes(chunk)  

#play stream  
#while data:  
#    stream.write(data)  
#    data = f.readframes(chunk)  

#stop stream  
#stream.stop_stream()  
#stream.close()  

#close PyAudio  
#p.terminate()