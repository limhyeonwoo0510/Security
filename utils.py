import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import requests
from bs4 import BeautifulSoup

def search_naver_news(query="보안", num_results=5):
    search_url = f"https://search.naver.com/search.naver?where=news&query={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(search_url)

    soup = BeautifulSoup(response.text, "html.parser")
    results = []

    news_items = soup.select("a > span.sds-comps-text-type-headline1")[:num_results]
    results = []
    
    for span in news_items:
        title = span.get_text(strip=True)
        link = span.parent.get("href")  # 부모 a 태그의 href
        if title and link:
            results.append({"title": title, "link": link})

    return results

# 그래프 그리기
def draw_bar_chart(df):
    font_path = "NanumGothic-Regular.ttf"  # 경로 맞게 조정
    font_name = font_manager.FontProperties(fname=font_path).get_name()
    plt.rc('font', family=font_name)

    years = df['연도']
    x = range(len(years))
    bar_width = 0.15

    fig, ax = plt.subplots(figsize=(12, 6))

    for i, col in enumerate(df.columns[1:]):
        ax.bar(
            [pos + i * bar_width for pos in x],
            df[col],
            width=bar_width,
            label=col
        )

    ax.set_xticks([pos + bar_width * (len(df.columns[1:]) - 1) / 2 for pos in x])
    ax.set_xticklabels(years)
    ax.set_xlabel("연도")
    ax.set_ylabel("발생 건수")
    ax.set_title("연도별 사이버 범죄 발생 추이")
    ax.legend()
    plt.tight_layout()
    return fig
