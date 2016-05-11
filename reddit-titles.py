from bs4 import BeautifulSoup
import markovify
import sys
import requests

headers = {
    'User-Agent': 'python:reddit-title-generator/v0.1',
    'content-type': 'text'
}


def crawl_url(input_url):
    intitles = ""
    soup = BeautifulSoup(input_url.text, 'lxml')

    # Find all the titles on a single reddit page
    titles = soup('a', {'class': 'title may-blank '})

    # Get each title and make it more like a long paragraph (better for markovify)
    for title in titles:
        intitles += title.text + '. '
    if intitles == '':
        print("Crawl did not seem to work, please try a different subreddit!")
        exit()
    return intitles


def generate_text(text):
    markov = markovify.Text(text, state_size=1)
    generated = markov.make_short_sentence(300, tries=40)
    return generated


if __name__ == "__main__":
    url = ""
    if len(sys.argv) == 1:
        subreddit = ""
        while not subreddit:
            subreddit = input("Generate post title from which subreddit? (Just the name, no /r/):\n")
        url = requests.get("http://reddit.com/r/" + subreddit, headers=headers, timeout=10)
    elif len(sys.argv) > 2:
        print("Please only enter a single argument, the subreddit name!")
        exit()
    else:
        url = requests.get("http://reddit.com/r/" + sys.argv[1], headers=headers, timeout=10)

    print(generate_text(crawl_url(url)))
