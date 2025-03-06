"""import requests
from bs4 import BeautifulSoup

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.google.com/",
})

url = "https://www.tripadvisor.com/Hotel_Review-g187147-d188902-Reviews-Hotel_Lutetia-Paris_Ile_de_France.html"
response = session.get(url)
print(response.status_code)  # Check if it's 200

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    reviews = soup.find_all("q", class_="reviewText")
    for review in reviews[:5]:  
        print(review.text)
else:
    print("Access Denied")
"""
import requests

from bs4 import BeautifulSoup

url = "https://www.tripadvisor.com/Attraction_Review-g187791-d192285-Reviews-Colosseum-Rome_Lazio.html"  # Example URL for Colosseum reviews

def scrape_tripadvisor_reviews(url):

    response = requests.get(url)
    print(response)

    soup = BeautifulSoup(response.content, 'html.parser')



    reviews = []

    for review_container in soup.find_all('div', class_="review-container"):

        reviewer_name = review_container.find('span', class_="username").text.strip()

        rating = review_container.find('span', class_="rating").text.strip()

        review_text = review_container.find('p', class_="review-text").text.strip()

        reviews.append({"reviewer": reviewer_name, "rating": rating, "review": review_text})



    return reviews



# Usage

reviews_data = scrape_tripadvisor_reviews(url)

print(reviews_data)
