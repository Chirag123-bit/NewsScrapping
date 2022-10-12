import json
import time
from turtle import title

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

options=webdriver.ChromeOptions() #create object of ChromeOptions 
options.add_argument("--lang=np") #set language to Nepali
PATH = "./chromedriver.exe"

driver = webdriver.Chrome(PATH,options=options) #create object of ChromeDriver
driver.get("https://www.annapurnapost.com") #open the website

# Get search bar
search = driver.find_elements(By.CLASS_NAME, "search-icon")[0] #get the search bar
search.click() #click on the search bar
items = [] #create a list to store the data
last_height = driver.execute_script("return document.body.scrollHeight") #get the height of the page
itemTargetCount = 30 #set the number of items to be scraped





try:
    # Wait for search bar to load
    search_bar = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.XPATH, "(//input[@placeholder='समाचार खोजि गर्नुहोस'])[1]"))
    ) #wait for the search bar to load
    driver.implicitly_wait(2) #wait for 2 seconds
    search_bar.send_keys("नेपाल") #search for the keyword
    search_btn = driver.find_element(By.XPATH, "//div[@class='search-input']//div[@class='search-icon']//*[name()='svg']") #get the search button
    search_btn.click() #click on the search button


    # Wait for search results to load
    driver.implicitly_wait(2)

    search_results = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#searchPage > div > div.row.row-search-news-list"))
    ) #wait for the search results to load

    # Get search results
    while len(items) < itemTargetCount:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") #scroll down the page
        time.sleep(5) #wait for 5 seconds
        new_height = driver.execute_script("return document.body.scrollHeight") #get the height of the page
        if new_height == last_height: #if the height of the page is same as the previous height then break the loop
            break
        last_height = new_height #set the previous height to the current height
        items = driver.find_elements(By.CSS_SELECTOR, "#searchPage > div > div.row.row-search-news-list > div") #get the items
        textElements = [] #create a list to store the text
        for item in items: #loop through the items
            dta = item.text.splitlines() #split the text by line
            title = dta[0] #get the title
            date_published = dta[1] #get the date published
            link = item.find_element(By.TAG_NAME, "a").get_attribute("href") #get the link

            textElements.append({
                "title": title,
                "date_published": date_published,
                "link": link
            }) #append the data to the list

        with open("data.json", "w", encoding='utf-8') as f: #open the file
            json.dump(textElements, f, ensure_ascii=False, indent=4) #dump the data to the file
except:
    driver.quit() #close the driver



finally:
    driver.quit() #close the driver

