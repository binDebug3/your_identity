import os
import numpy as np
from imageio import imread
from matplotlib import pyplot as plt
from scipy import linalg as la
import cv2


def get_faces(path="./celebrities/"):
    """Traverse the specified directory to obtain one image per subdirectory. 
    Flatten and convert each image to grayscale.

    Parameters:
        path (str): The directory containing the dataset of images.

    Returns:
        ((mn,k) ndarray) An array containing one column vector per
            subdirectory. k is the number of people, and each original
            image is mxn.
    """
    ind_name_map = {}
    
    # Traverse the directory and get one image per subdirectory.
    faces = []
    i = 0
    for (dirpath, dirnames, filenames) in os.walk(path):
        for fname in filenames:
            if fname[-5:]=="1.jpg":       # Only get jpg images.
                # Load the image, convert it to grayscale,
                # and flatten it into a vector.
                img = imread(dirpath+"/"+fname, as_gray=True)
                faces.append(np.ravel(img))

                # Store the name of the person and the path to the image.
                ind_name_map[i] = (fname[:-6], dirpath+"/"+fname)
                assert os.path.exists(ind_name_map[i][1])
                i += 1
                break

    # Put all the face vectors column-wise into a matrix.
    return np.transpose(faces), ind_name_map


def sample_faces(k, path="./celebrities/"):
    """Generate k sample images from the given path.

    Parameters:
        n (int): The number of sample images to obtain. 
        path(str): The directory containing the dataset of images.  
    
    Yields:
        ((mn,) ndarray): An flattend mn-array representing a single
        image. k images are yielded in total.
    """

    files = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        for fname in filenames:
            if fname[-3:]=="jpg":       # Only get jpg images.
                files.append(dirpath+"/"+fname)

    # Get a subset of the image names and yield the images one at a time.
    test_files = np.random.choice(files, k, replace=False)
    for fname in test_files:
        yield np.ravel(imread(fname, as_gray=True))

def show(image, m=209, n=140):
    """Plot the flattened grayscale 'image' of width 'w' and height 'h'.
    
    Parameters:
        image ((mn,) ndarray): A flattened image.
        m (int): The original number of rows in the image.
        n (int): The original number of columns in the image.
    """
    # reshape the image and show it
    image = np.reshape(image, (m, n))
    plt.imshow(image, cmap = "gray")
    
class FacialRec(object):
    """Class for storing a database of face images, with methods for
    matching other faces to the database.
    
    Attributes:
        F ((mn,k) ndarray): The flatten images of the dataset, where
            k is the number of people, and each original image is mxn.
        mu ((mn,) ndarray): The mean of all flatten images.
        Fbar ((mn,k) ndarray): The images shifted by the mean.
        U ((mn,k) ndarray): The U in the compact SVD of Fbar;
            the columns are the eigenfaces.
    """
    # initialize the class with vectors of faces
    def __init__(self, path='./celebrities/'):
        """Initialize the F, mu, Fbar, and U attributes.
        This is the main part of the computation.
        """
        # get F, compute the mean_face and compute Fbar
        self.F, self.ind_name_map = get_faces(path=path)
        self.mu = self.F.mean(axis=1)
        self.Fbar = (self.F.T - self.mu).T
        
        # get the SVD of Fbar and save U
        U, Sigma, Vh = la.svd(self.Fbar, full_matrices=False)
        self.U = U


    def project(self, A, s):
        """Project a face vector onto the subspace spanned by the first s
        eigenfaces, and represent that projection in terms of those eigenfaces.
        
        Parameters:
            A((mn,) or (mn,l) ndarray): The array to be projected. 
            s(int): the number of eigenfaces.
        Returns: 
            ((s,) ndarray): An array of the projected image of s eigenfaces.
        """
        return self.U[:,:s].T @ A


    def find_nearest(self, g, s=38):
        """Find the index j such that the jth column of F is the face that is
        closest to the face image 'g'.
        
        Parameters:
            g ((mn,) ndarray): A flattened face image.
            s (int): the number of eigenfaces to use in the projection.

        Returns:
            (int): the index of the column of F that is the best match to
                   the input face image 'g'.
        """
        # get F_hat
        F_ = self.project(self.Fbar, s)
        
        # get g_bar_hat
        g_ = self.project(g-self.mu, s)
        
        # find argmin ||F_ - g_||_2 and return it
        diff = (F_.T - g_).T
        j = np.argmin(np.linalg.norm(diff, axis=0))

        # return the index of the top three closest faces
        # j = np.argsort(np.linalg.norm(diff, axis=0))[:50]
        return j

    # Problem 6
    def match(self, image, s=38, m=209, n=140):
        """Display an image along with its closest match from the dataset. 
        
        Parameters:
            image ((mn,) ndarray): A flattened face image.
            s (int): The number of eigenfaces to use in the projection.
            m (int): The original number of rows in the image.
            n (int): The original number of columns in the image.
        """

        # find the index of the image that is the nearest
        j = self.find_nearest(image, s=s)
        # name = [self.ind_name_map[i] for i in j]
        # return [self.F[:,i].reshape((m,n)) for i in j], name
        name = self.ind_name_map[j]
        return self.F[:, j].reshape((m, n)), name
        
        # select the match and reshape this and the original
        match = self.F[:,j].reshape((m,n))
        orig = image.reshape((m,n))
        
        # plot the original and the matche
        plt.subplot(1,2,1)
        plt.imshow(orig, cmap="gray")
        plt.title("Original")
        plt.subplot(1,2,2)
        plt.imshow(match, cmap="gray")
        plt.title("Match")
        plt.show()


def benj_is_the_GOAT(path = './test/'):
    # get the face
    face = FacialRec('./test/')
    celeb = FacialRec()

    # get location of closest face
    n = celeb.find_nearest(face.F[:,0])

    # plot the original and the match
    plt.subplot(1,2,1)
    show(face.F[:,0])
    plt.title("Original Image")
    plt.subplot(1,2,2)
    show(celeb.F[:,n])
    plt.title("New Image")
    plt.show()

# benj_is_the_GOAT()
celebrities = FacialRec('./celebrities/')


def get_celebrity(image):
    """takes in an image from the webcam and returns the best celebrity match
    and their name
    """
    # convert the image to grayscale and flatten it
    image = np.array(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    image = np.ravel(image)

    # get the celebrity match
    celebrity_img, celebrity_name = celebrities.match(image)
    print(celebrity_name[0])

    # convert the celebrity image to a PIL image
    return celebrity_img, celebrity_name


if __name__ == "__main__":
    pass

