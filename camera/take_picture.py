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

    stream = io.BytesIO()
    camera.capture(stream, format='jpeg')

    # Convert the picture into a numpy array
    buff = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)

    # Now creates an OpenCV image
    image = cv2.imdecode(buff, 1)

    cv2.imwrite('./results/face.jpg', image)

    # Get a S3 upload url
    data = {
        "name": "camera/%s.jpg" % datetime.datetime.now().isoformat(),
        "type": "image/jpeg"
    }
    resp = requests.post(endpoint, json=data)
    print(resp.json()['uploadURL'])

    resp = requests.put(resp.json()['uploadURL'], data=open('./results/face.jpg', 'rb').read(), headers={'Content-type': 'image/jpeg'})
    print resp
