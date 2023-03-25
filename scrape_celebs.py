import urllib.request
from selenium import webdriver
from selenium.webdriver.common.by import By


class Celebrities(object):
    def __init__(self):
        self.website = "https://www.imdb.com/list/ls058011111/?sort=list_order,asc&mode=grid&page=1&ref_=nmls_vw_grd"
        self.driver = webdriver.Chrome(
            executable_path=r"C:\Users\dalli\PycharmProjects\CarMarket\Casper\chromedriver_win32\chromedriver.exe")

        self.driver.get(self.website)

        self.names = self.findNames()
        self.links = self.findLinks()


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
        for name, link in self.names, self.links:
            path = "celebrities/" + "_".join(name.split()) + ".png"
            urllib.request.urlretrieve(link, path)


if __name__ =="__main__":
    celebs = Celebrities()
    print(celebs.names)
    print(celebs.links)

    celebs.driver.close()