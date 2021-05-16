# scraper.py

# Import standard library modules.
import string
import os
import re

# Import external modules.
import requests
import json
from bs4 import BeautifulSoup

# Set headers for requests.get().
headers = {"Accept-Language": "en-US,en;q=0.5"}


# Stage 1
def get_quote(url):
    """Accept a URL and return its content in JSON format."""
    error_message = "Invalid quote resource!"
    # Make the request and verify that the expected response is received.
    try:
        r = requests.get(url, headers=headers)
        content = json.loads(r.text)["content"]
    except ConnectionError or KeyError:
        return error_message
    if r.status_code != 200:
        return error_message
    return content


# Stage 2
def get_movie_title_and_description(url):
    """Accept a URL of a movie on IMDB.com and return its title and description."""
    content = {}
    error_message = "Invalid movie page!"
    # Verify the URL.
    if not url.startswith("https://www.imdb.com/title/"):
        return error_message
    # Make the request and verify that the expected response is received.
    try:
        r = requests.get(url, headers=headers)
    except ConnectionError:
        return error_message
    if r.status_code != 200:
        return error_message
    # Parse the response content.
    soup = BeautifulSoup(r.content, "html.parser")
    content["title"] = soup.find("h1").contents[0].strip()
    content["description"] = soup.find("div", class_="summary_text").contents[0].strip()
    # Verify that there is both a title and a description.
    try:
        assert content["title"] != [] and content["description"] != []
    except AssertionError:
        return error_message
    return content


# Stage 3
def save_page_source_code(url):
    """Accept a URL, save the source code to a file and return a status message."""
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        return "The URL returned " + str(r.status_code) + "!"
    else:
        page_content = r.content
        with open("source.html", "wb") as file:
            file.write(page_content)
        return "Content saved."


# Stages 4 and 5
def get_soup(url, page=None):
    """Accept a URL and optional page number and return a 'soup' of its content."""
    params = {"page": page}
    try:
        r = requests.get(url, headers=headers, params=params)
    except ConnectionError as conn_error:
        print(conn_error)
        return None
    return BeautifulSoup(r.content, "html.parser")


def save_articles(n_pages, desired_article_type):
    """Accept the number of pages and article type, save articles by page number and return a status message."""
    # Assign the default URL.
    url = "https://www.nature.com/nature/articles"
    for page in range(1, n_pages + 1):
        # Create a directory to store articles.
        try:
            os.mkdir(f"/home/valencia/PycharmProjects/Web Scraper/Web Scraper/task/Page_{page}")
        except FileExistsError:
            pass
        # Get soup from page.
        soup = get_soup(url, page)
        if soup:
            # Iterate through each article on the page and, if it's of the desired type, save a copy of its
            # content(body) in the folder for that page.
            for article in soup.find_all("article"):
                # Get article name, then strip punctuation and replace spaces with underscores
                name = str(article.find("a").contents[0])
                name = name.translate(name.maketrans(" ", "_", string.punctuation)).replace("'", "")
                href = article.find("a", {"data-track-action": "view article"})["href"].strip()
                article_type = article.find("span", {"data-test": "article.type"}).text.strip().lower()
                if article_type == desired_article_type:
                    # Get soup from article
                    article_soup = get_soup("https://www.nature.com" + href)
                    if article_soup:
                        # Extract the body of the article and save it as bytes in a .txt file
                        regex = re.compile(".*body.*")
                        body = article_soup.find("div", {"class": regex}).text.strip()
                        with open(f"Page_{page}/{name}.txt", "wb") as file:
                            file.write(body.encode("UTF-8"))
        else:
            return "There was a problem reaching the website."
    return "All articles saved."


try:
    number_of_pages = int(input())
    type_of_article = input().lower().strip()
    print(save_articles(number_of_pages, type_of_article))
except ValueError as error:
    print(error)
