import os

import urllib.request
from selenium import webdriver
from selenium.webdriver.common.by import By
import cv2
import time
from PIL import Image


class Celebrities(object):
    def __init__(self):
        self.website = "https://www.imdb.com/list/ls058011111/?sort=list_order,asc&mode=grid&page=1"
        self.driver = webdriver.Chrome(
            executable_path=r"C:\Users\dalli\PycharmProjects\CarMarket\Casper\chromedriver_win32\chromedriver.exe")

        self.driver.get(self.website)

        self.names = []
        self.links = []
        self.pageCount = 1


    def scrape(self):
        """
        Scrape the website for celebrity names and links to their images
        :return:
        """
        for i in range(10):
            self.names = self.names + self.findNames()
            self.links = self.links + self.findLinks()
            print("Iteration: " + str(i))
            print(len(self.names))
            print(len(self.links), "\n")
            self.driver.get(self.getNextPage())
        self.driver.close()


    def getNextPage(self):
        """
        Click the next button on the page
        :return:
        """
        nextPage = self.website
        index = -1
        while nextPage[index].isdigit():
            index -= 1
        index += 1

        # find the next page number
        currStart = nextPage[index:]
        newStart = str(int(currStart) + self.pageCount)

        # update website link
        site = nextPage[:len(nextPage) + index] + newStart
        self.website = site
        return site


    def findNames(self):
        """
        Find the names of each celebrity on the page
        :return: names (list): list of names as strings
        """
        names = []
        nameClass = "//div[@class='lister-item-image']/a/img"

        # get a list of name elements and save the text content
        nameElems = self.driver.find_elements(By.XPATH, nameClass)

        for elem in nameElems:
            names.append(elem.get_attribute('alt'))

        return names


    def findLinks(self):
        """
        Find the links to each celebrity's image
        :return: links (list): list of link strings
        """
        links = []
        linkClass = "//div[@class='lister-item-image']/a/img"

        # get a list of name elements and save the text content
        linkElems = self.driver.find_elements(By.XPATH, linkClass)

        for elem in linkElems:
            links.append(elem.get_attribute('src'))

        return links


    def save_images(self):
        """
        Save the images of each celebrity
        :return: None
        """
        for i, name in enumerate(self.names):
            alt = "_".join(name.split())
            path = "celebrities/" + alt
            # dir_path = os.path.dirname(path)

            # Check if the directory exists, if not create it and save the image
            if not os.path.exists(path):
                os.makedirs(path)
                path += "/" + alt + ".jpg"
                urllib.request.urlretrieve(self.links[i], path)

    def save_names(self):
        """
        Save the names of each celebrity
        :return: None
        """
        with open("celebrities/names.txt", "w") as file:
            for name in self.names:
                file.write("_".join(name.split()) + "\n")

# END CLASS

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

    detected = False

    # Check if any faces are detected
    box = []
    if len(faces) > 0:

        detected = True

        # Draw rectangles around the detected face regions
        for (x, y, w, h) in faces:
            # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            box = [x, y, x+w, y+h]
            break

    return detected, frame, box


def get_faces(path="./celebrities"):
    """Traverse the specified directory to obtain one image per subdirectory.
    Parameters:
        path (str): The directory containing the dataset of images.
    Returns:
        ((mn,k) ndarray) An array containing one column vector per
            subdirectory. k is the number of people, and each original
            image is mxn.
    """
    # Traverse the directory and get one image per subdirectory.
    faces = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        for fname in filenames:
            if fname[-3:] == "jpg":  # Only get jpg images.
                # Load the image, convert it to grayscale,
                image = cv2.imread(dirpath + "\\" + fname)

                # find the face in the image
                face_finding = face_recognition(image)
                if image is None:
                    print(f"Failed to read image: {fname}")
                    continue

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
                    resized_image = image.resize(dimensions)

                    # save the image
                    pil_image.save(dirpath + "\\" + fname[:-4] + "1.jpg")
                    print("Saved image: " + fname[:-4] + "1.jpg")
                else:
                    print("Error: No face found in image", fname)
                break




if __name__ == "__main__":
    pass
    get_faces()
    # celebs = Celebrities()
    # celebs.scrape()
    # celebs.save_names()
    # celebs.save_images()

