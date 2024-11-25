import requests
from bs4 import BeautifulSoup

def scrape_product_prices(search_query: strl):
    url = f"https://www.arukereso.hu/kereses/?st={search_query}"
    response = requests.get(url)
    if response.status_code != 200:
        return []
    
    soup = BeautifulSoup(response.text, "html.parser")
    products = []

    for item in soup.select("div.product-item"):
        name = item.select.one ('.product-title').get_text(strip=True)
        price = item.select.one ('.price').get_text(strip=True).replace("Ft", "").replace(" ", "")
        products.append({"name": name, "price": float(price)})

    return products
