# import dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import time
import pandas as pd

from selenium import webdriver

GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google-chrome'
CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.binary_location = GOOGLE_CHROME_PATH

# def init_browser():
#     # executable_path = {"executable_path": "chromedriver.exe"}
#     # return Browser("chrome", **executable_path, headless=False)
#     browser = webdriver.Chrome(execution_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
#     return browser


def scrape():
    # browser = init_browser()
    browser = webdriver.Chrome(execution_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)

    # visit NASA's Mars Exploration Program news site
    url_news = 'https://mars.nasa.gov/news'
    browser.visit(url_news)

    time.sleep(2)

    # scrape page
    html_news = browser.html
    soup_news = bs(html_news, 'html.parser')

    time.sleep(2)

    # find latest news title and paragraph text
    news_title = soup_news.find_all('div', class_='content_title')[0].text
    news_p = soup_news.find_all('div', class_='article_teaser_body')[0].text



    # visit JPL Featured Space Image page
    url_image = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_image)

    time.sleep(2)

    # navigate to full image version of featured image
    browser.click_link_by_id('full_image')

    time.sleep(3)

    # browser.click_link_by_partial_href('details')
    browser.click_link_by_partial_text('more info')

    time.sleep(2)

    # scrape page
    html_image = browser.html
    soup_image = bs(html_image, 'html.parser')

    # find featured image source url
    partial_image_url = soup_image.find_all('div', class_='download_tiff')[1].find('a')['href']
    featured_image_url = 'https:' + partial_image_url



    # visit Mars Weather twitter page
    url_weather = 'https://twitter.com/marswxreport'
    browser.visit(url_weather)

    time.sleep(2)

    # scrape page
    html_weather = browser.html
    soup_weather = bs(html_weather, 'html.parser')

    # find latest weather report
    tweets = soup_weather.find_all('p', class_='tweet-text')

    tweets_list = []

    for tweet in tweets:
        if tweet.text.split()[0] == 'InSight':
            if tweet.find('a'):
                pic_url = tweet.find('a').text
                full_string = tweet.text
                tweet_string = full_string.replace(pic_url, '')
                tweets_list.append(tweet_string)
            else:
                tweets_list.append(tweet.text)

    try:
        mars_weather = tweets_list[0].replace('\n', ', ')
        mars_weather = mars_weather.replace('InSight s', 'S')
        mars_weather = mars_weather.replace(') low', '), low')
        mars_weather = mars_weather.replace(') high', '), high')
    except:
        pass



    # url for Mars Facts page
    url_facts = 'https://space-facts.com/mars/'
    
    # create dataframe containing facts
    tables = pd.read_html(url_facts)

    mars_facts = tables[0]
    mars_facts.columns = ['Description','Value']
    mars_facts = mars_facts.set_index('Description')

    mars_facts_html = mars_facts.to_html()
    


    # visit USGS Astrogeology page
    url_hemisphere = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_hemisphere)

    time.sleep(2)
    # scrape page
    html_hemisphere = browser.html
    soup_hemisphere = bs(html_hemisphere, 'html.parser')

    # find image titles and urls
    hemispheres = soup_hemisphere.find_all('div', class_='description')

    hemisphere_image_urls = []

    hemispheres

    for hemisphere in hemispheres:
        
        hemisphere_dict = {}
        
        title = hemisphere.find('a').text
        print(title)
        
        url = 'https://astrogeology.usgs.gov' + hemisphere.find('a')['href']
        browser.visit(url)
        time.sleep(2)

        html = browser.html
        soup = bs(html, 'html.parser')
        full_image = soup.find('img',class_='wide-image')['src']
        image_url = 'https://astrogeology.usgs.gov' + full_image
        print(f'{image_url}\n')
        
        hemisphere_dict['title'] = title
        hemisphere_dict['image_url'] = image_url
        
        hemisphere_image_urls.append(hemisphere_dict)
        
        browser.back()
        time.sleep(2)



    # store scraped data in a dictionary
    scraped_data = {
        'latest_news': [news_title,news_p],
        'featured_image_url': featured_image_url,
        'mars_weather': mars_weather,
        'mars_facts': mars_facts_html,
        'hemisphere_image_urls': hemisphere_image_urls
    }


    # quit browser after scraping
    browser.quit()

    # return results
    return scraped_data
