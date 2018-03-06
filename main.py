serverUrl = "http://<<PUBLIC IPV4 HERE>>:8093/"

import time
import pychromecast
import sys
from flask import Flask
from flask import request
import gtts
import threading
import random
import json
from mutagen.mp3 import MP3

chromecasts = pychromecast.get_chromecasts()
names = [cc.device.friendly_name for cc in chromecasts]
print(names)

app = Flask(__name__)

@app.route("/audio.mp3")
def hello():
    read = None
    f = open("file.mp3","rb")
    read = f.read()
    f.close()
    return read
@app.route("/")
def hi():
    return "SUP!"


@app.route("/push")
def sayToServer():
    global chromecasts
    urlData = getArgs(request.url)
    device = urlData["device"]
    text = urlData["text"]
    slow = True
    if ("slow" in urlData.keys()):
        if (urlData["text"] == "true"):
            slow = True
        if (urlData["text"] == "false"):
            slow = False


    cast = None
    if (device in names):
        print("Device Found")
    else:
        return "Device Not Found"

    cast = next(cc for cc in chromecasts if cc.device.friendly_name == device)
    oldVol = None
    if ("vol" in urlData.keys()):
        oldVol = getCastVolume(cast)
        newVol = float(round(float(urlData["vol"]),1))
        setCastVolume(cast,newVol)
        saytext(text, cast, sayslow=slow)
        setCastVolume(cast, oldVol)
    else:
        saytext(text,cast,sayslow=slow)

    return "Pushed."

@app.route("/devices")
def getdevs():
    global names
    return str(names)





def saytext(pushtext,device,sayslow=True,dosleep=True):
    print("Saying Text")
    tts = gtts.gTTS(text=pushtext, lang='en', slow=sayslow)
    tts.save("file.mp3")
    times = MP3("file.mp3").info.length
    mc = device.media_controller
    mc.play_media(serverUrl+"audio.mp3", 'audio/mp3',title="Push Notification")
    mc.block_until_active()
    mc.play()
    print(mc.status);
    if (dosleep == True):
        time.sleep(times +5)

def getCastVolume(device):
    pvol = device.status.volume_level*100
    val = round(float(pvol),1)
    print(device.status)
    print(device.status.volume_level)
    print(pvol)
    print(val)
    return val

def setCastVolume(device,perc):
    toDec = round(perc,1)/100
    print(toDec)
    device.set_volume(toDec)

def runServer():
    print("Starting Server")
    app.run(host='0.0.0.0', port=8093)

def getArgs(url):
    urlSplit = url.split("?",1)[1]
    urlData = urlSplit.split("&")
    build = {}
    for data in urlData:
        keySplit = data.split("=",1)
        key = keySplit[0]
        value = keySplit[1]
        build[key] = value
    return build


if __name__ == '__main__':
    #thd = threading.Thread(target=runServer,daemon=True)
    #thd.start()
    runServer()

