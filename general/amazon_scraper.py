import bs4
import requests

URL = ''

HEADERS = {
    'User-Agent':
    'Mozilla/5.0 (X11; CrOS x86_64 12239.19.0) AppleWebKit/537.36 (KHTML, like\
     Gecko) Chrome/76.0.3809.38 Safari/537.36'
}

WEBPAGE = requests.get(URL, headers=HEADERS)

SOUP = bs4.BeautifulSoup(WEBPAGE.content, 'html.parser')
