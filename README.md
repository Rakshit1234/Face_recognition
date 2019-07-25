-------------------------------------------------------------------------------------------------------------------
Automated Door Lock with Facial Recognition and Voice Output on BeagleBone Black Wireless (powered by OSD335x)
-------------------------------------------------------------------------------------------------------------------

License:   Copyright 2018, Octavo Systems, LLC. All rights reserved.
           
The Software is available for download and use subject to the terms and 
conditions of this License. Access or use of the Software constitutes 
acceptance and agreement to the terms and conditions of this License.

Redistribution and use of the Software in source and binary forms, with 
or without modification, are permitted provided that the following conditions 
are met:
  - Redistributions of source code must retain the above copyright notice, 
    this list of conditions and the capitalized paragraph below.
  - Redistributions in binary form must reproduce the above copyright notice, 
    this list of conditions and the capitalized paragraph below in the 
    documentation and/or other materials provided with the distribution.

The names of the software's authors or their organizations may not be used 
to endorse or promote products derived from the Software without specific 
prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE 
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF 
THE POSSIBILITY OF SUCH DAMAGE.

----------------------------------------------------------------------------------------------------------------

Overview:

The objective of this project is to automate any office/home door(preinstalled with door closer).
The project uses OpenCV Fisher Face Recognizer to recognize the face of people who are trying to enter the room. 
A geared DC Motor is used to actually open the door. A motion click is used to detect indoor motion and open the
door for anyone trying to leave the room. "Flite" voice synthesizer is used to output suitable greeting messages.


Procedure to build OpenCV and run the project code on BeagleBone Black Wireless:

1. Get the latest Debian image from https://beagleboard.org/latest-images

2. Burn the image to an SD card (minimum 8GB required for this project) using the instructions from:
   https://beagleboard.org/getting-started#update

3. Expand the File System of your SD card from 4GB to 8GB using the instructions from (See Note below): 
   http://dev.iachieved.it/iachievedit/expanding-your-beaglebone-microsd-filesystem/

   NOTE: In step 6, set the First Sector to 8192 instead of leaving it blank

4. Copy the given files (installScript.sh, getTrainingData.py, trainAndPredict.py,haarcascade_frontalface_default.xml) to the 
   same directory on your BeagleBone Black Wireless.

5. Make the install script executable:

   ```sudo chmod +x installScript.sh```
   
6. Run installScript.sh

   The script will install all the necessary dependencies and download OpenCV 3.1.0. 

   A few issues were found during the build process of OpenCV. Hence, the last 7 lines of this script (installScript.sh) were           
   intentionally commented to prevent the build process of OpenCV. To avoid possible issues during build, apply the following 
   fixes:

   a. To resolve hdf5.h error:
  
   Open common.cmake:
     
    ```nano opencv-3.1.0/modules/python/common.cmake```
   
   Copy and paste the following lines at the end of common.cmake:
     
   ```
   find_package(HDF5)
   include_directories(${HDF5_INCLUDE_DIRS})
   ```
     
   Save and close the file.
     
   b. OpenCV "predict confidence" wrapper workaround:
  
   Navigate to line 259 of face.hpp

     ```nano opencv_contrib/modules/face/include/opencv2/face.hpp```
     
   Replace the line with:
     
     ```int predict(InputArray src) const;```
     
   Save and close the file.
     
7. Uncomment the last 7 lines of installScript.sh and rerun the script. The OpenCV build process may take 6 to 10 hours to 
   complete.


8. The face recognizer needs atleast 2 sets of pictures to train on. Run getTrainingData.py:

   ```python getTrainingData.py <name of the person in front of the camera>```

   Example:
   
   ```python getTrainingData.py John```
   
   Once the script starts running, the camera will turn on and you will be able to see "Camera on" message on the console.
   Stand right in front of the camera. Once a face is captured, "Face captured" message is displayed on console. A count of
   number of pictures captured is also displayed. Atleast 100 pictures per person is necessary to get good predicton.
   

9. At this point, the Face Recognizer should be ready to Train on the available images and then make Predictions. Run 
   trainAndPredict.py:

   ```python trainAndPredict.py```
   
   The script will display messages on the console as it goes through different phases of training.
   
10. Once "Face Recognition in progress" message is displayed on terminal, the Face Recognizer will be able to predict the name 
of the people standing in front of the camera.
   


   


   
     


