from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import traceback

app = Flask(__name__)

@app.route('/api/crawl', methods=['POST'])
def crawl_naver_news():
    # 네이버 뉴스 검색창에 '도서'를 검색한 결과 URL
    url = 'https://search.naver.com/search.naver?where=news&query=도서'
    
    # 크롤링 차단 방지를 위한 User-Agent 설정
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # 네이버 뉴스 검색 결과의 제목과 링크를 담고 있는 선택자 (.news_tit)
        articles = soup.select('a.news_tit')
        
        if articles:
            result_text = "📚 네이버 최신 도서 뉴스라노!\n\n"
            
            # 카카오톡 말풍선 글자 수 제한이 있으니 깔끔하게 상위 5개만 추출
            for idx, article in enumerate(articles[:5], 1):
                title = article.text.strip()
                link = article['href']
                result_text += f"{idx}. {title}\n🔗 {link}\n\n"
                
            # 맨 마지막 줄바꿈 기호 제거
            result_text = result_text.strip()
        else:
            result_text = "도서 뉴스를 찾지 못했다노. 네이버 구조가 바뀌었을 수 있어!"
            
    except Exception as e:
        print(f"Error occurred: {e}")
        print(traceback.format_exc())
        result_text = "뉴스 크롤링 중 에러가 발생했다노... 서버 로그를 확인해줘!"

    # 카카오톡 챗봇 스킬 응답 JSON 포맷
    response_data = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": result_text
                    }
                }
            ]
        }
    }
    
    return jsonify(response_data)

# 서버가 깨어있는지 확인하거나, cron-job으로 깨울 때 쓰는 기본 페이지
@app.route('/')
def index():
    return "Kakao Chatbot Book News Server is running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
