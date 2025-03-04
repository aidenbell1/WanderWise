import requests
from bs4 import BeautifulSoup

url = "https://www.tripadvisor.com/Hotel_Review-g187147-d188902-Reviews-Hotel_Lutetia-Paris_Ile_de_France.html"
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

reviews = soup.find_all("q", class_="reviewText")
for review in reviews[:5]:  # Print first 5 reviews
    print(review.text)