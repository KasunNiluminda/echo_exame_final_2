import cv2
import os
import time
import sys
from roboflow import Roboflow
import cv2
import sys
# ... Other imports and code ...

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python your_script.py <image_data>")
        sys.exit(1)

    image_data = sys.argv[1]

# Roboflow model setup (assuming the provided API keys and model details are accurate)
rf1 = Roboflow(api_key="lnQxs4tjd5OyXc6fQwJ1")
rf2 = Roboflow(api_key="lnQxs4tjd5OyXc6fQwJ1")
rf3 = Roboflow(api_key="lnQxs4tjd5OyXc6fQwJ1")
project1 = rf1.workspace().project("custom_book_detection")
project2 = rf2.workspace().project("phone-finder")
project3 = rf3.workspace().project("monitordetection-buevj")
model1 = project1.version(2).model
model2 = project2.version(4).model
model3 = project3.version(4).model


# Get the directory path where the Python script is located using sys.argv[0]
current_directory = os.path.dirname(os.path.abspath(sys.argv[0]))

# Define the cascades directory path (relative to the current directory)
cascades_directory = os.path.join(current_directory, "cascades")

# Check if the cascades directory exists
if not os.path.exists(cascades_directory):
    print("Error: 'cascades' directory not found. Please ensure the directory exists.")
    sys.exit(1)

# List of required cascade file names
cascade_files = [
    "haarcascade_upperbody.xml",
    "haarcascade_frontalface_default.xml",
    "haarcascade_eye.xml",
    "haarcascade_mcs_nose.xml"
]

# Check for the existence of all required cascade files
missing_files = [file for file in cascade_files if not os.path.exists(os.path.join(cascades_directory, file))]

if missing_files:
    print(f"Error: One or more cascade files not found: {', '.join(missing_files)}")
    sys.exit(1)

# Load Haar cascade classifiers
bodyCascade = cv2.CascadeClassifier(os.path.join(cascades_directory, "haarcascade_upperbody.xml"))
faceCascade = cv2.CascadeClassifier(os.path.join(cascades_directory, "haarcascade_frontalface_default.xml"))
eyeCascade = cv2.CascadeClassifier(os.path.join(cascades_directory, "haarcascade_eye.xml"))
noseCascade = cv2.CascadeClassifier(os.path.join(cascades_directory, "haarcascade_mcs_nose.xml"))


# Video capture setup for inbuilt and portable cameras
video_capture = cv2.VideoCapture(0)
video_capture1 = cv2.VideoCapture(1)

# Window setup
cv2.namedWindow("Webcam Stream", cv2.WINDOW_NORMAL)
cv2.namedWindow("Portable Camera Stream", cv2.WINDOW_NORMAL)

# Define other variables and constants
start_time = None
detection_timeout = 5
detection_flag = False


