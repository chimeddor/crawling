from serpapi import GoogleSearch
from bs4 import BeautifulSoup as bs
import  requests
from typing import Any


class Crawling:
    BASE_GOOGLE_URL = "https://www.google.com/"
    BASE_NAVER_URL = "https://www.naver.com/"
    HEADERS = {
        'User-Agent': 
                ('Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N)'
                 'AppleWebKit/537.36 (KHTML, like Gecko)'
                 'Chrome/135.0.0.0 Mobile Safari/537.36'
                 )
                }
    API_KEY = "YOUR API KEY"

    #login 필요한 웹 browser인경우 사용
    def login():
        pass

    @classmethod
    def search(cls, keyword: str, lang: str="ko", country: str = "kr") -> list[str]:

        params = {
            "engine": "google_light",
            "q": keyword,
            "hl": lang,
            "google_domain": "google.com",
            #google location 검색 시 어떤 국가 기준으로 결과를 보여준다는 뜻
            "gl": country,
            "api_key": cls.API_KEY,
        }
        try:
            search = GoogleSearch(params)
            results: dict[str, Any] = search.get_dict()
            content = []

            if "organic_results" not in results:
                return []
            
            for result in results.get("organic_results", []):
                link = result.get("link")
                if link:
                    try:
                        page = requests.get(link, headers=cls.HEADERS, timeout=5)
                        soup = bs(page.text, "lxml")
                        paragraphs = soup.find_all("p")
                        #strip으로 텍스트 앞뒤의 공백, 탭 줄바꿈 문자 등을 제거
                        text = ' '.join(text for p in paragraphs if (text := p.get_text(strip=True)))
                        print(link)
                        print(f"page: {page}")
                        print(f"paragraphs: {paragraphs}")
                        print("...")
                    except Exception as e:
                        print(f"[Error] link과 관련 예외 발생: {e}")

        except Exception as e:
            print(f"[Error] 검색 중 예외 발생: {e}")
            return []

if __name__ == "__main__":
    keyword = input("크롤링할 내용 입력: ")
    result = Crawling.search(keyword)
    
# search가 attribute
print(Crawling.search("what is machine learning"))
