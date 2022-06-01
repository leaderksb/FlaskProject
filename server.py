from flask import Flask, render_template, request
import logging
import mongoDB

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

    return render_template('index.html', linkDataHtml=links)

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

@app.route('/login/', methods=['GET','POST'])
def login():
    print('/login/')

    if request.method == 'POST':
        loginIdReceive = request.form.get('loginIdGive')  # 아이디
        loginPwReceive = request.form.get('loginPwGive')  # 비밀번호

        print("########################################")

        if loginIdReceive == "" or loginIdReceive.strip() == "":  # loginIdReceive에 문자열이 없거나 입력된 문자열이 처음부터 끝까지 공백일 시
            # loginPwReceive 텍스트 필드에 입력된 문자열이 없으면 팝업창 띄우고 /login/ 페이지로 이동

            print("loginIdReceive == "" or loginIdReceive.strip() == """)
            return """
            <script type="text/javascript"> alert("ID를 입력해 주세요."); document.location.href="/login/";</script>
            """
        elif loginPwReceive == "" or loginPwReceive.strip() == "":  # loginPwReceive에 문자열이 없거나 입력된 문자열이 처음부터 끝까지 공백일 시
            # loginPwReceive 텍스트 필드에 입력된 문자열이 없으면 팝업창 띄우고 /login/ 페이지로 이동

            print("loginPwReceive == "" or loginPwReceive.strip() == ")
            return """
            <script type="text/javascript"> alert("PW를 입력해 주세요."); document.location.href="/login/";</script>
            """
        else:  # loginIdReceive, loginPwReceive 텍스트 필드에 입력된 문자열이 있으면
            print("로그인 시도 : ")
            print(mongoDB.login(loginIdReceive, loginPwReceive))
            if mongoDB.login(loginIdReceive, loginPwReceive) == "resultCustomer":
                # return render_template('customer.html')
                return '/customer/<main>/'
            elif mongoDB.login(loginIdReceive, loginPwReceive) == "resultStaff":
                return '/staff/<main>/'
            elif mongoDB.login(loginIdReceive, loginPwReceive) == "resultManager":
                return '/manager/<main>/'
            elif mongoDB.login(loginIdReceive, loginPwReceive) == "error":
                return '/error/<main>/'

    return render_template('login.html')

@app.route('/signup/', methods=['GET','POST'])
def signup():
    print('/signup/')

    if request.method == 'POST':
        signupNameReceive = request.form.get('signupNameGive')  # 이름
        signupIdReceive = request.form.get('signupIdGive')  # 아이디
        signupPwReceive = request.form.get('signupPwGive')  # 비밀번호
        signupPhoneReceive = request.form.get('signupPhoneGive')  # 전화번호
        signupGenderReceive = request.form.get('signupGenderGive')  # 성별
        signupAgeReceive = request.form.get('signupAgeGive')  # 나이대

        print("########################################")

        if signupIdReceive == "" or signupIdReceive.strip() == "":  # signupIdReceive에 문자열이 없거나 입력된 문자열이 처음부터 끝까지 공백일 시
            # signupIdReceive 텍스트 필드에 입력된 문자열이 없으면 팝업창 띄우고 /signup/ 페이지로 이동
            return """
            <script type="text/javascript"> alert("ID를 입력해 주세요."); document.location.href="/signup/";</script>
            """
        else:  # signupIdReceive 텍스트 필드에 입력된 문자열이 있으면
            print(mongoDB.idChk(signupIdReceive))
            # ID 중복 확인
            if mongoDB.idChk(signupIdReceive) == 1:  # 존재하는 ID라면. 중복된 ID.
                return """
                <script type="text/javascript"> alert("이미 사용 중인 ID입니다."), document.location.href="/signup/"; </script>
                """
            elif mongoDB.idChk(signupIdReceive) == 0:  # 존재하지 않는 ID라면
                print("존재하지 않는 ID라면")
                
                ###############  여기에 나머지 다른 텍스트 필드 값들이 있는지 확인 코드 추가  ###############
                
                mongoDB.signup(signupNameReceive, signupIdReceive, signupPwReceive, signupPhoneReceive, signupGenderReceive, signupAgeReceive)
                return """
                <script type="text/javascript"> alert("회원가입이 완료되었습니다."), document.location.href="/login/"; </script>
                """

        print(signupNameReceive, signupIdReceive, signupPwReceive, signupPhoneReceive, signupGenderReceive, signupAgeReceive)

    return render_template('signup.html')
    # return '/signup/'

@app.route('/manager/<main>/', methods=['GET','POST'])
def manager(main):
    print('/manager/<main>/')
    return '/manager/<main>/'

@app.route('/staff/<main>/', methods=['GET','POST'])
def requester(main):
    print('/staff/<main>/')
    return '/staff/<main>/'

# app.run(port=5001, debug=True)  # debug 모드로 실행 가능. 실제 서비스 할 때는 사용 X. 편의를 위함.
app.run(debug=True)  # debug 모드로 실행 가능. 실제 서비스 할 때는 사용 X. 편의를 위함.
