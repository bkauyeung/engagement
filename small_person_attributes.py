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

# This key will serve all examples in this document.
KEY = "cd320c37933e4679bc822d2d3a12a3ef"
# This endpoint will be used in all examples in this quickstart.
ENDPOINT = "https://bryantenor2.cognitiveservices.azure.com/"
# Create an authenticated FaceClient.
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
# Change to whatever you name the beginning of  your jpg.
section = 'sec4'


###############
# Detect faces
def get_attributes(image_file):
    test_image_array = glob.glob(image_file)
    image = open(test_image_array[0], 'r+b')
    faces = face_client.face.detect_with_stream(image, detectionModel='detection_03', return_face_attributes = ['age', 'headPose', 'smile','emotion'], return_Face_Id= True)
    image_attributes = {}
    for face in faces:
        head_pose = face.face_attributes.head_pose.as_dict()
        emotion = face.face_attributes.emotion.as_dict()
        image_attributes['name'] = str(image_file)[5:-4]
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
    return image_attributes

def export_data():
    cols = ['name', 'smile', 'roll', 'yaw', 'pitch', 'anger', 'contempt', 'disgust', 'fear', 'happiness', 'neutral', 'sadness', 'surprise']
    df = pd.DataFrame()
    images = [file for file in glob.glob('*.jpg') if file.startswith(section)]
    for image in images:
        df = df.append(get_attributes(image), ignore_index=True)
    df = df[cols]
    df.to_csv('class_snapshot.csv', index=False)
    return df

export_data()
