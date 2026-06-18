from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
import random

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():

    url = "https://store.kyobobook.co.kr/bestseller/online/daily"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    books = []

    # 교보문고 제목 추출 (여러 구조 대비)
    for tag in soup.find_all(["a", "span"]):
        text = tag.get_text(strip=True)
        if text and len(text) > 5:
            if "원" not in text:  # 가격 제거용 필터
                books.append(text)

    # 중복 제거
    books = list(set(books))

    if books:
        book = random.choice(books)
        result = f"📚 오늘의 교보문고 추천\n\n📖 {book}"
    else:
        result = "도서 정보를 가져오지 못했습니다."

    return jsonify({
        "version": "2.0",
        "template": {
            "outputs": [{
                "simpleText": {
                    "text": result
                }
            }]
        }
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
