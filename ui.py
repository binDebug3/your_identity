import cv2
import tkinter as tk
from PIL import Image, ImageTk
import time
from copy import deepcopy
from facial_recognition import get_celebrity

temp_img_path = "./images/iron_man.jpeg"

HEIGHT = 209
WIDTH = 140

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
        self.output_width = WIDTH
        self.output_height = HEIGHT
        self.size = (int(self.width), int(self.height))
        
        self.padding = 5
        
        # Create a canvas that can fit the above video source size
        self.canvas = tk.Canvas(
            window, 
            width = self.width*2+self.padding*4, 
            height = self.height+self.padding*2
        )
        self.canvas.pack()
        
        # Button to quit the application
        self.btn_quit = tk.Button(window, text="Quit", command=self.quit)
        self.btn_quit.pack(anchor=tk.SE, padx=5, pady=5)
        
        # get the celebrity photo
        '''self.celebrity = Image.open(temp_img_path)
        self.celebrity = self.celebrity.resize(self.size)
        self.celebrity_tk = ImageTk.PhotoImage(self.celebrity)'''
        
        # Load the pre-trained face detection classifier
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        
        
        self.delay = 15 # milliseconds
        with open("counter.txt") as file:
            self.counter = int(file.read())
        
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
                
                # crop the current frame to be centered around the detected
                # face
                x,y,w,h = x_l,y_l,w_l,h_l
                
                cx = x + w//2
                cy = y + h//2
                
                start_x = int(cx - self.output_width)
                start_y = int(cy - self.output_height)
                end_x = int(start_x + self.output_width*2)
                end_y = int(start_y + self.output_height*2)
                
                curr_frame = curr_frame[start_y:end_y, start_x:end_x, ::-1]
                
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
                image = self.photo, 
                anchor = tk.NW
            )
            
            if detected:
                
                # load in the current image and resize it
                curr_img = Image.open("images/curr_img.jpg")
                curr_img = curr_img.resize((self.output_width, self.output_height))
                
                # get the celebrity look alike
                celebrity_img, celebrity_name = get_celebrity(curr_img)
                
                celebrity_img = Image.open(celebrity_name[1])
                
                celebrity_tk = ImageTk.PhotoImage(image = celebrity_img)
                self.celebrity_tk = celebrity_tk
                
                celebrity_img = self.celebrity_tk
                celebrity_name = "iron man"
                
                print("creating image")
                
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
