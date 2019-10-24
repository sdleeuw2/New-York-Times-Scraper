# Selenium libraries
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException 
from selenium.common.exceptions import NoSuchElementException 
from selenium import webdriver 

# Other libraries
import os  
import time 
import datetime 
import pandas as pd 
import numpy as np

start = datetime.datetime.strptime("01-01-1992", "%d-%m-%Y") # start date query
end = datetime.datetime.strptime("01-01-2019", "%d-%m-%Y") # end date query
date_vector = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)] # dates as numeric vector
date_vector_chr = np.array([date_obj.strftime('%Y%m%d') for date_obj in date_vector]) # dates as character vector
df = pd.DataFrame(data = {'date': date_vector, 'date_chr': date_vector_chr}) # df containing both vectors
df["url"] = "https://www.nytimes.com/search?dropmab=false&endDate=" + df.date_chr + "&query=&sections=U.S.%7Cnyt%3A%2F%2Fsection%2Fa34d3d6c-c77f-5931-b951-241b4e28681c&sort=best&startDate=" + df.date_chr + "&types=article"
urls = np.array(df.url) # isolated vector of urls
dates = np.array(df.date_chr) # isolated vector of dates as characters

links = pd.DataFrame(np.empty((0, 3), dtype = np.str))
links = links.rename(columns={0: "url", 1: "text", 2: "date"})

def scroll_page(url):
    #button_element = browser.find_element_by_xpath('//*[@id="site-content"]/div/div[2]/div[2]/div/button')
    try:
        button_element = browser.find_element_by_xpath('//*[@id="site-content"]/div/div[2]/div[2]/div/button')
    except:
        button_element = None
    while button_element: # is present
        button_element.click() # click button
        time.sleep(np.random.uniform(2, 6)) # wait randomized number of seconds
        try:
            button_element = browser.find_element_by_xpath('//*[@id="site-content"]/div/div[2]/div[2]/div/button')
        except:
            button_element = None

def collect(old_dataframe):
    for j in range(0, len(link_element)): # for each element in the vector of link elements
        link = link_element[j] # select one element in vector
        url = link.get_attribute("href") # get the url connected to the element
        link_text = link.text # get the text connected to the element
        if "PRINT EDITION" in link_text: # if text in element contains "PRINT EDITION"
            url_array = np.array(url) # collect urls in array
            text_array = np.array(link_text) # collect text in array 
            newdata = pd.DataFrame(data = {'url': url_array, 'text': text_array}, index=[0]) # bind arrays in df
            newdata["date"] = dates[i] # add new column containing the date
            old_dataframe = old_dataframe.append(newdata) # append to already existing df
    return(old_dataframe) # return the existing df including the new data

print ("Starting Time: " + str(datetime.datetime.now()))
for i in range(0, len(urls)):
    try: 
        chrome_options = Options()  
        chrome_options.add_argument("--headless")  
        chrome_options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'  
        browser = webdriver.Chrome(executable_path='path/chromedriver', options=chrome_options) 
        url = urls[i]
        browser.get(url) 
        try:
            button_element = browser.find_element_by_xpath('//*[@id="site-content"]/div/div[2]/div[2]/div/button')
        except:
            button_element = None
        scroll_page(url)
        link_element = browser.find_elements_by_xpath('//*[@id="site-content"]/div/div[2]/div[1]/ol/li[.]/div/div/a')
        links = collect(links)
        browser.quit()
        links.to_csv("nyt_urls_1991_2018.csv", index=False)
        print(str(i) + " out of " + str(len(urls)), end="\r")
    except:
        pass 
print ("End Time: " + str(datetime.datetime.now()))
os.system("I am done collecting urls")