#-*- coding: utf-8 -*-

from flask import Flask, render_template, request
import pandas as pd
import matplotlib
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
# import matplotlib.pylab as plt  사용 지양
import hashlib  # 단방향 해시 암호화
import random
# import mongoDB
import mariaDB

font_location = './static/fonts/NanumGothic.ttf' # For Windows
font_name = fm.FontProperties(fname=font_location).get_name()
matplotlib.rc('font', family=font_name)

app = Flask(__name__)

links = {
    '로그인 페이지':'/login/',
    '회원가입 페이지':'/signup/',
    '관리자 페이지':'/manager/product/inquiry/',
    '직원 페이지':'/staff/product/order/',
    '고객 페이지':'/customer/product/order/'
}

# print(type(links))

@app.route('/')  # 개발용 페이지
def index():
    return render_template('index.html', linkDataHtml=links)

@app.route('/login/', methods=['GET','POST'])  # 로그인
def login():
    print('/login/')
    loginGenderReceive = ''

    if request.method == 'POST':
        loginIdReceive = request.form.get('loginIdGive')  # 아이디
        loginPwReceive = request.form.get('loginPwGive')  # 비밀번호

        if loginIdReceive.strip() == "":  # loginIdReceive에 문자열이 없거나 입력된 문자열이 처음부터 끝까지 공백일 시
            # loginIdReceive 텍스트 필드에 입력된 문자열이 없으면 팝업창 띄우고 /login/ 페이지로 이동
            return """
            <script type="text/javascript"> alert("ID를 입력해 주세요."); document.location.href="/login/";</script>
            """
        elif loginPwReceive.strip() == "":  # loginPwReceive에 문자열이 없거나 입력된 문자열이 처음부터 끝까지 공백일 시
            # loginPwReceive 텍스트 필드에 입력된 문자열이 없으면 팝업창 띄우고 /login/ 페이지로 이동
            return """
            <script type="text/javascript"> alert("PW를 입력해 주세요."); document.location.href="/login/";</script>
            """
        else:  # loginIdReceive, loginPwReceive 텍스트 필드에 입력된 문자열이 있으면
            # loginGenderReceive = mariaDB.genderSelect(loginIdReceive, loginPwReceive)
            salt = mariaDB.saltSelect(loginIdReceive)
            print("salt", salt)
            salting = loginPwReceive + str(salt)
            password = hashlib.sha256(salting.encode()).hexdigest()
            print("password", password)

            # if mongoDB.login(loginIdReceive, loginPwReceive) == "resultCustomer":
            if mariaDB.login(loginIdReceive, password) == "resultCustomer":
                return """
                <script type="text/javascript"> alert(" """ + loginIdReceive + """ 고객님 로그인 되었습니다."); document.location.href="/customer/product/order/";</script>
                """
            # elif mongoDB.login(loginIdReceive, loginPwReceive) == "resultStaff":
            elif mariaDB.login(loginIdReceive, password) == "resultStaff":
                return """
                <script type="text/javascript"> alert(" """ + loginIdReceive + """님 직원 로그인 되었습니다."); document.location.href="/staff/product/order/";</script>
                """
            # elif mongoDB.login(loginIdReceive, loginPwReceive) == "resultManager":
            elif mariaDB.login(loginIdReceive, password) == "resultManager":
                return """
                <script type="text/javascript"> alert(" """ + loginIdReceive + """님 관리자 로그인 되었습니다."); document.location.href="/manager/product/inquiry/";</script>
                """
            elif mariaDB.login(loginIdReceive, password) == "resultNone":
                return """
                <script type="text/javascript"> alert("ID 또는 PW가 존재하지 않습니다. 회원가입해 주세요."); document.location.href="/signup/";</script>
                """

    return render_template('login.html')

