import cv2

from os.path import exists

if exists("D:\AlexWork"):
    jeffs_cpu = True
else:
    jeffs_cpu = False

if not jeffs_cpu:
    from fer import FER


# FACE RECOGNITION -----------------------------------------------------------------------------------------------------

def face_recognition(frame):
    """
    Takes in a frame and checks to see if a person is in that frame/image
    it returns a boolean value representing on if their is a person in the frame
    and the frame with the bounding box drawn around the face
    :param frame: the frame to be analyzed
    :return: frame (cv2 image)
             box (list of ints) the boundary where the face is located
    """

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # Detect the faces in the grayscale frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    # Check if any faces are detected
    if len(faces) > 0:
        # Draw rectangles around the detected face regions
        box = []
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            box = [x, y, x + w, y + h]

    # return the frame with the bounding box drawn around the face
    return frame, [box]



# AGE AND GENDER DETECTION ---------------------------------------------------------------------------------------------

# define the path of the face detection, age detection, and gender detection models
# faceProto = "content/opencv_face_detector.pbtxt"
# faceModel = "content/opencv_face_detector_uint8.pb"
ageProto = "content/age_deploy.prototxt"
ageModel = "content/age_net.caffemodel"
genderProto = "content/gender_deploy.prototxt"
genderModel = "content/gender_net.caffemodel"

# define the list of age buckets and gender that our age detector will predict.
MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
ageList = ['(0-2)', '(3-6)', '(7-12)', '(13-18)', '(19-22)', '(23-27)', '(28-35)', '(36-44)', '(45-57)', '(58-100)']
genderList = ['Male', 'Female']

# Load the face detection, age detection, and gender detection models
ageNet = cv2.dnn.readNet(ageModel, ageProto)
genderNet = cv2.dnn.readNet(genderModel, genderProto)
# faceNet = cv2.dnn.readNet(faceModel, faceProto)

padding = 20


def age_gender_detector(frame):
    """
    Predicts the age and gender of the person in an image
    :param frame: (cv2 image) the image to be processed
    :return:    gender (string): the gender of the person in the image
                gender confidence (float): the confidence of the gender prediction from 0 to 1
                age (string): the age range of the person in the image
                age confidence (float): the confidence of the age prediction from 0 to 1
                emotion (string): the emotion of the person in the image
                emotion confidence (float): the confidence of the emotion prediction from 0 to 1
    """

    # Read frame and get the face
    frameFace, bboxes = face_recognition(frame)

    for bbox in bboxes:
        # crop the face
        face = frame[max(0,bbox[1]-padding):min(bbox[3]+padding,frame.shape[0]-1),max(0,bbox[0]-padding):min(bbox[2]+padding, frame.shape[1]-1)]

        # predict gender
        blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
        genderNet.setInput(blob)
        genderPreds = genderNet.forward()
        gender = genderList[genderPreds[0].argmax()]
        # dont print
        # print("Gender Output : {}".format(genderPreds))
        # print("Gender : {}, conf = {:.3f}".format(gender, genderPreds[0].max()))

        # predict age
        ageNet.setInput(blob)
        agePreds = ageNet.forward()
        age = ageList[agePreds[0].argmax()]
        # don't print
        # print("Age Output : {}".format(agePreds))
        # print("Age : {}, conf = {:.3f}".format(age, agePreds[0].max()))

        # detect emotion
        '''detector = FER(mtcnn=True)
        emotions = detector.detect_emotions(frame)[0]['emotions']
        emotion = max(emotions, key=emotions.get)'''


        # don't display the label or the frame
        # label = "{},{}".format(gender, age)
        # cv2.putText(frameFace, label, (bbox[0], bbox[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2, cv2.LINE_AA)

    # return gender, genderPreds[0].max(), age, agePreds[0].max(), emotion, emotions[emotion]
    return gender, genderPreds[0].max(), age, agePreds[0].max()


# EMOTION DETECTION ---------------------------------------------------------------------------------------------------
def emotion_detector(frame):
    """
    Predicts the emotion of the person in an image
    :param frame: (cv2 image) the image to be processed
    :return:    emotion (string): the emotion of the person in the image
                emotion confidence (float): the confidence of the emotion prediction from 0 to 1
    """
    # detect emotion
    detector = FER(mtcnn=True)
    emotions = detector.detect_emotions(frame)[0]['emotions']

    # return emotion
    return max(emotions, key=emotions.get)

if __name__ == "__main__":
    pass
    # print(age_gender_detector(cv2.imread("images/image1.jpg")))
    # print(emotion_detector(cv2.imread("images/image1.jpg")))
