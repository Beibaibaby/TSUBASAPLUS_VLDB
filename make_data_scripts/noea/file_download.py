import requests
from bs4 import BeautifulSoup

url = "https://www.ncei.noaa.gov/pub/data/uscrn/products/hourly02/2020/"
html = requests.get(url).content
soup = BeautifulSoup(html, "html.parser")

# Find all <a> in your HTML that have a not null 'href'. Keep only 'href'.
links = [a["href"] for a in soup.find_all("a", href=True)]
print(links)



