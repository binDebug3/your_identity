import cv2 as cv

with open("counter.txt") as file:
    counter = int(file.read())

# Create a VideoCapture object to access the camera
camera_port = 0
camera = cv.VideoCapture(camera_port, cv.CAP_DSHOW)

# Check if the camera is accessible
if not camera.isOpened():
    print("Unable to access camera")
    exit()

# Read a frame from the camera
ret, frame = camera.read()

# Release the camera resource
camera.release()

# Save the captured frame to a file
cv.imwrite(f'images/image{counter}.jpg', frame)

counter += 1

with open("counter.txt", "w+") as file:
    file.write(str(counter))