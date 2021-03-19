import string
import requests
import json
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


def save_articles():
    url = "https://www.nature.com/nature/articles"
    try:
        response = requests.get(url, headers={"Accept-Language": "en-US,en;q=0.5"})
    except ConnectionError:
        print("There was a problem reaching the website.")
        return None
    data = response.content
    soup = BeautifulSoup(data, "html.parser")
    saved_articles = []
    for article in soup.find_all("article"):
        name = str(article.find("a").contents[0])
        # Strip punctuation and replace spaces with underscores
        name = name.translate(name.maketrans(" ", "_", string.punctuation)).replace("'", "")
        href = article.find("a", {"data-track-action": "view article"})["href"].strip()
        if article.find("span", {"data-test": "article.type"}).text.strip().lower() == "news":
            article_response = requests.get("https://www.nature.com" + href,
                                            headers={"Accept-Language": "en-US,en;q=0.5"})
            news_data = article_response.content
            news_soup = BeautifulSoup(news_data, "html.parser")
            body = news_soup.find("div", {"class": "article__body"}).text.strip()
            with open(name + ".txt", "wb") as file:
                file.write(body.encode("UTF-8"))
                saved_articles.append(name)
    print("Saved articles:\n", saved_articles)


# user_url = input("Input the URL: \n")
# print(save_page_source_code(user_url))

save_articles()
