import streamlit as st
import requests
from bs4 import BeautifulSoup
from soynlp.noun import LRNounExtractor_v2
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def fetch_news_titles(keyword, pages=3):
    titles = []
    for page in range(1, pages + 1):
        url = f"https://search.naver.com/search.naver?where=news&query={keyword}&start={page*10-9}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        titles.extend([title.get_text() for title in soup.select('.news_tit')])
    return titles

def extract_nouns_from_titles(titles):
    noun_extractor = LRNounExtractor_v2()
    nouns = noun_extractor.train_extract(titles)
    return [noun for noun, score in nouns.items() if score.score > 0.1]  # 점수 기준을 낮춤

def generate_wordcloud(nouns):
    if not nouns:
        st.write("추출된 명사가 없습니다. 워드 클라우드를 생성할 수 없습니다.")
        return
    text = ' '.join(nouns)
    wordcloud = WordCloud(font_path='/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf', width=800, height=800, background_color='white').generate(text)
    plt.figure(figsize=(8, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.close()
    return plt

def main():
    st.title("네이버 뉴스 키워드 워드 클라우드 생성기")
    keyword = st.text_input("검색할 키워드를 입력하세요:", "오뚜기")
    pages = st.number_input("검색할 페이지 수를 입력하세요:", min_value=1, max_value=10, value=3)
    
    if st.button("워드 클라우드 생성"):
        with st.spinner("뉴스 제목을 가져오는 중..."):
            titles = fetch_news_titles(keyword, pages)
        with st.spinner("명사를 추출하는 중..."):
            nouns = extract_nouns_from_titles(titles)
        with st.spinner("워드 클라우드를 생성하는 중..."):
            fig = generate_wordcloud(nouns)
            if fig:
                st.pyplot(fig)

if __name__ == "__main__":
    main()