@app.route('/signup/', methods=['GET','POST'])  # 회원가입
def signup():
    print('/signup/')

    if request.method == 'POST':  # name 속성으로 전달 받음
        signupNameReceive = request.form.get('signupNameGive')  # 이름
        signupIdReceive = request.form.get('signupIdGive')  # 아이디
        signupPwReceive = request.form.get('signupPwGive')  # 비밀번호
        signupPwCfReceive = request.form.get('signupPwCfGive')  # 비밀번호
        signupPhoneReceive = request.form.get('signupPhoneGive')  # 전화번호
        signupGenderReceive = request.form.get('signupGenderGive')  # 성별
        signupAgeReceive = request.form.get('signupAgeGive')  # 나이대

        salt = random.randint(0, 100000000)  # 0~100000000 사이의 랜덤한 정수

        salting = signupPwReceive + str(salt)

        password = hashlib.sha256(salting.encode()).hexdigest()

        print("########################################")
        print(signupNameReceive, signupIdReceive, password, salt, signupPhoneReceive, signupGenderReceive, signupAgeReceive)
        print("########################################")

        if signupNameReceive.strip() == "":  # signupNameReceive에 문자열이 없거나 입력된 문자열이 처음부터 끝까지 공백일 시
            # signupNameReceive 텍스트 필드에 입력된 문자열이 없으면 팝업창 띄우고 /signup/ 페이지로 이동
            return """
            <script type="text/javascript"> alert("Name을 입력해 주세요."); document.location.href="/signup/";</script>
            """
        elif signupIdReceive.strip() == "":  # signupIdReceive에 문자열이 없거나 입력된 문자열이 처음부터 끝까지 공백일 시
            # signupIdReceive 텍스트 필드에 입력된 문자열이 없으면 팝업창 띄우고 /signup/ 페이지로 이동
            return """
            <script type="text/javascript"> alert("ID를 입력해 주세요."); document.location.href="/signup/";</script>
            """
        elif signupPwReceive.strip() == "":  # signupPwReceive에 문자열이 없거나 입력된 문자열이 처음부터 끝까지 공백일 시
            # signupPwReceive 텍스트 필드에 입력된 문자열이 없으면 팝업창 띄우고 /signup/ 페이지로 이동
            return """
            <script type="text/javascript"> alert("PW를 입력해 주세요."); document.location.href="/signup/";</script>
            """
        # 비밀번호 일치 확인
        elif signupPwReceive != signupPwCfReceive:  # signupPwReceive와 signupPwCfReceive가 같지 않으면
            return """
            <script type="text/javascript"> alert("PW가 일치하지 않습니다."); document.location.href="/signup/";</script>
            """
        elif signupPhoneReceive.strip() == "":  # signupPhoneReceive에 문자열이 없거나 입력된 문자열이 처음부터 끝까지 공백일 시
            # signupPhoneReceive 텍스트 필드에 입력된 문자열이 없으면 팝업창 띄우고 /signup/ 페이지로 이동
            return """
            <script type="text/javascript"> alert("Phone를 입력해 주세요."); document.location.href="/signup/";</script>
            """
        else:  # signupIdReceive 텍스트 필드에 입력된 문자열이 있으면
            # print(mongoDB.idChk(signupIdReceive))
            print(mariaDB.idChk(signupIdReceive))
            # ID 중복 확인
            # if mongoDB.idChk(signupIdReceive) == 1:  # 존재하는 ID라면. 중복된 ID.
            if mariaDB.idChk(signupIdReceive.replace(" ", "")) == 1:  # 존재하는 ID라면. 중복된 ID.
                return """
                <script type="text/javascript"> alert("이미 사용 중인 ID입니다."), document.location.href="/signup/"; </script>
                """
            # elif mongoDB.idChk(signupIdReceive) == 0:  # 존재하지 않는 ID라면
            elif mariaDB.idChk(signupIdReceive.replace(" ", "")) == 0:  # 존재하지 않는 ID라면
                print("존재하지 않는 ID라면")

                print(signupNameReceive, signupIdReceive.replace(" ", ""), signupPwReceive.replace(" ", ""), signupPhoneReceive, signupGenderReceive, signupAgeReceive)
                # mongoDB.signupInsert(signupNameReceive, signupIdReceive.replace(" ", ""), signupPwReceive.replace(" ", ""), signupPhoneReceive, signupGenderReceive, signupAgeReceive)
                mariaDB.signUpInsert(signupNameReceive, signupIdReceive.replace(" ", ""), password, str(salt), signupPhoneReceive, signupGenderReceive, signupAgeReceive)
                return """
                <script type="text/javascript"> alert("회원가입이 완료되었습니다."), document.location.href="/login/"; </script>
                """

    return render_template('signup.html')

