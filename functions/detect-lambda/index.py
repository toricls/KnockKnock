import boto3
import requests
client = boto3.client('rekognition')

def handler(event, context):
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

    try:
        name = response['FaceMatches'][0]['Face']['ImageId']['ExternalImageId']
    except:
        print "WUT"
        return None
    url = "https://yiwmrr53ce.execute-api.us-east-1.amazonaws.com/stage/mp3"
    resp = request.post(url, data={"text": "%s is here!" % name})
    print resp.json()

    url = resp.json()['mp3URL']
    print url
