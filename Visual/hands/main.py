

import time
from pathlib import Path
import cv2
import depthai as dai

# Create pipeline
pipeline = dai.Pipeline()

# Define sources and outputs
camRgb = pipeline.createColorCamera()
videoEnc = pipeline.createVideoEncoder()
xoutJpeg = pipeline.createXLinkOut()
xoutRgb = pipeline.createXLinkOut()

xoutJpeg.setStreamName("mkv")
xoutRgb.setStreamName("rgb")

# Properties
camRgb.setBoardSocket(dai.CameraBoardSocket.RGB)
camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_4_K)
videoEnc.setDefaultProfilePreset(camRgb.getVideoSize(), camRgb.getFps(), dai.VideoEncoderProperties.Profile.MJPEG)

# Linking
camRgb.video.link(xoutRgb.input)
camRgb.video.link(videoEnc.input)
videoEnc.bitstream.link(xoutJpeg.input)

# Connect to device and start pipeline
with dai.Device(pipeline) as device:

    # Output queue will be used to get the rgb frames from the output defined above
    qRgb = device.getOutputQueue(name="rgb", maxSize=30, blocking=False)
    qJpeg = device.getOutputQueue(name="mkv", maxSize=30, blocking=True)

    # Make sure the destination path is present before starting to store the examples
    dirName = "rgb_data"
    Path(dirName).mkdir(parents=True, exist_ok=True)

    while True:
        inRgb = qRgb.tryGet()  # Non-blocking call, will return a new data that has arrived or None otherwise

        if inRgb is not None:
            cv2.imshow("rgb", inRgb.getCvFrame())

        for encFrame in qJpeg.tryGetAll():
            with open(f"{dirName}/{int(time.time() * 1000)}.mkv"
                      f"", "wb") as f:
                f.write(bytearray(encFrame.getData()))

        if cv2.waitKey(1) == ord('q'):
            break








'''
##########################################
# Ler dados enoncms
##########################################


##########################################
# submeter dados enoncms
##########################################

def SubmitData(data):
    url = "https://emoncms.org/input/post?"
    url += "node=emontx"
    url += "&apikey=1af79b8aa2d605ea3e350c3783a88c2d"
    url += "&fulljson=" + json.dumps(data)
    y=requests.get(url)

##########################################
# Change stage
##########################################

def ChangeStage(data, action):
    gestureLUT = {"SwapRight": "socket1", "SwapLeft": "socket2", "LeftArmUp": "socket3"}
    if data[gestureLUT[action]] == 1:
        data[gestureLUT[action]] = 0
    else:
        data[gestureLUT[action]] = 1
    return data

#readData()
data = {"socket1": 0, "socket2": 0, "socket3": 0}
PersonDetected = True
DetectDog = True
PresentGesture = "LeftArmUp"

while True:
    # (a) on/off 4 power plugs
    # HERE "Function to detect gestures" - Activate/Deactivate PowerPlugs - example detect "SwapRight"
    # same movement turn off the PowerPlug
    data = ChangeStage(data, "SwapRight")
    # (b) detect/not detect a person turn on/off light in the present room
    # HERE "Function to detect persons" - if a person detect in the room turn on the lap on the room
    # person leave turn off the light
    #if PersonDetected == True:
     #  data["TurnLampRoomOn"] = False
    # (c) detect person + dog + arm up - open door dog go out; otherwise close door
    # HERE "Function detect dogs" - detect persons & detect a dog & person arm is up - automatically opens door for dog go out
    # if PersonDetected == True and DetectDog == True and PresentGesture == "LeftArmUp":
      #  data["Door4DogGoOut"] = True
    #else:
      #  data["Door4DogGoOut"] = False
    #SubmitData(data)
    print(data) # remove only to see results
    cv2.waitKey(15000) # dammy remove
    import cv2
import requests
import json
'''