@app.route('/manager/product/inquiry/', methods=['GET','POST'])  # 제품 조회
def managerProductInquiry():
    print('/manager/product/inquiry/')

    productList = mariaDB.productexpirydateSelect()

    return render_template('managerProductInquiry.html', productDataHtml=productList)

@app.route('/manager/product/register/', methods=['GET','POST'])  # 제품 등록
def managerProductRegister():
    print('/manager/product/register/')

    if request.method == 'POST':  # name 속성으로 전달 받음
        productNameReceive = request.form.get('productNameGive')  # 제품명
        productIdReceive = request.form.get('productIdGive')  # 제품 아이디
        productSerialCodeReceive = request.form.get('productSerialCodeGive')  # 제품 시리얼 코드
        productQuantityReceive = request.form.get('productQuantityGive')  # 수량
        productPriceReceive = request.form.get('productPriceGive')  # 가격
        productRegisterReceive = request.form.get('productRegisterDateGive')  # 등록일자
        productPeriodReceive = request.form.get('productPeriodGive')  # 유통기간
        productExpiryDateReceive = request.form.get('productExpiryDateGive')  # 유통기한

        print("########################################")
        print(productNameReceive, productIdReceive, productSerialCodeReceive, str(productQuantityReceive), productPriceReceive, productRegisterReceive, str(productPeriodReceive), productExpiryDateReceive)
        print("########################################")

        if productNameReceive.strip() == "":  # productNameReceive에 문자열이 없거나 입력된 문자열이 처음부터 끝까지 공백일 시
            # productNameReceive 텍스트 필드에 입력된 문자열이 없으면 팝업창 띄우고 /manager/product/register/ 페이지로 이동
            return """
            <script type="text/javascript"> alert("Product Name을 입력해 주세요."); document.location.href="/manager/product/register/";</script>
            """
        elif productIdReceive.strip() == "":  # productIdReceive에 문자열이 없거나 입력된 문자열이 처음부터 끝까지 공백일 시
            # productIdReceive 텍스트 필드에 입력된 문자열이 없으면 팝업창 띄우고 /manager/product/register/ 페이지로 이동
            return """
            <script type="text/javascript"> alert("Product ID를 입력해 주세요."); document.location.href="/manager/product/register/";</script>
            """
        elif productSerialCodeReceive.strip() == "":  # productSerialCodeReceive에 문자열이 없거나 입력된 문자열이 처음부터 끝까지 공백일 시
            # productSerialCodeReceive 텍스트 필드에 입력된 문자열이 없으면 팝업창 띄우고 /manager/product/register/ 페이지로 이동
            return """
            <script type="text/javascript"> alert("Serial Code를 입력해 주세요."); document.location.href="/manager/product/register/";</script>
            """
        elif str(productQuantityReceive).strip() == "":  # str(productQuantityReceive)에 문자열이 없거나 입력된 문자열이 처음부터 끝까지 공백일 시
            # str(productQuantityReceive) 텍스트 필드에 입력된 문자열이 없으면 팝업창 띄우고 /manager/product/register/ 페이지로 이동
            return """
            <script type="text/javascript"> alert("Quantity를 입력해 주세요."); document.location.href="/manager/product/register/";</script>
            """
        elif str(productPriceReceive).strip() == "":  # str(productPriceReceive)에 문자열이 없거나 입력된 문자열이 처음부터 끝까지 공백일 시
            # str(productPriceReceive) 텍스트 필드에 입력된 문자열이 없으면 팝업창 띄우고 /manager/product/register/ 페이지로 이동
            return """
            <script type="text/javascript"> alert("Price를 입력해 주세요."); document.location.href="/manager/product/register/";</script>
            """
        else:
            mariaDB.productInsert(productNameReceive, productIdReceive.replace(" ", ""), productSerialCodeReceive.replace(" ", ""), productQuantityReceive.replace(" ", ""), productPriceReceive.replace(" ", ""), productPeriodReceive)
            mariaDB.expirydateInsert(productSerialCodeReceive)
            return """
            <script type="text/javascript"> alert(" """ + productNameReceive + """ 제품 등록 되었습니다."); document.location.href="/manager/product/register/";</script>
            """

    return render_template('managerProductRegister.html')

