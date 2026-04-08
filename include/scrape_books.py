# include/scrape_books.py

import requests
from bs4 import BeautifulSoup
import csv
import os

def scrape_books():
    base_url = "https://books.toscrape.com/catalogue/"
    url = "https://books.toscrape.com/catalogue/page-1.html"
    all_data = []

    while url:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        books = soup.find_all("article", class_="product_pod")

        for book in books:
            data = {}
            data["rating"] = book.find("p", class_="star-rating")["class"][1]
            data["title"] = book.find("h3").find("a")["title"]
            data["price"] = book.find("p", class_="price_color").text.strip()
            all_data.append(data)

        next_btn = soup.find("li", class_="next")
        url = base_url + next_btn.find("a")["href"] if next_btn else None

    # save to books_project/seeds/ inside Docker
    output_path = "/usr/local/airflow/books_project/seeds/books.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["rating", "title", "price"])
        writer.writeheader()
        writer.writerows(all_data)

    print(f"Done! {len(all_data)} books saved.")

if __name__ == "__main__":
    scrape_books()