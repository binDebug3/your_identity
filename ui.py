import cv2
import tkinter as tk
from PIL import Image, ImageTk
import time
from copy import deepcopy

temp_img_path = "./images/iron_man.jpeg"

class App:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        
        # Check if the camera is accessible
        if not self.cap.isOpened():
            print("Unable to access camera")
            exit()
            
        # a counter to keep track of time
        self.last_capture = time.perf_counter()
        
        # get the image size that we will be using
        self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.size = (int(self.width), int(self.height))
        
        self.padding = 5
        
        # Create a canvas that can fit the above video source size
        self.canvas = tk.Canvas(
            window, 
            width = self.width*2+self.padding*4, 
            height = self.height+self.padding*2)
        self.canvas.pack()
        
        # Button to quit the application
        self.btn_quit = tk.Button(window, text="Quit", command=self.quit)
        self.btn_quit.pack(anchor=tk.SE, padx=5, pady=5)
        
        # get the celebrity photo
        self.celebrity = Image.open(temp_img_path)
        self.celebrity = self.celebrity.resize(self.size)
        self.celebrity_tk = ImageTk.PhotoImage(self.celebrity)
        
        # Load the pre-trained face detection classifier
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        
        
        self.delay = 15 # milliseconds
        with open("counter.txt") as file:
            self.counter = int(file.read())
        
        self.update()
        
        self.window.mainloop()
        
    def face_recognition(self, frame):
        
        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect the faces in the grayscale frame
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        detected = False
        
        # Check if any faces are detected
        if len(faces) > 0:
            # Take a picture and save it to a file
            if time.perf_counter() - self.last_capture > 5:
                detected = True
                self.last_capture = time.perf_counter()
                cv2.imwrite(f'images/curr_img.jpg', frame)
                self.counter += 1

            # Draw rectangles around the detected face regions
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
        return detected, frame
        
        
    def update(self):
        # Get a frame from the video source
        ret, frame = self.cap.read()
        
        if ret:
            
            detected, new_frame = self.face_recognition(frame)
            
            if detected:
                # create a ImageTK photo object from the new_frame
                self.photo = ImageTk.PhotoImage(image = Image.fromarray(new_frame))
                
                # create the live feed image
                self.canvas.create_image(
                    self.padding, self.padding, 
                    image = self.photo, anchor = tk.NW
                )

                # create the celebrity image (for now just ironman)
                self.canvas.create_image(
                    self.width+self.padding*2, self.padding, 
                    image = self.celebrity_tk, anchor=tk.NW
                )
            
        
        self.window.after(self.delay, self.update)
    
    def quit(self):
        self.cap.release()
        self.window.destroy()

App(tk.Tk(), "Live feed")
