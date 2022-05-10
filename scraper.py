# Youtube Trending webscraping

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import csv
from datetime import date

YT_TRENDING_URL = 'https://youtube.com/feed/trending'
driver = webdriver.Chrome(ChromeDriverManager().install())

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
    return driver

def get_videos(driver):
    driver.get(YT_TRENDING_URL)
    video_tag = 'ytd-video-renderer'
    videos = driver.find_elements_by_tag_name(video_tag) 
    return videos


print('Creating Driver...')
driver = get_driver()
videos = get_videos(driver)

print(f'-----Found {len(videos)} videos-----')


    

def write_to_file(videos):
    video = videos
    title_tag = video.find_element(By.ID, 'video-title')
    title = title_tag.text
    
    url = title_tag.get_attribute('href')
    
    thumbnail_tag = video.find_element(By.TAG_NAME, 'img')
    thumbnail_url = thumbnail_tag.get_attribute('src')
    
    channel_div = video.find_element(By.CLASS_NAME, 'ytd-channel-name')
    channel_name = channel_div.text

    description = video.find_element(By.ID, 'description-text').text

    return title, url, thumbnail_url, channel_name, description


# open the file in the write mode
today = date.today()
today = str(today).replace('-','_')

f = open(f'./youtube_trending_{today}', 'w',encoding="utf-8")

# create the csv writer
writer = csv.writer(f)
row = ['Title', 'URL', 'Thumbnail', 'Channel', 'Description']
writer.writerow(row)
for i in range(len(videos)):
    writer.writerow([write_to_file(videos[i])])
# close the file
f.close()
