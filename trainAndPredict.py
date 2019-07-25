# -------------------------------------------------------------------------------------------------------------------
# Automated Door Lock with Facial Recognition and Voice Output on BeagleBone Black Wireless (powered by OSD335x)
# -------------------------------------------------------------------------------------------------------------------
#
# License:   Copyright 2018, Octavo Systems, LLC. All rights reserved.
#
# The Software is available for download and use subject to the terms and
# conditions of this License. Access or use of the Software constitutes
# acceptance and agreement to the terms and conditions of this License.
#
# Redistribution and use of the Software in source and binary forms, with
# or without modification, are permitted provided that the following conditions
# are met:
#   - Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the capitalized paragraph below.
#   - Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the capitalized paragraph below in the
#     documentation and/or other materials provided with the distribution.
#
# The names of the software's authors or their organizations may not be used
# to endorse or promote products derived from the Software without specific
# prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
# THE POSSIBILITY OF SUCH DAMAGE.
#
# ------------------------------------------------------------------------------------------------------------------

# trainAndPredict.py

import cv2, sys, numpy, os,pyttsx,time
import Adafruit_BBIO.GPIO as GPIO

from subprocess import call
import os


GPIO.setup("P8_12", GPIO.OUT) # Motor driver control
GPIO.setup("P8_14", GPIO.OUT) # Motor driver control
GPIO.setup("P8_16", GPIO.IN)  # Read motion sensor

GPIO.output("P8_12",GPIO.LOW)
GPIO.output("P8_14",GPIO.LOW)


scale = 4
db = 'database'

tOpen = 5.3 # No. of seconds to run the motor to open door
tClose = 4 # No. of seconds to run the motor to close door
tIdle = 10 # No. of seconds to remain idle between door opening and closing
tIdle2 = 2

faceFound=0

unknownFace=0 # Number of checks for unknown face
unknownThresh = 500 # Threshold to filter unknown ppl


######################### Function to Open and Close the door #################

def manage_door(dOpen,dIdle,dClose,dIdle2):

	GPIO.output("P8_12",GPIO.HIGH) # Open door
	GPIO.output("P8_14",GPIO.LOW)
	print("Door opened")
	time.sleep(dOpen)

	GPIO.output("P8_12",GPIO.LOW) # Door idle
    	GPIO.output("P8_14",GPIO.LOW)
	time.sleep(dIdle)

	GPIO.output("P8_12",GPIO.LOW) # Close door
	GPIO.output("P8_14",GPIO.HIGH)
	print("Door closed")
	time.sleep(dClose)

	GPIO.output("P8_12",GPIO.LOW) # Door idle
	GPIO.output("P8_14",GPIO.LOW)
	time.sleep(dIdle2)

###############################################################################


# Collect training data from database
(images, lables, names, id) = ([], [], {}, 0)
for (subdirs, dirs, files) in os.walk(db):
    for subdir in dirs:
        names[id] = subdir
        subjectpath = os.path.join(db, subdir)
        for filename in os.listdir(subjectpath):
            path = subjectpath + '/' + filename
            lable = id
	    images.append(cv2.imread(path, 0))
            lables.append(int(lable))
        id += 1

# Create a array of images and labels from training data
print("Collecting Training Data")
(images, lables) = [numpy.array(lis) for lis in [images, lables]]

# Train FisherFaceRecognizer from the training data
print("Training in progress")
model = cv2.face.createFisherFaceRecognizer()
model.train(images, lables)

#Fetch trained frontal face classifier
haarFaceClassifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#Capture a frame from camera
webcam = cv2.VideoCapture(0)

#Set the resolution of the camera
webcam.set(3,320)
webcam.set(4,240)

print("Face Recognition in progress")

while True:

	if(faceFound==1):
		wasteFrameCount = 10
		while(wasteFrameCount > 0):
			print("Frame wasted")
			(rval,im) = webcam.read() # clear camera buffer by grabbing frames and not doing anything with them once a face is found
			wasteFrameCount=wasteFrameCount-1
		faceFound=0
	else:
		(rval,im) = webcam.read()


	im = cv2.flip(im, 1, 0)
	imGrayscale = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
	imScaled = cv2.resize(imGrayscale, (imGrayscale.shape[1] / scale, imGrayscale.shape[0] / scale))
	faces = haarFaceClassifier.detectMultiScale(imScaled)
	faces = sorted(faces, key=lambda x: x[3])

	if faces:

		faceFound=1
       		print("Face found")
        	faceOne = faces[0]
        	(x, y, w, h) = [v * scale for v in faceOne]
        	face = imGrayscale[y:y + h, x:x + w]
        	faceResized = cv2.resize(face, (112, 92))

        	lableIndex = model.predict(faceResized)
		lableText = names[lableIndex[0]]

		print("Name of the person is:")
		print(lableText)
		print("Confidence Level of prediction is")
		print(lableIndex[1])

        # Check lable name and confidence level
		if((lableText=="basu")&(lableIndex[1]<unknownThresh)):
			call(["flite","-voice","rms","-t","Welcome Basu"])
			manage_door(tOpen,tIdle,tClose,tIdle2)
		        unknownFace = 0

		elif(lableIndex[1]>unknownThresh):
			unknownFace=unknownFace+1

			if(unknownFace==3): # declare a person unknown only if 3 consecutive frames from the camera are unknown
				call(["flite","-voice","rms","-t","You are not authorized to access this area"])
				unknownFace=0


	# read Motion Click to check if anyone is trying to  move out of the building
	if GPIO.input("P8_16"):
		call(["flite","-voice","rms","-t","See you soon"])
		manage_door(tOpen,tIdle,tClose,tIdle2)
