from bs4 import BeautifulSoup
import markovify
import requests

intitles = ""

headers = {
    'User-Agent': 'python:reddit-title-generator/v0.1',
    'content-type': 'text'
}

subreddit = input("Generate post title from which subreddit? (Just the name, no /r/) ")
url = requests.get("http://reddit.com/r/" + subreddit, headers=headers)

soup = BeautifulSoup(url.text, 'lxml')
titles = soup('a', {'class': 'title may-blank '})

for title in titles:
    intitles += title.text + '. '

markov = markovify.Text(intitles, state_size=1)

print(markov.make_short_sentence(300, tries=50))
