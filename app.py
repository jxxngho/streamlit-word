import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os

def get_weather_info():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 브라우저 창을 표시하지 않음
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    # ChromeDriver 경로 설정 (필요에 따라 수정)
    chromedriver_path = "../chromedriver-win64/chromedriver.exe"
    service = Service(chromedriver_path)
    
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        # Google의 날씨 정보 페이지로 이동
        driver.get("https://www.google.com/search?q=weather")
        
        # CSS 선택자를 이용해서 원하는 클래스를 가져온다.
        element = driver.find_element(By.ID, "wob_tm").text
        loc = driver.find_element(By.CSS_SELECTOR, 'span.BBwThe').text
        
        return loc, element
    except Exception as e:
        return None, str(e)
    finally:
        driver.quit()

st.title("Weather Information")

if st.button("Get Weather Info"):
    loc, temperature = get_weather_info()
    if loc and temperature:
        st.write(f'현재 {loc}의 온도는 {temperature}도!')
    else:
        st.write(f'Error: {temperature}')
