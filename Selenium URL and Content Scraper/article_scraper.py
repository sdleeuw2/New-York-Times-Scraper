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

# Import dataframe
df = pd.read_csv('path/urls_complete.csv')

# Separate columns into arrays
urls = np.array(df.url) 
dates = np.array(df.date) 
overview = np.array(df.text) 

# Create empty dataframe
content_df = pd.DataFrame(np.empty((0, 4), dtype = np.str)) #
content_df = content_df.rename(columns={0: "url", 1: "text", 2: "date", 3: "content"})    

# Loop over urls and combine all info in dataframe
for i in range(0, ):
    # obtain values from arrays
    url = urls[i]
    date = dates[i]
    text = overview[i]
    # open url 
    chrome_options = Options()  
    chrome_options.add_argument("--headless")  
    chrome_options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'  
    browser = webdriver.Chrome(executable_path='path/chromedriver', options=chrome_options) 
    browser.get(url) 
    # collect text 
    content_element = browser.find_element_by_xpath('//*[@id="story"]')
    if content_element:
        content = content_element.text # get the text connected to the element
    else: 
        content = "NA"
    newdata = pd.DataFrame(data = {'url': url, 'text': text, 'date': date, 'content': content}, index=[0]) # bind arrays in df  
    content_df = content_df.append(newdata) # append to already existing df
    content_df.to_csv("nyt-urls-with-content-1992-2018.csv", index=False)

