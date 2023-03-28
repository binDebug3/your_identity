import cv2
from PIL import Image

from facial_recognition import get_celebrity


def face_recognition(frame):
    """takes in a frame and checks to see if a person is in that frame/image
    it returns a boolean value representing on if their is a person in the frame
    and the frame with the bounding box drawn around the face
    """
    # Convert the frame to grayscale
    try:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    except cv2.error:
        return False, frame, []
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # Detect the faces in the grayscale frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    # Check if any faces are detected
    detected = False
    box = []
    if len(faces) > 0:
        detected = True

        # Draw rectangles around the detected face regions
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            box = [x, y, x+w, y+h]
            break

    return detected, frame, box


def load(dirpath=None, fname=None):
    image = cv2.imread(dirpath + "\\" + fname)

    # find the face in the image
    face_finding = face_recognition(image)
    if image is None:
        print(f"Failed to read image: {fname}")

    dimensions = image.shape

    if face_finding[0]:
        box = face_finding[2]

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
            bottom = min(bottom - top, image.shape[0])
            top = 0
        if bottom > image.shape[0]:
            top = max(bottom - image.shape[0], 0)
            bottom = image.shape[0]
        if left < 0:
            right = min(right - left, image.shape[1])
            left = 0
        if right > image.shape[1]:
            left = max(right - image.shape[1], 0)
            right = image.shape[1]


        # crop actual image
        face = face_finding[1][top:bottom, left:right, ::1]

        # Convert the cv2 image to a pil image and resize it
        pil_image = Image.fromarray(cv2.cvtColor(face, cv2.COLOR_BGR2RGB))
        resized_image = pil_image.resize((dimensions[1], dimensions[0]))

        # save the image
        resized_image.save(dirpath + "\\" + fname[:-4] + "1.jpg")
        print("Saved image: " + fname[:-4] + "1.jpg")
        print("Dimensions: ", resized_image.size)
    else:
        print("Error: No face found in image", fname)


if __name__ == "__main__":
    # check an uploaded photo against celebrity database
    path = r""
    photo = ""
    load(path, photo)

    cropped = photo.split(".")[0] + "1.jpg"
    celebrity_img, celebrity_name = get_celebrity(Image.open(path + "\\" + cropped))
    print([c[0] for c in celebrity_name])