from flask import Flask, request, jsonify
import random

app = Flask(__name__)

books = [
    "지적 대화를 위한 넓고 얕은 지식",
    "정의란 무엇인가",
    "무소유",
    "사피엔스",
    "코스모스",
    "총, 균, 쇠",
    "방구석 미술관",
    "영어회화 100일의 기적",
    "어린 왕자",
    "거꾸로 읽는 세계사"
]

@app.route("/")
def home():
    return "Book Bot Running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    book = random.choice(books)

    return jsonify({
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": f"📚 오늘의 추천 도서\n\n📖 {book}"
                    }
                }
            ]
        }
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
