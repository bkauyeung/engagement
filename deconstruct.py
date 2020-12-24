import sys
from PIL import Image
import os

OFFSET_Y = 154
TILE_WIDTH = 480
TILE_HEIGHT = 270
BLUR_RADIUS = 10
TILES_PER_ROW = 4

def is_all_black(image, ux, uy, w, h):
    for x in range(ux, ux + w):
        for y in range(uy, uy + h):
            if image.getpixel((x, y)) != (0, 0, 0):
                print(x, y, image.getpixel((x, y)))
                return False
    return True

def detect_num_participants(screenshot):
    # For now this assumes the number is between 8 and 12

    if is_all_black(screenshot, TILE_WIDTH // 2, OFFSET_Y + 2 * TILE_HEIGHT + BLUR_RADIUS, 100, 100):
        return 10
    elif is_all_black(screenshot, 0, OFFSET_Y + 2 * TILE_HEIGHT + BLUR_RADIUS, 100, 100):
        return 11
    else:
        return 12

def extract_participant_image(screenshot, num_participants, index):
    """
    Returns a subimage for the given participant's camera view.

    Note: This still refers to the original image. If you need to change it call load().
    """
    row = index // TILES_PER_ROW
    col = index % TILES_PER_ROW
    y = OFFSET_Y + TILE_HEIGHT * row

    if row < 2 or num_participants == 12:
        row_x_offset = 0
    elif num_participants == 11:
        row_x_offset = TILE_WIDTH // 2
    elif num_participants == 10:
        row_x_offset = TILE_WIDTH

    x = row_x_offset + TILE_WIDTH * col

    return screenshot.crop((x, y, x + TILE_WIDTH - 1, y + TILE_HEIGHT - 1))


# img = Image.open(sys.argv[1])
path="C:/Users/bkauy/OneDrive/Desktop/241_Final_Project/videos_and_frames/treatment/pilot_s4_batch2Result/"
picture_number = 0
for image in os.listdir(path):
    img = Image.open(image)
    np = detect_num_participants(img)

    for i in range(np):
        subimg = extract_participant_image(img, np, i)
        subimg.save("{}/{}.jpg".format(picture_number,i))
        picture_number +=1
