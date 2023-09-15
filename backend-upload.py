#!/usr/bin/python3
import cgi
import os
import time
import cv2
import boto3
import time


from cvzone.HandTrackingModule import HandDetector
upload_dir = "upload/"

print("Content-Type: text/plain")
print()

try:
    form = cgi.FieldStorage()
    image_file = form['image']
    
    if image_file.filename:
        timestamp = int(time.time())
#        filename = f"image_{timestamp}.png"
        filename = "myimage.png"
        
        filepath = os.path.join(upload_dir, filename)
        with open(filepath, 'wb') as f:
            f.write(image_file.file.read())
        print("<p>Live Streaming Started ..</p>")
    else:
        print("No image file received")
except Exception as e:
    print("An error occurred:", str(e))

myec2=boto3.resource('ec2')
def launchos():
    res=myec2.create_instances(
    ImageId="",
    InstanceType="t2.micro",
    MaxCount=1,
    MinCount=1
    )
    print("os launched ...")
detector = HandDetector(maxHands=1,
                        detectionCon=0.8)

img = cv2.imread("upload/myimage.png")

hand = detector.findHands(img , draw=False)
if hand:
        lmlist = hand[0]
        if lmlist:
            fingerup = detector.fingersUp(lmlist)
            print(fingerup)
            if fingerup == [1, 1, 1, 1, 1]:
                print("index finger ..")
                launchos()

            elif fingerup == [0, 1, 1, 0, 0]:
                print("index and middle finger ..")

            else:
                print("i work with index or middle finger ..")

else:
        print("no hand detected")
