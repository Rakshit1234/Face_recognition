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

# getTrainingData.py

import cv2, sys, numpy, os, time

counter = 0
scale = 4
noOfPics = 100

#Get the name of the person whose pictures are being captured
nameOfPerson = sys.argv[1]

#Find or create the folder containing training data (Pictures)
db = 'database'
path = os.path.join(db, nameOfPerson)
if not os.path.isdir(path):
    os.makedirs(path)

#Fetch trained frontal face classifier
haarFaceClassifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#Capture a frame from camera
webcam = cv2.VideoCapture(0)

#Set the resolution of the camera
webcam.set(3,320)
webcam.set(4,240)

print "Camera on"


#Loop until the required number of pics are captured
while counter < noOfPics:

    #Grab a frame
    (rval,im) = webcam.read()

    #Process frame and detect faces
    im = cv2.flip(im, 1, 0)
    imGrayscale = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    imScaled = cv2.resize(imGrayscale, (imGrayscale.shape[1] / scale, imGrayscale.shape[0] / scale))
    faces = haarFaceClassifier.detectMultiScale(imScaled)
    faces = sorted(faces, key=lambda x: x[3])

    #If faces found, resize and write to database
    if faces:

        print("Face captured")
        print(counter)

        faceOne = faces[0]
        (x, y, w, h) = [v * scale for v in faceOne]
        face = imGrayscale[y:y + h, x:x + w]
        faceResized = cv2.resize(face, (112, 92))
        pin=sorted([int(n[:n.find('.')]) for n in os.listdir(path)
               if n[0]!='.' ]+[0])[-1] + 1
        cv2.imwrite('%s/%s.png' % (path, pin), faceResized)
	time.sleep(0.4)
	counter += 1

print str(counter) + " images saved to " + nameOfPerson +" folder in database "
