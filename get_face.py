import cv2 as cv


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
cv.imwrite('captured_image.jpg', frame)