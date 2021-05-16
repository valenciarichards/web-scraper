import requests

from bs4 import BeautifulSoup

index = int(input())
link = input()
r = requests.get(link)
soup = BeautifulSoup(r.text, "html.parser")
subtitles = soup.find_all("h2")
print(subtitles[index].text)