while True:
    ret, frames = video_capture.read()      #get the frames from the inbuilt camera video
    ret1, frame1 = video_capture1.read()      #get the frames from the inbuilt camera video
    gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)     #convert images of inbuilt camera video capture from BGR format into gray scale
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)    #convert images of portable camera video capture from BGR format into gray scale
    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30),
                                         flags=cv2.CASCADE_SCALE_IMAGE)     #if there is a face, get the output of its region coordinates
    bodies = bodyCascade.detectMultiScale(gray1, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30),
                                         flags=cv2.CASCADE_SCALE_IMAGE)     #if there is a body, get the output of its region coordinates
    if len(faces) > 0:      #check whether there is any face
        start_time = time.time()    #get the time of this moment
        detection_flag = True       #if there is any faces this will be get true

    if detection_flag and time.time() - start_time > detection_timeout:
        # If no eyes or noses are detected within the predefined time region(detection_timeout), show notification
        if len(eyes) == 0 and len(noses) == 0:
            cv2.putText(frames, "No face, eyes, or nose detected!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,(0, 0, 255), 2)
    for (x, y, w, h) in faces:
        # Draw a rectangle around the face
        cv2.rectangle(frames, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frames, "face", (x,y-2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)       #put a text named "face" on the rectangle
        if len(faces)>1:
             cv2.putText(frames, "Cheating", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)     #if there are more than 1 face , show a text named "cheating" on th top left corner of the window

        # Extract the region of interest (ROI) within the face rectangle
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frames[y:y + h, x:x + w]

        # Perform eye detection within the face ROI
        eyes = eyeCascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            # Draw a rectangle around each detected eye
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 0, 255), 2)

        # Perform nose detection within the face ROI
        noses = noseCascade.detectMultiScale(roi_gray)
        for (nx, ny, nw, nh) in noses:
            # Draw a rectangle around the detected nose
            cv2.rectangle(roi_color, (nx, ny), (nx + nw, ny + nh), (255, 0, 0), 2)
            
    cv2.imshow("Webcam Stream", frames)     #show the video capture of the inbuilt camera

    
    for (x, y, w, h) in bodies:
        # Draw a rectangle around the face
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame1, "Person", (x,y-2), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)      #put a text named "Person" on the rectangle
        if len(bodies)>1:
            cv2.putText(frame1, "Cheating", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)       #if there are more than 1 body , show a text named "cheating" on th top left corner of the window


    if ret1:
        a = model1.predict(frame1, confidence=40, overlap=30).json()        #if there is any notebook, show the give the output including its coordinates
        Notebook = []
        for predictions in a['predictions']:
            Notebook.append([predictions['x'], predictions['y'], predictions['width'], predictions['height']])      #put coordinates of the cener of the notebook region, width,height and put them in to Notebook list
            print(Notebook)     #print the Notebook list
            x, y, w, h = int(predictions['x']), int(predictions['y']), int(predictions['width']), int(predictions['height'])        #define variable for above parameters
            #x1=x-w/2,x2=x+w/2,y1=y+h/2,y2=y-h/2
            cv2.rectangle(frame1, (int(x-w/2), int(y+h/2)), (int(x+w/2), int(y-h/2)), (255, 0, 0), 2)       #draw the rectangle around the notebook
            cv2.putText(frame1, "NoteBook", (int(x-w/2),int(y+h/2)-2), cv2.FONT_HERSHEY_SIMPLEX, .75, (255, 0, 0), 2)       #put a text named "Notebook on that rectangle"
            cv2.putText(frame1, "Cheating", (0,20), cv2.FONT_HERSHEY_SIMPLEX, .75, (0, 0, 255), 2)      #put a text named "cheating on the top left corner of the window"


        #this is for mobile phone detecting and the process is same as above
        b = model2.predict(frame1, confidence=40, overlap=30).json()
        mobiles = []
        for predictions in b['predictions']:
            mobiles.append([predictions['x'], predictions['y'], predictions['width'], predictions['height']])
            print(mobiles)
            x, y, w, h = int(predictions['x']), int(predictions['y']), int(predictions['width']), int(predictions['height'])
            cv2.rectangle(frame1, (int(x-w/2), int(y+h/2)), (int(x+w/2), int(y-h/2)), (0, 0, 255), 2)
            cv2.putText(frame1, "Phone", (int(x-w/2),int(y+h/2)-2), cv2.FONT_HERSHEY_SIMPLEX, .75, (0, 0, 255), 2)
            cv2.putText(frame1, "Cheating", (0,20), cv2.FONT_HERSHEY_SIMPLEX, .75, (0, 0, 255), 2)
       
        #this is for mobile phone detecting and the process is same as above
        c = model3.predict(frame1, confidence=40, overlap=30).json()
        Moniters = []
        for predictions in c['predictions']:
            Moniters.append([predictions['x'], predictions['y'], predictions['width'], predictions['height']])
            print(Moniters)
            x, y, w, h = int(predictions['x']), int(predictions['y']), int(predictions['width']), int(predictions['height'])
            cv2.rectangle(frame1, (int(x-w/2), int(y+h/2)), (int(x+w/2), int(y-h/2)), (0, 255, 0), 2)
            cv2.putText(frame1, "Moniter", (int(x-w/2),int(y+h/2)-2), cv2.FONT_HERSHEY_SIMPLEX, .75, (0, 255, 0), 2)
            if len(Moniters)>1:
                cv2.putText(frame1, "Cheating", (0,20), cv2.FONT_HERSHEY_SIMPLEX, .75, (0, 0, 255), 2)      #if there is more than 1 moniter, show the text named cheating
        

        
        cv2.imshow("Portable Camera Stream", frame1)        #show the video capture of the inbuilt camera

    #command to quit the program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


