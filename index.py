import boto3
import requests
client = boto3.client('rekognition')

rpi_endpoint = "http://ba753c15.ngrok.io"

def detect(event, context):
    print event
    image = {
            'S3Object': {
                'Bucket': event['Records'][0]['s3']['bucket']['name'],
                'Name': event['Records'][0]['s3']['object']['key']
            }
        }
    print image
    try:
        response = client.search_faces_by_image(
            CollectionId='knockknock',
            Image=image,
            MaxFaces=1,
        )
    except:
        print "No face found"
        return None
    print response
    try:
        name = response['FaceMatches'][0]['Face']['ExternalImageId']
    except:
        print "WUT"
        return None

    # we found a face, woohoo!

    # let's generate an mp3
    url = "https://yiwmrr53ce.execute-api.us-east-1.amazonaws.com/stage/mp3"
    resp = requests.post(url, json={"text": "%s is here!" % name})
    print resp.json()

    mp3_url = resp.json()['mp3URL']

    # start waving
    resp = requests.get("%s/wave" % rpi_endpoint)

    # blink the led
    resp = requests.get("%s/blink" % rpi_endpoint)
