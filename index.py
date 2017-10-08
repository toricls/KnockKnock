import boto3
import requests
import os
client = boto3.client('rekognition')

rpi_endpoint = os.environ.get('RPI_ENDPOINT')
slack_endpoint = os.environ.get('SLACK_ENDPOINT')

def detect(event, context):
    print event
    image_url = "https://s3.amazonaws.com/%s/%s" % (event['Records'][0]['s3']['bucket']['name'], event['Records'][0]['s3']['object']['key'])
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
        slack_msg = "Something happened at your door: %s" % image_url
        print slack_msg
        data = {
            "text": slack_msg
        }
        requests.post(slack_endpoint, json=data)
        return None
    print response
    try:
        name = response['FaceMatches'][0]['Face']['ExternalImageId']
    except:
        print "WUT"
        return None

    # we found a face, woohoo!
    slack_msg = "%s is at your door: %s" % (name, image_url)
    data = {
        "text": slack_msg
    }
    print slack_msg
    requests.post(slack_endpoint, json=data)

    # let's generate an mp3
    url = "https://yiwmrr53ce.execute-api.us-east-1.amazonaws.com/stage/mp3"
    resp = requests.post(url, json={"text": "%s is here!" % name})
    print resp.json()

    mp3_url = resp.json()['mp3URL']

    # start waving
    resp = requests.get("%s/wave" % rpi_endpoint)
