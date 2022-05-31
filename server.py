from flask import Flask
import random

app = Flask(__name__)

@app.route('/')
def index():
    # return 'random : <strong>' + str(random.random()) + '</strong>'
    return 'hi'

# app.run(port=5001, debug=True)  # debug 모드로 실행 가능. 실제 서비스 할 때는 사용 X. 편의를 위함.
app.run(debug=True)  # debug 모드로 실행 가능. 실제 서비스 할 때는 사용 X. 편의를 위함.
