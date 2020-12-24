11/15/2020
Bryan Notes


Video Recordings from isvc needed to be adjusted for download. I first downloaded zoom recordings from a shared link by exposing the download link through the front end html. You can then right click the link to download the file locally. On Windows, you need to also download right click plugin for this to work. https://www.youtube.com/watch?v=Y0VQfQCN4BA.
I took available video recordings in gallery mode from the following classes on the given day(s).

W203 Gunnar - May 15, 2019
W203 Mark - May 11, 2019
W203 Paul - May 8, 2019
W261 Ramki - May 26, 2020
W266 Mark - Jan 23, 2020
W266 Sid - Jan 25, 2020

I ran each recording under VLC Media Player and saw that most videos were recorded at 25 fps. To get discrete clips equally spaced, I used VLC to save static screenshots at 12 fps so that we would get an average of 2 frames per second. I randomly chose 3 or 4 spots to generate screenshots throughout the recorded lecture and saved them into a file. Please see how I did this here: https://www.youtube.com/watch?v=2Lt1lcyweTw

Then I downloaded Photoshop (Adobe Creative Cloud is free for students) and was able to crop individual pictures out of the gallery mode and store them as individual pictures. Cropping multiple fields inside an image is called slicing. Automating this process in Photoshop is called batch processing. Batch slicing can be done by creating a Photoshop "action" that records your slicing process and using a special save called Export -> Save as Web Page. When you batch slice, remember not to touch the default naming convention or you will run into issues saving the photos (They will write over each other. If you planned on getting 15 frames by 10 images, you will get 1 frame by 10 images instead.)

These photos were originally cropped to avoid the name and protect anonymity. These 730+ photos were not normalized and are stored in the file called "Miscellaneous". The new thing I plan on doing is normalizing the photos and cropping the entire screen but normalizing the size and equally blurring out the individuals names to keep it anonymous. 

Normalization and Anonymizing (Blacking out Names)
I normalized all frames to 310x170. Most images cropped from photoshop and zoom were slightly larger than this, so it is good that I captured most of the image with the aspect ratio here. Then I blacked out the bottom left portion of the names provided by zoom in the frame using cv2.bitwise function. The python file is called normalized_and_cleaned.py