@app.route('/manager/product/sale/inquiry/', methods=['GET','POST'])  # 매출 조회
def managerProductSaleInquiry():
    print('/manager/product/sale/inquiry/')

    if request.method == 'GET':
        saleTypeReceive = request.args.get('type')  # 구매 유형

        print("saleTypeReceive >>", saleTypeReceive)

        contentsCnt = mariaDB.productSaleCnt(saleTypeReceive)
        contentNames = mariaDB.productSaleNameSelect(saleTypeReceive)
        contentsDF = mariaDB.productSaleSelect(saleTypeReceive)
        contentsDF['date'] = pd.to_datetime(contentsDF['date'])  # 데이터프레임 문자열 칼럼 숫자형으로 변환
        contentsDF['sum_quantity'] = pd.to_numeric(contentsDF['sum_quantity'])  # 데이터프레임 문자열 칼럼 숫자형으로 변환

        print()
        print()

        print("contentsCnt *", contentsCnt)
        print("contentNames *", contentNames)
        print("contentsDF['sum_quantity'] *", contentsDF['sum_quantity'])

        print()
        print()

        # color = ['red', 'orange', 'yellow', 'green', 'cyan', 'navy', 'purple']
        # mfColor = ['salmon', 'gold', 'lightyellow', 'lightgreen', 'lightcyan', 'royalblue', 'mediumorchid']

        # aDF = pd.DataFrame({'date':['2022-01-20', '2022-02-20', '2022-03-20', '2022-04-20', '2022-05-20', '2022-06-20'], 'quantity':[1, 0, 1, 0, 1, 0]})

        # plt.figure(linewidth=2.5)
        # duplicationDF = contentsDF.drop_duplicates(['name'], keep='first')  # 데이터프레임의 제품명 중복 제거. 첫번째만 남김.
        # #
        # print("duplicationDF['name'].cnt >>", duplicationDF['name'].count())
        # print()
        # print("duplicationDF >>", duplicationDF)
        # print()
        # duplicationDF.set_index('name')  # name을 인덱스로 지정
        # print()
        # print()
        # for nameCnt in range(0, contentsCnt):
        #     print()
        #     print()
        #     print(contentsDF)
        #     print()
        #     print()
        #     plt.plot(contentsDF['date'], contentsDF['quantity'], label=nameCnt,
        #     # plt.plot(list_x_values, list_y_values,
        #              color=color[nameCnt],
        #              marker='o', markerfacecolor=mfColor[nameCnt],
        #              markersize=10)

        plt.figure()  # 전체 그림 리셋

        for name, size in zip(contentNames, contentsCnt):
            long_df_sub = contentsDF[contentsDF['name'] == name]
            plt.plot(long_df_sub.date, long_df_sub.sum_quantity, marker='*', markersize=5, linewidth=1.5)

        plt.legend(contentNames, fontsize=12, loc='best')
        plt.title('Last 6 months sales to {0}'.format(saleTypeReceive))
        plt.xlabel('Month')
        plt.ylabel('Quantity')

        plt.savefig('./static/images/{0}Plot.png'.format(saleTypeReceive),
                    # facecolor='#D4F4FA',
                    facecolor='#A5EAD7',
                    edgecolor='black',
                    format='png', dpi=120)

    return render_template('managerProductSaleInquiry.html', typeData=saleTypeReceive)

