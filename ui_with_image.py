import cv2
import tkinter as tk
from PIL import Image, ImageTk

class App:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        
        self.cap = cv2.VideoCapture(0)
        self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        
        # Create a canvas that can fit the above video source size
        self.canvas = tk.Canvas(window, width = self.width, height = self.height)
        self.canvas.pack(side=tk.LEFT)
        
        # Load and display the image
        self.image = Image.open("images/image1.png")
        self.photo = ImageTk.PhotoImage(self.image)
        self.image_label = tk.Label(window, image=self.photo)
        self.image_label.pack(side=tk.RIGHT)
        
        # Button to quit the application
        self.btn_quit = tk.Button(window, text="Quit", command=self.quit)
        self.btn_quit.pack(anchor=tk.SE, padx=5, pady=5)
        
        self.delay = 15 # milliseconds
        
        self.update()
        
        self.window.mainloop()
        
    def update(self):
        # Get a frame from the video source
        ret, frame = self.cap.read()
        
        if ret:
            self.photo = ImageTk.PhotoImage(image = Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW)
        
        self.window.after(self.delay, self.update)
    
    def quit(self):
        self.cap.release()
        self.window.destroy()

App(tk.Tk(), "Live feed")
