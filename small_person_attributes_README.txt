Read Me File
10/27/2020
Bryan

The small_person_attributes.py file uses the Microsoft Cognitive Services Face API by running a script against pictures of individual people on webcam to give information on their head pose, smile, and emotions.
Pictures are labeled as "sec4_name.jpg" and need to be in the same root directory for the file to run.

Inputs in root directory:
1. Small_person_attributes.py
2. JPGs of individual faces in the "sec4_name.jpg" format


Output is a csv file with:
1. The name of the individual (taken from name inside sec4_name.jpg) - String
2. Smile - Boolean
3. Head_pose
	a. Roll - Float
	b. Yaw - Float
	c. Pitch - Float
4. Emotions (a-h are float values that add up to 1)
	a. Anger
	b. Contempt
	c. Disgust
	d. Fear
	e. Happiness
	f. Neutral
	g. Sadness
	h. Surprise
