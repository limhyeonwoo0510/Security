import requests
from bs4 import BeautifulSoup

def search_naver_news(query="보안", num_results=5):
    search_url = f"https://search.naver.com/search.naver?where=news&query={query}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(search_url, headers=headers, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    results = []

    news_items = soup.select("ul.list_news > li")[:num_results]
    for item in news_items:
        a_tag = item.select_one("a.news_tit")
        if a_tag:
            title = a_tag.get("title")
            link = a_tag.get("href")
            results.append({"title": title, "link": link})

    return results
