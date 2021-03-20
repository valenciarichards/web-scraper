import string
import requests
import json
import os
import re
from bs4 import BeautifulSoup


def get_quote(url):
    error_message = "Invalid quote resource!"
    response = requests.get(url, headers={"Accept-Language": "en-US,en;q=0.5"})
    if response.status_code != 200:
        return error_message
    try:
        content = json.loads(response.text)["content"]
    except KeyError:
        return error_message
    return content


def get_title_and_description(url):
    content = {}
    error_message = "Invalid movie page!"
    if not url.startswith("https://www.imdb.com/title/"):
        return error_message
    try:
        response = requests.get(url, headers={"Accept-Language": "en-US,en;q=0.5"})
    except ConnectionError:
        return error_message
    if response.status_code != 200:
        return error_message
    soup = BeautifulSoup(response.content, "html.parser")
    content["title"] = soup.find("h1").contents[0].strip()
    content["description"] = soup.find("div", class_="summary_text").contents[0].strip()
    try:
        assert content["title"] != [] and content["description"] != []
    except AssertionError:
        return error_message
    return content


def save_page_source_code(url):
    response = requests.get(url, headers={"Accept-Language": "en-US,en;q=0.5"})
    if response.status_code != 200:
        return "The URL returned " + str(response.status_code) + "!"
    else:
        page_content = response.content
        with open("source.html", "wb") as file:
            file.write(page_content)
        return "Content saved."


def save_articles(n_pages, article_type):
    url = "https://www.nature.com/nature/articles"
    saved_articles = []
    for page in range(1, n_pages + 1):
        try:
            os.mkdir(f"/home/valencia/PycharmProjects/Web Scraper/Web Scraper/task/Page_{page}")
        except FileExistsError:
            pass
        try:
            response = requests.get(url, headers={"Accept-Language": "en-US,en;q=0.5"})
        except ConnectionError as conn_error:
            print(conn_error)
            return None
        data = response.content
        soup = BeautifulSoup(data, "html.parser")
        for article in soup.find_all("article"):
            name = str(article.find("a").contents[0])
            # Strip punctuation and replace spaces with underscores
            name = name.translate(name.maketrans(" ", "_", string.punctuation)).replace("'", "")
            href = article.find("a", {"data-track-action": "view article"})["href"].strip()
            if article.find("span", {"data-test": "article.type"}).text.strip().lower() == article_type:
                article_response = requests.get("https://www.nature.com" + href,
                                                headers={"Accept-Language": "en-US,en;q=0.5"})
                article_data = article_response.content
                article_soup = BeautifulSoup(article_data, "html.parser")
                regex = re.compile(".*body.*")
                body = article_soup.find("div", {"class": regex}).text.strip()
                with open(f"Page_{page}/{name}.txt", "wb") as file:
                    file.write(body.encode("UTF-8"))
                    saved_articles.append(name)
        next_page_link = soup.find("a", class_="c-pagination__link")["href"].strip()
        url = "https://www.nature.com" + next_page_link
    return "Saved articles:\n", saved_articles


try:
    number_of_pages = int(input())
    type_of_article = input().lower().strip()
    save_articles(number_of_pages, type_of_article)
except ValueError as error:
    print(error)
