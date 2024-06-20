import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import nltk
import streamlit as st
from soynlp.noun import LRNounExtractor_v2

def main():
    st.header('최대 7일 이내의 뉴스 키워드를 찾을 수 있습니다')
    date = st.text_input('키워드를 보고싶은 일자를 입력해주세요. ex)20210324')
    news_url = f'https://news.naver.com/main/ranking/popularDay.nhn?date={date}'

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}
    req = requests.get(news_url, headers=headers)
    soup = BeautifulSoup(req.text, 'html.parser')
    news_titles = soup.select('.rankingnews_box > ul > li > div > a')

    crawled_title = []
    for title in news_titles:
        crawled_title.append(title.text)

    title = "".join(crawled_title)
    filtered_title = title.replace('.', ' ').replace('"', ' ').replace(',', ' ').replace("'", " ").replace('·', ' ').replace('=', ' ').replace('\n', ' ')

    # 명사 추출
    noun_extractor = LRNounExtractor_v2()
    nouns = noun_extractor.train_extract([filtered_title])  # 명사 추출

    new_ko = []
    for word, score in nouns.items():
        if len(word) > 1 and word != '단독' and word != ' ':
            new_ko.append(word)

    ko = nltk.Text(new_ko, name='기사 내 명사')

    data = ko.vocab().most_common(150)
    data = dict(data)

    # font_path = 'C:/Windows/Fonts/HMFMPYUN.ttf'
    wc = WordCloud(background_color="white", width=1000, height=1000, max_words=100, max_font_size=300)
    wc = wc.generate_from_frequencies(data)

    fig = plt.figure()
    plt.title(f'{date} KeyWords')
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(fig)

if __name__ == '__main__':
    main()
