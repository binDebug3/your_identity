import cv2
import time


# Load the pre-trained face detection classifier
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# record the index of the image to be saved
with open("counter.txt") as file:
    counter = int(file.read())

# Create a VideoCapture object to access the camera
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Check if the camera is accessible
if not cap.isOpened():
    print("Unable to access camera")
    exit()

last_capture = time.perf_counter()
# Loop over the frames from the camera
while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect the faces in the grayscale frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    # Check if any faces are detected
    if len(faces) > 0:
        # Take a picture and save it to a file
        if time.perf_counter() - last_capture > 5:
            last_capture = time.perf_counter()
            cv2.imwrite(f'images/image{counter}.jpg', frame)
            counter += 1

        # Draw rectangles around the detected face regions
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the video stream with rectangles drawn around the detected face regions
    cv2.imshow('Face Detection', frame)

    # Check if the user has pressed the 'q' key to exit the loop
    if cv2.waitKey(1) == ord('q'):
        break

# Release the camera resource
cap.release()

# Destroy all windows
cv2.destroyAllWindows()


with open("counter.txt", "w+") as file:
    file.write(str(counter))
