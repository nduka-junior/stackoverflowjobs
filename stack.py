from selenium import webdriver
import requests
import time
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import re
from random import randint
import json
PATH = "PATH-TO-YOUR-CHROME-WEBDRIVER"

# items to scrape enables the python scripts to perform searches in stackoverflow jobs
itemsToScrape = 'python'
json_data=[]

options = Options() # option is used to prevent websites from detecting these scripts as bots
ua = UserAgent()
userAgent = ua.random
options.add_argument(f'user-agent={userAgent}')
driver = webdriver.Chrome(chrome_options=options, executable_path=PATH)


def download_image(imagesrc):
    r = requests.get(imagesrc)

    # check if the image has an extension of jpg,png,gif,or jpeg
    regex = r"\.jpeg|\.png|\.gif|\.jpg"
    imgName = re.search(regex, imagesrc, re.MULTILINE).group()
    randnum=randint(1,10000000000000000000000000)

    # download and store the image
    with open(f'images\{randnum}{imgName}', 'wb') as file:
        file.write(r.content)

def tagsfunc(tag):
    return tag.getText().strip()


driver.get(f"https://stackoverflow.com/jobs?q={itemsToScrape}")



mainloop=True
while mainloop:
    time.sleep(2)
    # get the page source of the current webpage
    pagesource=driver.page_source

    soup=BeautifulSoup(pagesource,'html.parser')

    main_divs=soup.select('.listResults .pl24')
    for main_div in main_divs:
        try:

            logo=main_div.find('img')
            logo=logo.get('src')
            download_image(logo)
            
            job_title=main_div.find('a',attrs={"class": "stretched-link"}).text.strip()
            job_url=main_div.find('a',class_='stretched-link').get('href')
            job_url='https://stackoverflow.com/'+job_url

            company_name=main_div.select('.fc-black-700 span:first-child')[0].text.strip()

            country_name=main_div.select('.fc-black-700 .fc-black-500')[0].text.strip()

            tags=main_div.find_all(class_='no-tag-menu')
            tags=list(map(tagsfunc,tags))

            days=main_div.find('div',class_='fs-caption').text.strip()

            data_scrape={
                'job_title':job_title,
                'job_logo':logo,
                'job_url':job_url,
                'company_name':company_name,
                'country_name':country_name,
                'tags':tags,
                'days_uploaded':days

            }
            json_data.append(data_scrape)
            
            
        except:
            print('nil')

    nextbutton=driver.find_element_by_css_selector('.s-pagination a:last-child')
    if nextbutton.text == 'nextchevron_right':
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        nextbutton.click()
    else:
        mainloop=False
        scrape_data=json.dumps(json_data,indent=5)
        with open('index.json', 'a+') as f:
            f.write(scrape_data)
        print('Done Scrapping')
