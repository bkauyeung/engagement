import asyncio
import io
import glob
import os
import sys
import time
import uuid
import requests
import pandas as pd
from urllib.parse import urlparse
from io import BytesIO
# To install this module, run:
# python -m pip install Pillow
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person


###################################### INITIALIZE
# This key will serve all examples in this document.
KEY = "cd320c37933e4679bc822d2d3a12a3ef"
# This endpoint will be used in all examples in this quickstart.
ENDPOINT = "https://bryantenor2.cognitiveservices.azure.com/"
# Create an authenticated FaceClient.
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
# Display the image in the users default image browser.
picture = "trick.jpg"
section = "sec4"
######################################

'''
Detect a face in an image that contains a single face.
We use Face detection model 2 because we are not retrieving attributes.
'''
def train_individual_faces(section):
    print()
    print('DETECT FACES')
    print()
    images = [file for file in glob.glob('*.jpg') if file.startswith(section)]
    detected_face_id = {}
    for image_jpg in images:
        test_image_array = glob.glob(image_jpg)
        image = open(test_image_array[0], 'r+b')
        pic = face_client.face.detect_with_stream(image, detectionModel='detection_02')
        if not pic:
               raise Exception('No face detected from image {}'.format(single_image_name))
        detected_face_id[pic[0].face_id] = str(image_jpg[5:-4])

        # Display the detected face ID in the first single-face image.
        # Face IDs are used for comparison to faces (their IDs) detected in other images.
        print('Detected face and created ID from', str(image_jpg), ':', pic[0].face_id)
    return detected_face_id

def identify_faces(image_jpg):
    test_image_array = glob.glob(image_jpg)
    image = open(test_image_array[0], 'r+b')

    # We use detection model 3 because we are retrieving attributes.
    detected_faces3 = face_client.face.detect_with_stream(image, detectionModel='detection_03', return_face_attributes = ['age', 'headPose', 'smile','emotion'], return_Face_Id= True)
    saved_ids = []
    print('Detected face IDs from', image, ':')
    if not detected_faces3:
        raise Exception('No face detected from image {}.'.format(image))
    else:
        for face in detected_faces3:
            saved_ids.append(face.face_id)
            # print(face.face_id)
            # print(face.face_attributes.emotion.as_dict())

    if not detected_faces3:
        raise Exception('No face detected from image {}'.format(multi_image_name))
    return detected_faces3, saved_ids

def get_attributes(face_model, names_location):

    # Create a dictionary of just the IDs and the names found from my similar matching.
    val_list = list(names_location.values())
    ids = [i['Face_ID'] for i in val_list]
    important = dict(zip(ids, names_location.keys()))

    df = pd.DataFrame()
    cols = ['id', 'name', 'smile', 'roll', 'yaw', 'pitch', 'anger', 'contempt', 'disgust', 'fear', 'happiness', 'neutral', 'sadness', 'surprise']

    for face in face_model:
        image_attributes = {}

        head_pose = face.face_attributes.head_pose.as_dict()
        emotion = face.face_attributes.emotion.as_dict()
        image_attributes['id'] = face.face_id
        if face.face_id in list(important.keys()):
            image_attributes['name'] = important[face.face_id]
        else:
            image_attributes['name'] = "Unknown"
        image_attributes['smile'] = face.face_attributes.smile
        image_attributes['roll'] = head_pose['roll']
        image_attributes['yaw'] = head_pose['yaw']
        image_attributes['pitch'] = head_pose['pitch']
        image_attributes['anger'] = emotion['anger']
        image_attributes['contempt'] = emotion['contempt']
        image_attributes['disgust'] = emotion['disgust']
        image_attributes['fear'] = emotion['fear']
        image_attributes['happiness'] = emotion['happiness']
        image_attributes['neutral'] = emotion['neutral']
        image_attributes['sadness'] = emotion['sadness']
        image_attributes['surprise'] = emotion['surprise']
        df = df.append(image_attributes, ignore_index=True)
    df = df[cols]
    return df

def export_data(df):
    df.to_csv('output.csv', index=False)

# Convert width height to a point in a rectangle
def getRectangle(faceDictionary):
    rect = faceDictionary.face_rectangle
    left = rect.left
    top = rect.top
    right = left + rect.width
    bottom = top + rect.height
    return ((left, top), (right, bottom))

# For each face returned use the face rectangle and draw a red box.
def draw_rectangles(image_jpg, face_model, name_location):
    picture = Image.open(image_jpg)
    print('Drawing rectangle around face.')
    draw = ImageDraw.Draw(picture)
    for i in range(len(face_model)):
    # for face in face_model:
        rectangle = getRectangle(face_model[i])
        draw.rectangle(rectangle, outline='red')
        # draw.multiline_text((rectangle[0][0], rectangle[0][1]), text=face.face_id)
    for i in name_location.keys():
        draw.multiline_text((name_location[i]['Left'], name_location[i]['Top']), text=i)
    picture.show()


def find_similar(face_model, individual_face_ids):
    print('-----------------------------')
    print()
    print('FINDING SIMILAR FACES IN GROUP PICTURE TO THE FIRST PICTURES...')
    # Search through faces detected in group image for the single face from first image.
    # First, create a list of the face IDs found in the second image.
    second_image_face_IDs = list(map(lambda x: x.face_id, face_model))
    # Next, find similar face IDs like the one detected in the first image.
    names = []
    locations = {}
    for i in individual_face_ids.keys():
        similar_faces = face_client.face.find_similar(face_id=i, face_ids=second_image_face_IDs)
        if not similar_faces:
            print(individual_face_ids[i], 'is missing from the picture.')
            names.append("Unknown")

        # The similar faces are matched using the Cognitive Services algorithm in find_similar().
        for face in similar_faces:
            print('We found', individual_face_ids[i], 'in', picture + ':', 'with confidence of', face.confidence)
            names.append(individual_face_ids[i])
            first_image_face_ID = face.face_id
            face_info = next(x for x in face_model if x.face_id == first_image_face_ID)
            if face_info:
                individual_attributes = {}
                individual_attributes['Face_ID'] = first_image_face_ID
                individual_attributes['Left'] = face_info.face_rectangle.left
                individual_attributes['Top'] = face_info.face_rectangle.top
                individual_attributes['Width'] = face_info.face_rectangle.width
                individual_attributes['Height'] = face_info.face_rectangle.height
            locations[individual_face_ids[i]] = individual_attributes
    print("You originally have", len(individual_face_ids.keys()), 'students. This group picture detects', len(second_image_face_IDs), 'faces.')
    return names, locations


detected_face_id = train_individual_faces(section)
detected_faces3, saved_ids = identify_faces(picture)
names, names_location = find_similar(detected_faces3, detected_face_id)
attributes = get_attributes(detected_faces3, names_location)
print(attributes)
export_data(attributes)
draw_rectangles(picture, detected_faces3, names_location)
