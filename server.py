from flask import Flask, render_template
import logging
import random

app = Flask(__name__)

links = {
    '로그인 페이지':'/login/',
    '회원가입 페이지':'/signup/',
    '관리자 메인페이지':'/manager/main/',
    '직원 메인페이지':'/staff/main/'
}

print(type(links))
# topics = [
#     {'link':'/login/', 'title':'로그인 페이지', 'body':'로그인 페이지 내용'},
#     {'link':'/signup/', 'title':'회원가입 페이지', 'body':'회원가입 페이지 내용'},
#     {'link':'/manager/main/', 'title':'관리자 메인페이지', 'body':'관리자 메인페이지 내용'},
#     {'link':'/staff/main/', 'title':'직원 메인페이지', 'body':'직원 메인페이지 내용'}
# ]

@app.route('/')
def index():
    # return 'random : <strong>' + str(random.random()) + '</strong>'
    # liTags = ''
    # for topic in topics:
    #     liTags = liTags +f'<li><a href="{topic["link"]}">{topic["title"]}</a></li>'

    return render_template("index.html", linkDataHtml=links)

    # return f'''<!doctype html>
    # <html>
    #      <body>
    #      <h1><a href="/">WEB</a></h1>
    #      <ol>
    #          {liTags}
    #      </ol>
    #      </body>
    # </html>
    # '''

@app.route('/login/')
def login():
    print('/login/')
    return render_template("login.html")
    # return '/login/'

@app.route('/signup/')
def signup():
    print('/signup/')
    return render_template("signup.html")
    # return '/signup/'

@app.route('/manager/<main>/')
def manager(main):
    print('/manager/<main>/')
    return '/manager/<main>/'

@app.route('/staff/<main>/')
def requester(main):
    print('/staff/<main>/')
    return '/staff/<main>/'

# app.run(port=5001, debug=True)  # debug 모드로 실행 가능. 실제 서비스 할 때는 사용 X. 편의를 위함.
app.run(debug=True)  # debug 모드로 실행 가능. 실제 서비스 할 때는 사용 X. 편의를 위함.
