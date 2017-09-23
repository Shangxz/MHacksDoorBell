# Python Dependencies
# ===================
import os
import time

# 3rd Party Dependencies
# ======================
from bs4 import BeautifulSoup

# Selenium
# ========

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException


class WebCrawler(object):

	def __init__(self, headless=True):

		chrome_options = Options()
		if headless: chrome_options.add_argument('--headless')

		# Disable Notifications
		# =====================
		prefs = {"profile.default_content_setting_values.notifications" : 2}
		chrome_options.add_experimental_option("prefs",prefs)

		self.driver = webdriver.Chrome(executable_path=os.path.join(os.getcwd(),'chromeDriver/chromedriver_mac'),chrome_options=chrome_options)
		self.driver.set_window_size(750, 1000)
		self.driver.set_page_load_timeout(10)

	def __del__(self):
		self.driver.close()

	def get(self,url):
		print ('Making request to \'{}\''.format(url))

		try:
			self.driver.get(url)
		except TimeoutException:
			self.driver.execute_script('window.stop();')

		return self.driver.page_source.encode('utf-8')

	def quit(self):
		self.driver.close()



class FacebookAPI(object):
	
	def __init__(self, email, password, headless = False):
		
		self.crawler = WebCrawler(headless)

		# login to FB
		# ===========
		loginURL = 'https://www.facebook.com/'
		self.crawler.get(loginURL)
		inputEmail = self.crawler.driver.find_element_by_xpath('''//*[@id="email"]''')
		inputPass = self.crawler.driver.find_element_by_xpath('''//*[@id="pass"]''')
		inputEmail.send_keys(email)
		inputPass.send_keys(password)
		inputPass.send_keys(Keys.ENTER)

		# loadprofile home, extract friends list url
		profileURL = 'https://www.facebook.com/deci.bell.735'
		profilePage = self.crawler.get(profileURL)

		soup = BeautifulSoup(profilePage, 'html.parser')
		friendsURL = soup.find("a", attrs={"data-tab-key":"friends"})['href']

		#loadfriends page
		friendsPage = self.crawler.get(friendsURL)
		soup = BeautifulSoup(friendsPage, 'html.parser')

		# parse for images
		imageURLs = soup.find_all("img",attrs={"class","_s0 _4ooo _1ve7 _rv img"})
		self.imageURLs = [(i['src'],i['aria-label']) for i in imageURLs]

	def downloadUrls():
		pass

	def uploadToS3():
		pass





			



if __name__ == '__main__':
	email = 'mhacksxgmss@gmail.com'
	password = 'raspberry'
	FacebookAPI(email,password,False)







