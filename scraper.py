from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import requests

url = "https://exoplanets.nasa.gov/discovery/exoplanet-catalog/"

browser = webdriver.Chrome("/Users/abhi1/Desktop/Python/C-127/venv/chromedriver.exe")

browser.get(url)
time.sleep(10)
headers = ["name","light_years_from_earth","planet_mass","stellar_magnitude","discovery_date","hyperlink","planet_type","planet_redius","orbital_radius","orbital_period","eccentricity"]
planet_data = []
new_planet_data = []

def scrape():
    
    
    for i in range(0,494):
        while True:
            time.sleep(2)
            soup = BeautifulSoup(browser.page_source,"html.parser")
            currentPageNum = int(soup.find_all("input",attrs={"class","page_num"})[0].get("value"))
            if currentPageNum < i:
                browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
            elif currentPageNum > i:
                browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[1]/a').click()
            else :
                break
            for ul_tag in soup.find_all("ul",attrs={"class","exoplanet"}):
                li_tags = ul_tag.find_all("li")
                templist = []
                for index,li_tag in enumerate(li_tags):
                    if index == 0:
                        templist.append(li_tag.find_all("a")[0].contents[0])
                    else:
                        try :
                            templist.append(li_tag.contents[0])
                        except:
                            templist.append("") 
                hyperlink_li_tag = li_tags[0]
                templist.append("https://exoplanets.nasa.gov"+ hyperlink_li_tag.find_all("a",href=True)[0]["href"])

                planet_data.append(templist)
            browser.find_elements_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
            print(f"{i}page done 1")

def scrap_more_data(hyperlink):
    try:
        page = requests.get(hyperlink)
        soup = BeautifulSoup(page.content,"html.parser")
        templist = []
        for tr_tag in soup.find_all("tr",attrs={"class":"fact_row"}):
            td_tags = tr_tag.find_all("td")
            for td_tag in td_tags:
                try :
                    templist.append(td_tag.find_all("div",attrs={"class":"value"})[0].contents[0])
                except:
                    templist.append("")
        new_planet_data.append(templist)
    except:
        time.sleep(1)
        scrap_more_data(hyperlink)

scrape()

for index,data in enumerate(planet_data):
    scrap_more_data(data[5])
    print(f"{index+1} page done 2  ")

final_planet_data = []
for index,data in enumerate(planet_data):
    new_planet_data_element = new_planet_data[index]
    new_planet_data_element = [element.replace("\n","")for element in new_planet_data_element]
    new_planet_data_element = new_planet_data_element[:7]
    final_planet_data.append(data+new_planet_data_element)


    
with open("extended_scrapper.csv","w")as f:
    csvWriter=csv.writer(f)
    csvWriter.writerow(headers)
    csvWriter.writerows(final_planet_data)



