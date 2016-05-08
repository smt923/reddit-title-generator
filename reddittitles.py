from bs4 import BeautifulSoup
import markovify
import sys
import requests

inputgiven = False
intitles = ""
headers = {
    'User-Agent': 'python:reddit-title-generator/v0.1',
    'content-type': 'text'
}

# Check if the user has given input, if not, prompt them for it
if len(sys.argv) == 1:
    subreddit = input("Generate post title from which subreddit? (Just the name, no /r/): ")
    url = requests.get("http://reddit.com/r/" + subreddit, headers=headers)
elif len(sys.argv) > 2:
    print("Please only enter a single argument, the subreddit name!")
    exit()
else:
    url = requests.get("http://reddit.com/r/" + sys.argv[1], headers=headers)

soup = BeautifulSoup(url.text, 'lxml')

# Find all the titles on a single reddit page
titles = soup('a', {'class': 'title may-blank '})

# Get each title and make it more like a long paragraph (better for markovify)
for title in titles:
    intitles += title.text + '. '

markov = markovify.Text(intitles, state_size=1)

print(markov.make_short_sentence(300, tries=50))
