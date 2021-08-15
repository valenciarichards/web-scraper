# Web Scraper

This scraper accepts the number of pages and type of articles from the user, scrapes [nature.com](https://www.nature.com/nature/articles) (once), and saves all articles of the selected type to individual text files organized in directories by page number.

Functions from previous stages which can be called by editing the main() function include:

- get_content()
  - Accept a URL and return its content in JSON format.
- get_movie_title_and_description()
  - Accept a URL of a movie on IMDB.com and return its title and description.
- save_page_source_code()
  - Accept a URL, save the source code to a file and return a status message.

This app was built as a JetBrains Academy project, and the repository also contains my code snippets from exercises from JetBrains Academy's Python Developer track in the "Problems" directory.

### External modules used

- BeautifulSoup
- requests


## How to use


### Clone the repository
```
git clone git@github.com:valenciarichards/web-scraper.git
```

### Requirements

To install all necessary modules, navigate to the root directory of the repository and run: 

```
pip install -r requirements.txt
```

### Usage

Navigate to "Web Scraper/task" and run:

```
python scraper.py
```
Then, enter the number of pages and type of articles to scrape when prompted. The articles will be saved as individual ".txt" files organized in directories by page number.


## License

The source code is released under the MIT License.
