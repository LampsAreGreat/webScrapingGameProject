import requests
from bs4 import BeautifulSoup
from csv import writer
from time import sleep
from random import choice

all_quotes = []
base_url = 'http://quotes.toscrape.com/'
url = '/page/1'

while url:

    res = requests.get(f'{base_url}{url}')
    #print(f'Now Scrapping {base_url}{url}...')
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    quotes = soup.find_all(class_='quote')

    for quote in quotes:
        all_quotes.append({
            'text': quote.find(class_='text').get_text(),
            'author': quote.find(class_='author').get_text(),
            'bio-link': quote.find('a')['href']
        })

    next_button = soup.find(class_='next')
    url = next_button.find('a')['href'] if next_button else None
    # sleep(.5)


quote = choice(all_quotes)
remainingGuesses = 4
print('here is a quote: ')
print(quote['text'])
guess = ''
while guess.lower() != quote['author'].lower() and remainingGuesses > 0:
    guess = input(
        f'Who said this quote? Guesses remaining: {remainingGuesses}\n')
    if guess.lower() == quote['author'].lower():
        print('you got it right! ')
        break
    remainingGuesses -= 1
    if remainingGuesses == 3:
        res = requests.get(f"{base_url}{quote['bio-link']}")
        soup = BeautifulSoup(res.text, 'html.parser')
        birth_date = soup.find(class_='author-born-date').get_text()
        birth_place = soup.find(class_='author-born-location').get_text()
        print(
            f"Here is a hint: The author was born {birth_place} on {birth_date}")
    elif remainingGuesses == 2:
        print(
            f"Here is a hint: The author's first name starts with a {quote['author'][0]}")
    elif remainingGuesses == 1:
        last_initial = quote['author'].split(' ')[1][0]
        print(
            f"Here is a hint: The author's last name starts with a {last_initial}")
    else:
        print(
            f"Sorry you ran out of guesses. The answer was {quote['author']}")
