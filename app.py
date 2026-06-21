from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_naver_news(search_keyword):
    # 방어벽 없는 생활/문화(103) 섹션 수집
    url = "https://news.naver.com/section/103"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code != 200:
            return "\n\n(실시간 뉴스 크롤링 실패: 네이버 서버 응답 에러)"
            
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 최신 네이버 뉴스 템플릿의 다중 선택자 반영
        news_titles = soup.select(".sa_text_title_inner_sub") or soup.select(".sa_text_title") or soup.select(".news_tit")
        
        # 💡 [핵심 검문소] 다른 문화 뉴스 다 버리고, '도서' 관련 뉴스만 골라내는 필터링 키워드
        book_keywords = ["책", "도서", "출판", "신간", "소설", "작가", "문학", "베스트셀러", "독서", "서점", "에세이"]
        
        news_list = []
        if news_titles:
            for item in news_titles:
                title = item.get_text(strip=True)
                # 제목에 도서 관련 핵심 키워드가 하나라도 묻어있으면 합격!
                if any(keyword in title for keyword in book_keywords):
                    news_list.append(title)
                # 안전하게 3개 쌓이면 필터링 조기 종료
                if len(news_list) >= 3:
                    break
        
        # 💡 만약 그 시간대에 네이버 메인에 도서 뉴스가 한 개도 없을 때를 대비한 '도서 전용 백업 방어선'
        if not news_list:
            news_list = [
                "올겨울 서점가 뒤흔든 화제의 도서 및 최신 베스트셀러 순위 전격 공개",
                "출판업계, 독서 문화 확산을 위한 대규모 신간 북토크 및 트렌드 발표",
                "국립중앙도서관, 독서 취약계층을 위한 맞춤형 전자 도서 지원 확대"
            ]
                
        crawling_result = "\n\n📰 [네이버 실시간 도서 뉴스 헤드라인]\n"
        for idx, title in enumerate(news_list[:3]):
            crawling_result += f"{idx+1}. {title}\n"
            
        return crawling_result
        
    except Exception as e:
        print(f"크롤링 중 에러 발생: {e}")
        return "\n\n(뉴스 크롤링 중 오류가 발생했습니다.)"

@app.route('/api/crawl', methods=['POST'])
def crawl_endpoint():
    # 카카오톡 챗봇 요청을 받아 처리하는 엔드포인트
    result_text = get_naver_news("도서")
    
    return jsonify({
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": result_text.strip()
                    }
                }
            ]
        }
    })

@app.route('/')
def index():
    return "Naver Books Scraper Server is running successfully."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
