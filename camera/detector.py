import io
import picamera
import datetime
import requests
import cv2
import numpy

#Create a memory stream so photos doesn't need to be saved in a file
stream = io.BytesIO()

endpoint = "https://yiwmrr53ce.execute-api.us-east-1.amazonaws.com/stage/requestUploadURL"

# Get the picture (low resolution, so it should be quite fast)
with picamera.PiCamera() as camera:
    camera.resolution = (320, 240)

    while True:
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
        cv2.imwrite('./results/face.jpg', image)

        # Draw a rectangle around every found face
        for (x,y,w,h) in faces:
            cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)

        # Save the debug image
        cv2.imwrite('./results/debug.jpg', image)
        if len(faces) > 0:
                # Get a S3 upload url
                data = {
                    "name": datetime.datetime.now().isoformat(),
                    "type": "image/jpeg"
                }
                print data
                resp = requests.post(endpoint, json=data)
                print(resp.json())
