from random import randint
import numpy as np
import time

import cv2
import tkinter as tk
from PIL import Image, ImageTk
from copy import deepcopy
from gpt3 import generate_prompt, generate_paragraph, generate_good_bye

from get_face import age_gender_detector, emotion_detector
from facial_recognition import get_celebrity
from voice_interface import speak, mic_input


from os.path import exists

if exists("D:\AlexWork"):
    jeffs_cpu = True
else:
    jeffs_cpu = False


# static variables
temp_img_path = "./images/iron_man.jpeg"

HEIGHT = 209
WIDTH = 140

SHOW_ADEN_PHASE = 0
GET_NAME_PHASE = 1
GET_CELEBRITY_PHASE = 2
SPEAKING_CELEBRITY_PHASE = 3
PHOTO_TRANSITION_PHASE = 3.5
GETTING_INFO_PHASE = 4
SPEAKING_INFO_PHASE = 5
STORY_PHASE = 5.5
SOMEONE_ELSE_PHASE = 6


class App:
    def __init__(self, window, window_title):
        # Create a window and pass it to the Application object
        self.window = window
        self.window.title(window_title)
        
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        
        # Check if the camera is accessible
        if not self.cap.isOpened():
            print("Unable to access camera")
            exit()
        
        # get the image size that we will be using
        self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.output_width = WIDTH
        self.output_height = HEIGHT
        self.size = (int(self.width), int(self.height))
        
        self.padding = 5
        
        # Create a canvas that can fit the above video source size
        self.canvas = tk.Canvas(
            window, 
            width=self.width*2+self.padding*4,
            height=self.height+self.padding*2
        )
        self.canvas.pack()
        
        # Button to quit the application
        self.btn_quit = tk.Button(window, text="Quit", command=self.quit)
        self.btn_quit.pack(anchor=tk.SE, padx=5, pady=5)
        
        # Load the pre-trained face detection classifier
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        
        # a phase that keeps track of what point we are in the UI process
        self.phase = SHOW_ADEN_PHASE

        # milliseconds to wait before updating the UI
        self.delay = 15
        
        # self attributes that allow the face morph from the original image to
        # the celebrity image
        self.transition_alpha = 0
        self.transition_beta = 100
            
        # a counter to keep track of time
        self.last_capture = time.perf_counter()
        
        self.update()
        self.window.mainloop()


    def face_recognition(self, frame):
        """takes in a frame and checks to see if a person is in that frame/image
        it returns a boolean value representing on if their is a person in the frame
        and the frame with the bounding box drawn around the face
        """
        curr_frame = deepcopy(frame)
        
        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect the faces in the grayscale frame
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        detected = False
        
        # Check if any faces are detected
        if len(faces) > 0:
            
            largest = -float('inf')
            x_l,y_l,w_l,h_l = 0,0,0,0
        
            # Draw rectangles around the detected face regions
            for (x, y, w, h) in faces:
                size = w*h
                if size > largest:
                    largest = size
                    x_l,y_l,w_l,h_l = x,y,w,h
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
            if time.perf_counter() - self.last_capture > 5:
                self.last_capture = time.perf_counter()
                
                # crop the current frame to be centered around the detected face
                x,y,w,h = x_l,y_l,w_l,h_l
                box = [x, y, x+w, y+h]
                
                # crop the image to the face
                modify = (box[2] - box[0]) // 5
                left = box[0] - modify
                right = box[2] + modify
                half_height = ((right - left) * 1.5) // 2
                vert_center = (box[1] + box[3]) // 2
                top = int(vert_center - half_height)
                bottom = int(vert_center + half_height)

                # check if the face is too close to the edge of the image
                if top < 0:
                    bottom = min(bottom - top, curr_frame.shape[0])
                    top = 0
                if bottom > curr_frame.shape[0]:
                    top = max(bottom - curr_frame.shape[0], 0)
                    bottom = curr_frame.shape[0]
                if left < 0:
                    right = min(right - left, curr_frame.shape[1])
                    left = 0
                if right > curr_frame.shape[1]:
                    left = max(right - curr_frame.shape[1], 0)
                    right = curr_frame.shape[1]

                # crop actual image
                curr_frame = curr_frame[top:bottom, left:right, ::-1]
                
                try:
                    # save the image
                    cv2.imwrite(f'images/curr_img.jpg', curr_frame)
                except Exception as e:
                    print(e, "error saving image with size ", curr_frame.shape)
                    detected = False
                
                detected = True

        return detected, frame


    def get_celebrity_look_alike(self, frame):
        """takes in a frame and uses the SVD algorithm to find the celebrity that
        looks most similar to the individual in this frame
        """
        return frame
        
        
    def update(self):
        
        if self.phase == SHOW_ADEN_PHASE:
            
            # load in the aden_with_tag photo
            self.aden_photo = Image.open("images/aden_with_tag.jpg")
            size = self.aden_photo._size
            dim = min(self.height - self.padding*4, self.width - self.padding*4)
            self.aden_photo = self.aden_photo.resize((int(dim),int(dim)))
            size = (int(dim), int(dim))
            self.aden_tk = ImageTk.PhotoImage(self.aden_photo)
            
            # display it in the centerish of the screen
            aden_left = int(self.width // 2 - size[0] // 2)
            aden_top = int(self.height // 2 - size[1] // 2)
            
            self.canvas.create_image(
                aden_left, aden_top,
                image=self.aden_tk, anchor=tk.NW
            )
            
            # after two seconds move on to the introduction phase
            if time.perf_counter() - self.last_capture > 2:
                self.phase = GET_NAME_PHASE
                self.last_capture = time.perf_counter()


        elif self.phase == GET_NAME_PHASE:
            
            speak("Hello, my name is Aden Tee.")
            
            # keep asking for name until it works
            while True:
                try:
                    reply = mic_input(prompt="What is your name? Please start by saying, My name is")
                    self.name = reply.split()[-1]
                except Exception as e:
                    speak("Try saying that again like this: My name is Aden Tee")
                    continue
                else:
                    break

            # update phase
            self.phase = GET_CELEBRITY_PHASE

            # update the last capture time
            speak("Let me take a look at you. Center your phase in the camera for me")
            self.last_capture = time.perf_counter()


        # after introduction, we do the GET_CELEBRITY_PHASE where it pops
        # up the live feed and finds the celebrity look-alike
        elif self.phase == GET_CELEBRITY_PHASE:

            # Get a frame from the video source
            ret, frame = self.cap.read()
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            if ret:
                # check the frame for a detected face and return whether there
                # is a person and the new_frame with the bounding box drawn
                detected, new_frame = self.face_recognition(frame)
                
                # create an ImageTK photo object from the new_frame
                self.photo = ImageTk.PhotoImage(image = Image.fromarray(new_frame))
                
                # create the live feed image
                self.canvas.create_image(
                    self.padding, self.padding, 
                    image = self.photo, 
                    anchor = tk.NW
                )

                # if a face is detected, then we can move on to the next phase
                if detected:
                    self.phase = SPEAKING_CELEBRITY_PHASE


        elif self.phase == SPEAKING_CELEBRITY_PHASE:
            
            # still display the live feed during the speaking celebrity phase
            # Get a frame from the video source
            ret, frame = self.cap.read()
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            if ret:
                # check the frame for a detected face and return whether or not their
                # is a person and the new_frame with the bounding box drawn
                detected, new_frame = self.face_recognition(frame)
                
                # create an ImageTK photo object from the new_frame
                self.photo = ImageTk.PhotoImage(image = Image.fromarray(new_frame))
                
                # create the live feed image
                self.canvas.create_image(
                    self.padding, self.padding, 
                    image=self.photo,
                    anchor=tk.NW
                )
                
            # load in the current image and resize it
            curr_img = Image.open("images/curr_img.jpg")
            curr_img = curr_img.resize((self.output_width, self.output_height))
            self.image_for_info = deepcopy(np.array(curr_img))
            
            # get the celebrity look alike
            celebrity_img, celebrity_name = get_celebrity(curr_img)
            
            self.celerity_name = celebrity_name[0].replace("_", " ")
            
            celebrity_img = Image.open(celebrity_name[1])
            
            celebrity_tk = ImageTk.PhotoImage(image = celebrity_img)
            self.celebrity_tk = celebrity_tk
                
            speak(
                f"{self.name}, I have analyzed your face, "
                "and I think the celebrity you look most like is " + 
                celebrity_name[0].replace("_", " ")
            )

            # resize the image
            trans_size = (280,418)
            user_img = curr_img.resize(trans_size)
            celebrity_img = celebrity_img.resize(trans_size)

            # convert to numpy array
            user_img = np.array(user_img)
            celebrity_img = np.array(celebrity_img)

            # update the phase
            self.user_img = user_img
            self.celebrity_img = celebrity_img
            self.phase = PHOTO_TRANSITION_PHASE


        elif self.phase == PHOTO_TRANSITION_PHASE:

            # Get a frame from the video source
            transition_img = cv2.addWeighted(
                self.user_img, (100-self.transition_alpha)/100, 
                self.celebrity_img, (self.transition_alpha)/100, 0
            )
            self.transition_alpha += 1

            # update alpha to implement transition
            done = False
            if self.transition_alpha > 100:
                done = True
                self.transition_alpha = 0

            # create the transition image
            if not done:
                self.transition_image = ImageTk.PhotoImage(image = Image.fromarray(transition_img))
                
                    
                # create the celebrity image (for now just ironman)
                self.canvas.create_image(
                    self.width+self.padding*2, self.padding, 
                    image=self.transition_image, anchor=tk.NW
                )
                time.sleep(0.005)

            else:
                self.phase = GETTING_INFO_PHASE


        elif self.phase == GETTING_INFO_PHASE:
            
            speak("I will now analyze your face to predict your gender and age.")

            # get gender and age estimation
            gender, gender_confidence, age, age_confidence = age_gender_detector(self.image_for_info)
            self.gender = gender
            self.gender_confidence = int(gender_confidence * 100)
            self.age = age
            self.age_confidene = int(age_confidence * 100)

            # get mood estimation
            if not jeffs_cpu:
                emotion, emotion_confidence = emotion_detector(self.image_for_info)
                
                self.emotion = emotion
                self.emotion_confidence = emotion_confidence

            # output and update phase
            print(gender, gender_confidence, age, age_confidence)
            self.phase = SPEAKING_INFO_PHASE


        elif self.phase == SPEAKING_INFO_PHASE:
            
            speak("Here is my prediction")
            
            speak(
                f"I am {self.gender_confidence} percent sure that you are {self.gender}"
            )
            
            # remove parentheses in the string
            age_str = self.age[1:-1]
            nums = list(map(int, age_str.split("-")))
            lower_age = nums[0]
            higher_age = nums[1]

            # set age
            self.age = randint(lower_age, higher_age)

            # say estimation and update phase
            speak(
                f"I am {self.age_confidene} percent sure that you are between "
                f"{lower_age} and {higher_age} years old)"
            )
            
            if not jeffs_cpu:
                speak(
                    f"I am {self.emotion_confidence} percent sure that you are {self.emotion}"
                )
            
            self.phase = STORY_PHASE


        elif self.phase == STORY_PHASE:
            
            # keep asking for whether to hear a story until it works
            while True:
                try:
                    reply = mic_input(prompt=(
                        "Would you like to hear a story about you that I came "
                        "up with? Please say 'Yes, I would like to' or "
                        "'No, thank you'."
                    ))
                    reply = reply.split()[0]
                    
                    reply = "".join([c for c in reply.lower() if c.isalpha()])
                    
                    if reply == 'yes' or reply == 'sure' or reply == 'okay':
                        self.yes_story = True
                    elif reply == 'no' or reply == 'nah':
                        self.yes_story = False
                    else:
                        self.yes_story = False
                        
                    
                except Exception as e:
<<<<<<< HEAD
                    speak("Try saying that again in a full sentence that ends with yes or no.")
=======
                    speak("Try saying that again like this: My name is Aden Tee")
                    self.yes_story = False
>>>>>>> d49a359de249c2e62db24d9a36f152a5b1b5242e
                    continue
                else:
                    break
            
            speak("Okay!")
            
            if self.yes_story:

                # generate the story
                prompt = generate_prompt(self.name, self.gender, str(self.age), self.celerity_name)
                story = generate_paragraph(prompt).replace("\"", "'")

                # speak the story
                speak("Here is the story I came up with")
                speak(story)

            # update phase and gui
            self.phase = SOMEONE_ELSE_PHASE
            self.canvas.delete('all')


        elif self.phase == SOMEONE_ELSE_PHASE:

            # say goodbye
            if self.yes_story:
                speak("I hope you liked my story.")
                
            speak(
                f"It was great talking to you {self.name}."
            )

            # say dramatic goodbye
            goodbye = generate_good_bye()
            speak(goodbye)

            # update phase
            speak("I would love to get to know someone else.")
            self.phase = SHOW_ADEN_PHASE
        
        self.window.after(self.delay, self.update)
    
    def quit(self):
        self.cap.release()
        self.window.destroy()

# Create a window and pass it to the Application object
App(tk.Tk(), "Live feed")
