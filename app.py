from flask import Flask, request, jsonify

app = Flask(__name__)

BOOKS = {
    "소설": [
        {
            "title": "불편한 편의점",
            "author": "김호연"
        },
        {
            "title": "아몬드",
            "author": "손원평"
        },
        {
            "title": "달러구트 꿈 백화점",
            "author": "이미예"
        }
    ],
    "경제": [
        {
            "title": "돈의 심리학",
            "author": "모건 하우절"
        },
        {
            "title": "부의 추월차선",
            "author": "엠제이 드마코"
        },
        {
            "title": "부자 아빠 가난한 아빠",
            "author": "로버트 기요사키"
        }
    ],
    "자기계발": [
        {
            "title": "아주 작은 습관의 힘",
            "author": "제임스 클리어"
        },
        {
            "title": "원씽",
            "author": "게리 켈러"
        },
        {
            "title": "그릿",
            "author": "앤절라 더크워스"
        }
    ]
}

@app.route("/", methods=["GET"])
def home():
    return "카카오 도서 추천 챗봇 서버 실행 중"

@app.route("/book", methods=["POST"])
def recommend_book():

    try:
        body = request.get_json()

        utterance = body.get("userRequest", {}).get("utterance", "")

        message = (
            "📚 추천 가능한 장르\n\n"
            "• 소설\n"
            "• 경제\n"
            "• 자기계발\n\n"
            "예) 소설 추천"
        )

        for genre, books in BOOKS.items():

            if genre in utterance:

                message = f"📚 {genre} 추천 도서\n\n"

                for idx, book in enumerate(books, start=1):
                    message += (
                        f"{idx}. {book['title']}\n"
                        f"   저자 : {book['author']}\n\n"
                    )

                break

        response = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": message
                        }
                    }
                ]
            }
        }

        return jsonify(response)

    except Exception as e:

        return jsonify({
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": f"오류 발생: {str(e)}"
                        }
                    }
                ]
            }
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
