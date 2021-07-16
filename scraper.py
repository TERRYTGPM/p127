from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import requests

start_url = "https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"
browser = webdriver.Chrome("chromedriver.exe")

browser.get(start_url)
time.sleep(10)

npd = []
planetdata = []
def scrape():
    headers = ["name", "distance", "mass","radius"]


    for i in range(0, 443):
        soup = BeautifulSoup(browser.page_source, "html.parser")

        for ul_tag in soup.find_all("tr", attrs={"class", "exoplanet"}):
            litags = ul_tag.find_all("th")
            temp_list = []
            for index, litag in enumerate(litags):
                if index == 0:
                    temp_list.append(litag.find_all("a")[0].contents[0])

                else: 
                    try:
                        temp_list.append(litag.contents[0])

                    except:
                        temp_list.append(" ")

            hyperlink_li_tag = litags[0]

            temp_list.append("https://en.wikipedia.org"+hyperlink_li_tag.find_all("a", href=True)[0]["href"])

            planetdata.append(temp_list)


        browser.find_element_by_xpath('//*[@id="mw-content-text"]/div[1]/table/tbody/tr[1]/td[2]/a').click()




def scrapemoredata(hyperlink):

        page = requests.get(hyperlink)

        soup = BeautifulSoup(page.content, "html.parser")

        temp_list = []

        for tr_tag in soup.find_all("tr", attrs={"class: fact_row"}):
            td_tags = tr_tag.find_all("td")

            for td_tag in td_tags:
                try:
                    temp_list.append(td_tag.find_all("div", attrs={"class": "value"})[0].contents[0])

                except:
                    temp_list.append(" ")
            
        npd.append(temp_list)

scrape()

for index, data in enumerate(planetdata):
    scrapemoredata(data[5])

finaldata = []

for index, data in enumerate(planetdata):
    finaldata.append(data + finaldata[index])


with open("final.csv", "w") as f:
    r = csv.writer(f)
    r.writerow(headers)
    r.writerows(finaldata)