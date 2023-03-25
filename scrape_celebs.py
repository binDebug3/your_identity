import os

import urllib.request
from selenium import webdriver
from selenium.webdriver.common.by import By


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


if __name__ == "__main__":
    pass
    # celebs = Celebrities()
    # celebs.scrape()
    # celebs.save_names()
    # celebs.save_images()

