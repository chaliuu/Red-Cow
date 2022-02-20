# Fedoract

Fedoract allows you to control your music in a fun and interactive way. It wireless streams your hand gestures and allows you to control your Spotify with them. 

We are using a camera mounted on a fedora to recognize hand gestures, and depending on which gesture, we can control other home applications using the technology of IoT. 

The camera will be mounted wirelessly on the hat and its video feed will be sent to the main computer to process. 

## About 

The software backend is built using the OpenCV and the mediapipe library. 

The mediapipe library includes a hand model that has been pre-trained using a large set of data and it is very accurate. 

We are using this model to get the positions of different features (or landmarks) of the hand, such as fingertips, the wrist, and the knuckles. Then we are using this information to determine the hand gesture made by the user.  

The Spotify front end is controlled and accessed using the Selenium web driver. Depending on the action determined by hand gesture recognition, the program presses the corresponding button. 

## Setup 

To run this project, you must have `python3` and you need to set up a python environment with the following modules : 

* mediapipe
* opencv-python
* osascript
* pycaw
* selenium
* urllib

You also need to install the chrome driver in the executable path. 

Path for MacOS :

```
/usr/local/bin 
```

For Windows, you need to find the path in the Program Files.

To run the project, use the following command : 

```
python3 hand-tracker/main.py
```