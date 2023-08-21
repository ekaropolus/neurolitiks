from flask import render_template
from gtts import gTTS
import requests
from bs4 import BeautifulSoup
import random
import uuid
from serpapi import GoogleSearch

            # <!--{% import "/main/macros/flo.html" as macros %}-->
            # <!--{{macros.flo()}}-->

def lvc_vg_ctr():
    # Searching for news articles using the SerpApi service
    params = {
        "q": "news",
        "tbm": "nws",
        "num": 100,
        "api_key": "31b48a24bad782b9d1e0ca42d350a00e2b027c8ea39ed2d5b79720d1ea7a508e"
    }
    search = GoogleSearch(params)
    results = search.get_dict().get('news_results')

    # Selecting a random article from the search results
    article = random.choice(results)
    article_title = article.get('title')
    article_body = article.get('snippet')
    article_url = article.get('link')

    # Scraping the article content using requests and BeautifulSoup
    r = requests.get(article_url)
    soup = BeautifulSoup(r.content, 'html.parser')
    article_content = soup.find('div', class_='article-content')
    if article_content is not None:
        article_body = article_content.text

    # Generate a unique filename for the input file
    BASE_PATH = '/home/3karopolus/mysite/ai_services/lite_voice_generation/static/audio/'
    uuid_name = str(uuid.uuid4())
    filename_gen = uuid_name + 'gen.wav'

    # Converting the article text to speech using gTTS
    tts = gTTS(article_title + ' ' + article_body, lang='en')
    tts.save(BASE_PATH +  filename_gen)

    return render_template('lvc_index.html', article_title=article_title, article_body=article_body, audio_file=filename_gen)
