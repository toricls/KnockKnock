import io
import picamera
import datetime
import requests
import cv2
import numpy
import sys

# get the username as input
username = sys.argv[1]

# Create a memory stream so photos doesn't need to be saved in a file
stream = io.BytesIO()

endpoint = "https://yiwmrr53ce.execute-api.us-east-1.amazonaws.com/stage/requestUploadURL"

# Get the picture (low resolution, so it should be quite fast)
with picamera.PiCamera() as camera:
    camera.resolution = (320, 240)

    while True:
        stream = io.BytesIO()
        camera.capture(stream, format='jpeg')

        # Convert the picture into a numpy array
        buff = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)

        # Now creates an OpenCV image
        image = cv2.imdecode(buff, 1)

        # Get the cascade file (with the generic faces)
        face_cascade = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml')

        # Convert to grayscale
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

        # Look for faces in the image using the loaded cascade file
        faces = face_cascade.detectMultiScale(gray, 1.1, 5)

        print "Found "+str(len(faces))+" face(s)"
        cv2.imwrite('./results/train.jpg', image)

        if len(faces) > 0:
            # Get a S3 upload url
            data = {
                "name": "training-data/%s/%s.jpg" % (username, datetime.datetime.now().isoformat().replace(':','')),
                "type": "image/jpeg"
            }
            resp = requests.post(endpoint, json=data)
            print(resp.json()['uploadURL'])

            resp = requests.put(resp.json()['uploadURL'], data=open('./results/train.jpg', 'rb').read(), headers={'Content-type': 'image/jpeg'})
            print resp
