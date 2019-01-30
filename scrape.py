import time
import mysql.connector

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#setting up the connection and browser
#mysql
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="Economictimes"
)

mycursor = mydb.cursor()

#WebDriver
browser = webdriver.Chrome('C:/Users/HP/Downloads/chromedriver')

browser.get("https://economictimes.indiatimes.com/markets/stocks/recos")
time.sleep(1)

elem = browser.find_element_by_tag_name("body")

#scrolling down till required place
no_of_pagedowns = 50

while no_of_pagedowns:
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.2)
    no_of_pagedowns-=1

#scrapping data
heading = browser.find_elements_by_xpath("//div[@class='eachStory']/h3")
subheading = browser.find_elements_by_xpath("//div[@class='eachStory']/p")
'''
id_S = browser.find_elements_by_xpath("//div[@class='eachStory']/h3/a")
id_ = []
for j in id_S:
	id_.append(j.get_attribute("data-orefid"))
'''
times = browser.find_elements_by_xpath("//div[@class='eachStory']/time")
storeTime = []
id_ = []
for j in times:
	storeTime.append(j.get_attribute("data-time"))
	check = j.get_attribute("data-time").replace(',','').replace(' ','').replace('MIST','').replace(':','')
	id_.append(check)

#storing data
for i in range(len(heading)):
    sql = "INSERT INTO articles (id, heading, subheading, button_text, storeTime ) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE id=id"
    val = (id_[i], heading[i].text,subheading[i].text, button, storeTime[i])
    mycursor.execute(sql, val)

    mydb.commit()

    print("records inserted.")