@app.route('/manager/power/confer/', methods=['GET','POST'])  # 권한 부여
def managerPowerConfer():
    print('/manager/power/confer/')

    informationList = mariaDB.informationSelect()

    if request.method == 'POST':  # name 속성으로 전달 받음
        informationPowerReceive = request.form.get('informationPowerGive')  # 권한
        informationIdReceive = request.form.get('informationIdGive')  # 아이디

        if informationIdReceive.strip() == "":  # informationIdReceive에 문자열이 없거나 입력된 문자열이 처음부터 끝까지 공백일 시
            # informationIdReceive 텍스트 필드에 입력된 문자열이 없으면 팝업창 띄우고 /manager/power/confer/ 페이지로 이동
            return """
            <script type="text/javascript"> alert("ID를 입력해 주세요."); document.location.href="/manager/power/confer/";</script>
            """
        else:  # informationIdReceive 텍스트 필드에 입력된 문자열이 있으면
        # ID 존재 여부 확인
            if mariaDB.idChk(informationIdReceive.replace(" ", "")) == 1:  # 존재하는 ID라면. 권한 부여.
                mariaDB.powerUpdate(informationPowerReceive.replace(" ", ""), informationIdReceive.replace(" ", ""))
                return """
                <script type="text/javascript"> alert(" """ + informationIdReceive.replace(" ", "") + """ 님에게 """ + informationPowerReceive.replace(" ", "") + """ 권한을 부여했습니다." ), document.location.href="/manager/power/confer/"; </script>
                """
            elif mariaDB.idChk(informationIdReceive.replace(" ", "")) == 0:  # 존재하지 않는 ID라면
                return """
                <script type="text/javascript"> alert("존재하지 않는 ID입니다."), document.location.href="/manager/power/confer/"; </script>
                """

    return render_template('managerPowerConfer.html', informationDataHtml=informationList)

@app.route('/staff/product/order/', methods=['GET','POST'])  # 제품 발주
def staffProductOrder():
    print('/staff/product/order/')

    productexpirydateList = mariaDB.productexpirydateSelect()

    if request.method == 'POST':  # name 속성으로 전달 받음
        productNameReceive = request.form.get('productNameGive').replace("\t", "")  # 제품명
        productCodeReceive = request.form.get('productCodeGive').replace("\t", "")  # 제품 시리얼 코드
        productQuantityReceive = request.form.get('productQuantityGive').replace("\t", "")  # 수량
        productPriceReceive = request.form.get('productPriceGive').replace("\t", "")  # 가격

        if productNameReceive.strip() == "" or productPriceReceive.strip() == "":  # 제품을 선택하지 않았다면
            return """
            <script type="text/javascript"> alert("제품을 선택하세요."), document.location.href="/customer/product/order/"; </script>
            """
        else:  # 제품을 선택했다면
            mariaDB.productSaleInsert('staff', productNameReceive.strip(), productQuantityReceive.strip(), str(int(productPriceReceive.strip()) * int(productQuantityReceive.strip())))  # <1> 매출 등록
            mariaDB.expirydateDelete(productCodeReceive.strip())  # <2> 판매된 제품 유통기한 정보 삭제
            mariaDB.productSaleDelete(productNameReceive.strip(), productCodeReceive.strip(), productQuantityReceive.strip())  # <3> 판매된 제품 정보 삭제

            return """
            <script type="text/javascript"> alert(" """ + productNameReceive.strip() + """ 제품, """ + productQuantityReceive.strip() + """개를 """ + str(int(productPriceReceive.strip()) * int(productQuantityReceive.strip())) + """₩ 가격에 주문하였습니다."), document.location.href="/staff/product/order/"; </script>
            """

    return render_template('staffProductOrder.html', productexpirydateDataHtml=productexpirydateList)