#finish the video captures from both cameras
video_capture.release()
video_capture1.release()
cv2.destroyAllWindows()     #close all windows

 



# import cv2      #import opencv library for video processing
# import os       #import os library
# import time     #import time library for get the time related outputs
# from roboflow import Roboflow       #import Roboflow library to apply detecting models


# rf1 = Roboflow(api_key="lnQxs4tjd5OyXc6fQwJ1")   #call the API KEY of the book detecting model
# rf2 = Roboflow(api_key="lnQxs4tjd5OyXc6fQwJ1")   #call the API KEY of the phone detecting model
# rf3 = Roboflow(api_key="lnQxs4tjd5OyXc6fQwJ1")   #call the API KEY of the monitor detecting model
# project1 = rf1.workspace().project("custom_book_detection")     #call the model name of the book detecting model
# project2 = rf2.workspace().project("phone-finder")      #call the model name of the phone detecting model
# project3 = rf3.workspace().project("monitordetection-buevj")        #call the model monitor of the book detecting model
# model1 = project1.version(2).model      #define the name for book detecting model
# model2 = project2.version(4).model      #define the name for phone detecting model
# model3 = project3.version(4).model      #define the name for monitor detecting model
# bodyCascadePath = os.path.dirname(cv2.__file__) + "D:\work\campus projects\ongoing project\voice\videomodel2\final\final\haarcascade_upperbody.xml"     #define the path for upperbody detecting model
# faceCascadePath = os.path.dirname(cv2.__file__) + "D:\work\campus projects\ongoing project\voice\videomodel2\final\final\haarcascade_frontalface_default.xml"       #define the path for face detecting model
# eyeCascadePath = os.path.dirname(cv2.__file__) + "D:\work\campus projects\ongoing project\voice\videomodel2\final\final\haarcascade_eye.xml"        #define the path for eye detecting model
# noseCascadePath = os.path.dirname(cv2.__file__) + "D:\work\campus projects\ongoing project\voice\videomodel2\final\final\haarcascade_mcs_nose.xml"      #define the path for nose detecting model
# bodyCascade = cv2.CascadeClassifier(bodyCascadePath)    #define the name for upperbody detecting model
# faceCascade = cv2.CascadeClassifier(faceCascadePath)    #define the name for face detecting model
# eyeCascade = cv2.CascadeClassifier(eyeCascadePath)      #define the name for eye detecting model
# noseCascade = cv2.CascadeClassifier(noseCascadePath)    #define the name for nose detecting model

# video_capture = cv2.VideoCapture(0)     #get the video input from the inbuilt webcam
# video_capture1 = cv2.VideoCapture(1)     #get the video input from the portable camera

# cv2.namedWindow("Webcam Stream", cv2.WINDOW_NORMAL)     #name the window of ibuilt web cam video capture
# cv2.namedWindow("Portable Camera Stream", cv2.WINDOW_NORMAL)    #name the window of portable camera video capture


# start_time = None       #define a variable to store the time
# detection_timeout = 5   #define a time range to check the user is looking at the screen or not
# detection_flag = False      #define a variable to identify whether a face is detected or not
