from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import time
import random
from fake_useragent import UserAgent

# Function to get a random User-Agent
def get_headers():
    ua = UserAgent()
    return {
        'User-Agent': ua.random,
        'Accept-Language': 'en-US, en;q=0.5'
    }

def get_title(soup):
    try:
        title = soup.find("span", attrs={"id": 'productTitle'}).text.strip()
    except AttributeError:
        title = ""
    return title

def get_price(soup):
    try:
        price = soup.find("span", attrs={'class': 'a-offscreen'}).text.strip()
    except AttributeError:
        try:
            price = soup.find("span", attrs={'class': 'a-price aok-align-center reinventPricePriceToPayMargin priceToPay'}).text.strip()
        except AttributeError:
            price = ""
    return price

def get_rating(soup):
    try:
        rating = soup.find("i", attrs={'class': 'a-icon a-icon-star a-star-4-5'}).text.strip()
    except AttributeError:
        try:
            rating = soup.find("span", attrs={'class': 'a-icon-alt'}).text.strip()
        except AttributeError:
            rating = ""
    return rating

def get_review_count(soup):
    try:
        review_count = soup.find("span", attrs={'id': 'acrCustomerReviewText'}).text.strip()
    except AttributeError:
        review_count = ""
    return review_count

def get_availability(soup):
    try:
        available = soup.find("div", attrs={'id': 'availability'}).find("span").text.strip()
    except AttributeError:
        available = "Not Available"
    return available

if __name__ == '__main__':
    URL = "https://www.amazon.in/s?k=puma+shoes+for+men&crid=1RQRBQU54KXKU&sprefix=%2Caps%2C227&ref=nb_sb_ss_recent_1_0_recent"
    try:
        webpage = requests.get(URL, headers=get_headers())
        webpage.raise_for_status()  # Check for request errors
    except requests.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    else:
        soup = BeautifulSoup(webpage.content, "html.parser")

        links = soup.find_all("a", attrs={'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
        links_list = [link.get('href') for link in links]

        data = {"title": [], "price": [], "rating": [], "reviews": [], "availability": []}

        for link in links_list:
            time.sleep(random.uniform(1, 3))  # Introduce a random delay between 1 to 3 seconds
            try:
                new_webpage = requests.get("https://www.amazon.in" + link, headers=get_headers())
                new_webpage.raise_for_status()  # Check for request errors
                new_soup = BeautifulSoup(new_webpage.content, "html.parser")

                data['title'].append(get_title(new_soup))
                data['price'].append(get_price(new_soup))
                data['rating'].append(get_rating(new_soup))
                data['reviews'].append(get_review_count(new_soup))
                data['availability'].append(get_availability(new_soup))
            except requests.HTTPError as err:
                print(f"HTTP error occurred: {err}")
            except Exception as err:
                print(f"An error occurred: {err}")

        amazon_df = pd.DataFrame(data)
        amazon_df['title'] = amazon_df['title'].replace('', np.nan, regex=True)

        amazon_df = amazon_df.dropna(subset=['title'])
        amazon_df.to_csv("amazon_data.csv", header=True, index=False)

print(amazon_df)

