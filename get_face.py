import cv2
import time
import numpy as np

# # Load the pre-trained face detection classifier
# face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# # record the index of the image to be saved
# with open("counter.txt") as file:
#     counter = int(file.read())
# # Create a VideoCapture object to access the camera
# cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# # Check if the camera is accessible
# if not cap.isOpened():
#     print("Unable to access camera")
#     exit()
# last_capture = time.perf_counter()
# # Loop over the frames from the camera
# while True:
#     # Read a frame from the camera
#     ret, frame = cap.read()
#     # Convert the frame to grayscale
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     # Detect the faces in the grayscale frame
#     faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
#     # Check if any faces are detected
#     if len(faces) > 0:
#         # Take a picture and save it to a file
#         if time.perf_counter() - last_capture > 5:
#             last_capture = time.perf_counter()
#             cv2.imwrite(f'images/image{counter}.jpg', frame)
#             counter += 1
#         # Draw rectangles around the detected face regions
#         for (x, y, w, h) in faces:
#             cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
#     # Display the video stream with rectangles drawn around the detected face regions
#     cv2.imshow('Face Detection', frame)
#     # Check if the user has pressed the 'q' key to exit the loop
#     if cv2.waitKey(1) == ord('q'):
#         break
# # Release the camera resource
# cap.release()
# # Destroy all windows
# cv2.destroyAllWindows()
# with open("counter.txt", "w+") as file:
#     file.write(str(counter))


def face_recognition(frame):
    """takes in a frame and checks to see if a person is in that frame/image
    it returns a boolean value representing on if their is a person in the frame
    and the frame with the bounding box drawn around the face
    """

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # Detect the faces in the grayscale frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    detected = False

    # Check if any faces are detected
    if len(faces) > 0:

        detected = True

        # Draw rectangles around the detected face regions
        box = []
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            box = [x, y, x + w, y + h]

    return frame, box




# define the path of the face detection, age detection, and gender detection models
# faceProto = "content/opencv_face_detector.pbtxt"
# faceModel = "content/opencv_face_detector_uint8.pb"
ageProto = "content/age_deploy.prototxt"
ageModel = "content/age_net.caffemodel"
genderProto = "content/gender_deploy.prototxt"
genderModel = "content/gender_net.caffemodel"

# define the list of age buckets and gender that our age detector will predict.
MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
genderList = ['Male', 'Female']

# Load the face detection, age detection, and gender detection models
ageNet = cv2.dnn.readNet(ageModel, ageProto)
genderNet = cv2.dnn.readNet(genderModel, genderProto)
# faceNet = cv2.dnn.readNet(faceModel, faceProto)

padding = 20

def age_gender_detector(frame):
    # Read frame
    t = time.time()
    frameFace, bboxes = face_recognition(frame)
    for bbox in bboxes:
        # print(bbox)
        face = frame[max(0,bbox[1]-padding):min(bbox[3]+padding,frame.shape[0]-1),max(0,bbox[0]-padding):min(bbox[2]+padding, frame.shape[1]-1)]

        blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
        genderNet.setInput(blob)
        genderPreds = genderNet.forward()
        gender = genderList[genderPreds[0].argmax()]
        # print("Gender Output : {}".format(genderPreds))
        print("Gender : {}, conf = {:.3f}".format(gender, genderPreds[0].max()))

        ageNet.setInput(blob)
        agePreds = ageNet.forward()
        age = ageList[agePreds[0].argmax()]
        print("Age Output : {}".format(agePreds))
        print("Age : {}, conf = {:.3f}".format(age, agePreds[0].max()))

        label = "{},{}".format(gender, age)
        cv2.putText(frameFace, label, (bbox[0], bbox[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2, cv2.LINE_AA)
    return frameFace

def get_demographics(frame):
    """
    :param frame: the frame to be analyzed
    :return: the emotion of the person in the frame
    """
    emotion = ""
    age = 0
    ethnicity = ""

    # image = cv2.imread(frame)
    image = frame

    # Convert the frame to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # Detect the faces in the grayscale frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    detected = False

    # Check if any faces are detected
    if len(faces) > 0:

        detected = True

        # Draw rectangles around the detected face regions
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Load the gender and age classification models
            gender_model = cv2.dnn.readNetFromCaffe('gender_deploy.prototxt', 'gender_net.caffemodel')
            age_model = cv2.dnn.readNetFromCaffe('age_deploy.prototxt', 'age_net.caffemodel')

            # # Load the ethnicity and emotion classification models
            # ethnicity_model = cv2.dnn.readNet('models/age_gender_models/ethnicity_deploy.prototxt',
            #                                   'models/age_gender_models/ethnicity_net.caffemodel')
            # emotion_model = cv2.dnn.readNetFromTensorflow('models/emotion_models/fer2013_mini_XCEPTION.102-0.66.hdf5.pb')

            # # Define the labels for ethnicity and emotion classification
            # ethnicity_labels = ['White', 'Black', 'Asian', 'Indian', 'Middle Eastern', 'Latino_Hispanic']
            # emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']


            # Extract the face ROI
            face = image[y:y+h, x:x+w]
            # Resize the face ROI to fit the input size of the models
            face = cv2.resize(face, (224, 224))

            # Gender classification
            gender_blob = cv2.dnn.blobFromImage(face, scalefactor=1.0, size=(227, 227),
                                                mean=(78.4263377603, 87.7689143744, 114.895847746), swapRB=False)
            gender_model.setInput(gender_blob)
            gender_preds = gender_model.forward()
            gender = np.argmax(gender_preds)

            # Age classification
            age_blob = cv2.dnn.blobFromImage(face, scalefactor=1.0, size=(227, 227),
                                             mean=(78.4263377603, 87.7689143744, 114.895847746), swapRB=False)
            age_model.setInput(age_blob)
            age_preds = age_model.forward()
            age = int(age_preds[0].dot(np.arange(0, 101).reshape(101, 1)).flatten()[0])

            # # Ethnicity classification
            # ethnicity_blob = cv2.dnn.blobFromImage(face, scalefactor=1.0, size=(227, 227),
            #                                        mean=(78.4263377603, 87.7689143744, 114.895847746), swapRB=False,
            #                                        crop=False)
            # ethnicity_model.setInput(ethnicity_blob)
            # ethnicity_preds = ethnicity_model.forward()
            # ethnicity = ethnicity_labels[np.argmax(ethnicity_preds)]
            #
            # # Emotion classification
            # emotion_blob = cv2.dnn.blobFromImage(face, 1.0 / 255, (64, 64), (0, 0, 0), swapRB=True, crop=False)
            # emotion_model.setInput(emotion_blob)
            # emotion_preds = emotion_model.forward()
            # emotion = emotion_labels[np.argmax(emotion_preds)]

            # Draw the results on the image
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)
            text = f"{gender} {age} {ethnicity} {emotion}"
            cv2.putText(image, text, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            cv2.imshow('Output', image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    return age, gender




print(age_gender_detector(cv2.imread("images/image1.jpg")))
