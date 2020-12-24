import cv2
import numpy as np
import os, sys

## Change accordingly - the folder where your video files reside
image_link = "C:/Users/bkauy/OneDrive/Desktop/241_Final_Project/videos_and_frames/raw_individual/"

def normalize_image(image_path):
    img =cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    # print('Original Dimensions : ',img.shape)
    # Captures most information in this rectangle coordinates
    width=310
    height=170
    dim = (width, height)
    # resize image
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    return resized

############# Blackout Names by creating two rectangles outside of the names and do bitwise operation
# Create the two rectangles with perimeters of the space we want to capture.
# Rectangle 1
def blackout_names_and_save(image):
    # These settings are what worked for my zoom images.
    start1 = (0,0)
    end1 = (160,140)

    # Rectangle 2
    start2 = (160,0)
    end2 = (310,170)

    # White mask color
    color = (255, 255, 255)
    # img = cv2.imread('test.jpg')
    # Draw a filled rectangle on black background as a mask
    mask = np.zeros_like(image)
    mask1 = cv2.rectangle(mask, start1, end1, color, -1)
    mask2 = cv2.rectangle(mask, start2, end2, color, -1)
    # Combine both masks into one
    mask_final = cv2.bitwise_and(mask1, mask2)

    # combine the mask with the resized image using bitwise logic.
    result = cv2.bitwise_and(image, mask_final)

    os.chdir("C:/Users/bkauy/OneDrive/Desktop/241_Final_Project/videos_and_frames/cleaned_individual")
    # cv2.imshow('masked image', result)
    cv2.imwrite(filename+'_clean.jpg', result)


for filename in os.listdir(image_link):
    image_path = image_link + filename
    result = normalize_image(image_path)
    blackout_names_and_save(result)