@app.route('/customer/product/order/', methods=['GET','POST'])  # 제품 주문
def customer():
    print('/customer/product/order/')

    productexpirydateList = mariaDB.productexpirydateSelect()

    if request.method == 'POST':  # name 속성으로 전달 받음
        productNameReceive = request.form.get('productNameGive').replace("\t", "")  # 제품명
        productCodeReceive = request.form.get('productCodeGive').replace("\t", "")  # 제품 시리얼 코드
        productQuantityReceive = request.form.get('productQuantityGive').replace("\t", "")  # 수량
        productPriceReceive = request.form.get('productPriceGive').replace("\t", "")  # 가격

        if productNameReceive.strip() == "" or productPriceReceive.strip() == "":  # 제품을 선택하지 않았다면
            return """
            <script type="text/javascript"> alert("제품을 선택하세요."), document.location.href="/customer/product/order/"; </script>
            """
        elif productQuantityReceive.strip() == "":  # 주문 수량을 기입하지 않았다면
            return """
            <script type="text/javascript"> alert("주문 수량을 입력하세요."), document.location.href="/customer/product/order/"; </script>
            """
        else:  # 제품을 선택하고 주문 수량을 기입했다면
            quantityBefore = mariaDB.quantitySelect(productNameReceive.strip(), productCodeReceive.strip())  # 선택한 제품 수량
            if int(quantityBefore) < int(productQuantityReceive.strip()):  # 현재 product 제품 수량이 모자랄 경우
                quantityIm = str(int(productQuantityReceive.strip()) - int(quantityBefore))  # 주문 불가한 제품 수량
                quantityBuy = str(quantityBefore)  # 주문 가능한 제품 수량

                print("int(quantityBefore) < int(productQuantityReceive.strip()) :", int(quantityBefore) < int(productQuantityReceive.strip()))

                mariaDB.productSaleInsert('customer', productNameReceive.strip(), quantityBefore, str(int(productPriceReceive.strip()) * int(productQuantityReceive.strip())))  # <1> 매출 등록

                print("현재 product 제품 수량이 모자라다면 < ", str(int(productQuantityReceive.strip())-int(quantityBefore)), "개")
                mariaDB.expirydateDelete(productCodeReceive.strip())  # <2> 판매된 제품 유통기한 정보 삭제
                mariaDB.productSaleDelete(productNameReceive.strip(), productCodeReceive.strip(), str(quantityBefore))  # <3> 판매된 제품 정보 삭제
                return """
                <script type="text/javascript"> alert(" """ + productNameReceive.strip() + """ 제품 재고 부족으로 인해 """ + quantityIm + """개 외 """ + quantityBuy + """개를 """ + str(int(productPriceReceive.strip()) * int(productQuantityReceive.strip())) + """₩ 가격에 주문하였습니다."), document.location.href="/customer/product/order/"; </script>
                """
            elif int(quantityBefore) == int(productQuantityReceive.strip()):  # 현재 product 제품 수량과 고객 주문 수량이 같을 경우

                print("int(quantityBefore) == int(productQuantityReceive.strip()) :", int(quantityBefore) == int(productQuantityReceive.strip()))

                mariaDB.productSaleInsert('customer', productNameReceive.strip(), productQuantityReceive.strip(), str(int(productPriceReceive.strip()) * int(productQuantityReceive.strip())))  # <1> 매출 등록

                mariaDB.expirydateDelete(productCodeReceive.strip())  # <2> 판매된 제품 유통기한 정보 삭제
                mariaDB.productSaleDelete(productNameReceive.strip(), productCodeReceive.strip(), productQuantityReceive.strip())  # <3> 판매된 제품 정보 삭제
                return """
                <script type="text/javascript"> alert(" """ + productNameReceive.strip() + """ 제품, """ + quantityBefore + """개를 """ + str(int(productPriceReceive.strip()) * int(productQuantityReceive.strip())) + """₩ 가격에 주문하였습니다."), document.location.href="/customer/product/order/"; </script>
                """
            elif int(quantityBefore) > int(productQuantityReceive.strip()):  # 현재 product 제품 수량이 충분할 경우
                print("int(quantityBefore) > int(productQuantityReceive.strip()) :", int(quantityBefore) > int(productQuantityReceive.strip()))
                mariaDB.productSaleInsert('customer', productNameReceive.strip(), productQuantityReceive.strip(), str(int(productPriceReceive.strip()) * int(productQuantityReceive.strip())))  # <1> 매출 등록
                mariaDB.quantityUpdate(quantityBefore, productQuantityReceive.strip(), productCodeReceive.strip()) # <2> 판매된 제품 수량 업데이트
                mariaDB.productSaleDelete(productNameReceive.strip(), productCodeReceive.strip(), productQuantityReceive.strip())  # <3> 판매된 제품 정보 삭제
                return """
                <script type="text/javascript"> alert(" """ + productNameReceive.strip() + """ 제품, """ + productQuantityReceive.strip() + """개를 """ + str(int(productPriceReceive.strip()) * int(productQuantityReceive.strip())) + """₩ 가격에 주문하였습니다."), document.location.href="/customer/product/order/"; </script>
                """

    return render_template('customerProductOrder.html', productexpirydateDataHtml=productexpirydateList)

# app.run(port=5001, debug=True)  # debug 모드로 실행 가능. 실제 서비스 할 때는 사용 X. 편의를 위함.
app.run(debug=True)  # debug 모드로 실행 가능. 실제 서비스 할 때는 사용 X. 편의를 위함.
