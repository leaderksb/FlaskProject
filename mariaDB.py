import pymysql

def informationSelect():
    # # DB 연동
    # conn = MongoClient('mongodb://localhost:27017/')  # MongoDB IP : 127.0.0.1, PORT : 27017, use information
    # # DB 생성
    # informationDB = conn['information']
    # global idChkDictionary
    # x = informationDB.information.count_documents( {"id":id} )

    conn = pymysql.connect(host='localhost', user='root', passwd='maria', db='intern', charset='utf8')
    try:
        with conn.cursor() as curs:
            curs.execute("select * from information;")
            rs = curs.fetchall()
            print(rs)
    finally:
        conn.close()

informationSelect()


def idChk(id):
    # # DB 연동
    # conn = MongoClient('mongodb://localhost:27017/')  # MongoDB IP : 127.0.0.1, PORT : 27017, use information
    # # DB 생성
    # informationDB = conn['information']
    # global idChkDictionary
    # x = informationDB.information.count_documents( {"id":id} )

    conn = pymysql.connect(host='localhost', user='root', passwd='maria', db='intern', charset='utf8')
    try:
        with conn.cursor() as curs:
            curs.execute("select * from information where id = '" + id + "';")
            x = curs.rowcount  # 조회된 값 개수
    finally:
        conn.close()  # DB 종료

    return x

# print(idChk("kimsubin"))
# print(idChk(""))


# 접속 속도 우선순위 : 1) 고객 2) 직원 3) 관리자
def login(id, pw):
    conn = pymysql.connect(host='localhost', user='root', passwd='maria', db='intern', charset='utf8')
    try:
        with conn.cursor() as curs:
            curs.execute("select * from information where power = 'customer' and id = '" + id + "' and pw='" + pw + "';")
            resultCustomer = curs.rowcount  # 조회된 값 개수
            curs.execute("select * from information where power = 'staff' and id = '" + id + "' and pw='" + pw + "';")
            resultStaff = curs.rowcount  # 조회된 값 개수
            curs.execute("select * from information where power = 'manager' and id = '" + id + "' and pw='" + pw + "';")
            resultManager = curs.rowcount  # 조회된 값 개수

        if resultCustomer == 1:
            return "resultCustomer"
        elif resultStaff == 1:
            return "resultStaff"
        elif resultManager == 1:
            return "resultManager"
        else:
            return "resultNone"
        print("resultCustomer :", resultCustomer, "resultStaff :", resultStaff, "resultManager :", resultManager)
    except Exception as e:
        print("Error :", e)
        return e
    finally:
        conn.close()  # DB 종료

# login("kimsubin", "kimsubin")


# 회원정보 삽입
def signUpInsert(name, id, pw, phone, gender, age):
    conn = pymysql.connect(host='localhost', user='root', passwd='maria', db='intern', charset='utf8')
    try:
        with conn.cursor() as curs:
            curs.execute("insert into information values ('customer', '" + name + "', '" + id + "', '" + pw + "', '" + phone
                         + "', '" + gender  + "', '" + age + "');")  # 기본 권한 customer
        conn.commit()
    finally:
        conn.close()


print("########################################")
# 상품 등록
def productInsert(name, id, code, quantity, price, period):
    conn = pymysql.connect(host='localhost', user='root', passwd='maria', db='intern', charset='utf8')
    try:
        with conn.cursor() as curs:
            # 제품명, 제품 ID, 제품 시리얼 코드, 수량, 가격, 등록일자 : now(), 유통기간
            curs.execute("insert into product values ('" + name + "', '" + id + "', '" + code + "', " + quantity + ", '" + price + "', now(), " + period + " );", (quantity, period))
            # TypeError: can only concatenate str (not "int") to str 문자열로 삽입
        conn.commit()
    finally:
        conn.close()

productInsert('name', 'id', 'code', 22, '1500', 88)
print("########################################")


# 문제 검색
def questionSelect():
    global qno, quiz, answer  # 전역변수 사용
    conn = pymysql.connect(host='localhost', user='root', passwd='11386013', db='tcpip', charset='utf8')
    try:
        with conn.cursor() as curs:
            curs.execute("select * from question order by rand() limit 1;")
            rs = curs.fetchall()
            qno = rs[0][0]  # 문제 번호
            quiz = rs[0][1]  # 문제 내용
            answer = rs[0][2]  # 정답

    finally:
        conn.close()


# 순위 검색
def rankSelect():
    global rank  # 전역변수 리스트 사용
    conn = pymysql.connect(host='localhost', user='root', passwd='11386013', db='tcpip', charset='utf8')
    try:
        with conn.cursor() as curs:
            # 문자열 타입 숫자의 내림차순
            curs.execute("select * from score order by score * 1 desc limit 3;")
            cnt = curs.rowcount  # 검색한 row 개수를 변수에 저장
            rs = curs.fetchall()

            if cnt == 0:
                rank.clear()
                rank.append("1등 공석")  # 1등 이름
                rank.append("0")  # 1등 점수
                rank.append("2등 공석")  # 2등 이름
                rank.append("0")  # 2등 점수
                rank.append("3등 공석")  # 3등 이름
                rank.append("0")  # 3등 점수
                print(rank)
            elif cnt == 1:
                rank.clear()
                rank.append(rs[0][0])  # 1등 이름
                rank.append(rs[0][1])  # 1등 점수
                rank.append("2등 공석")  # 2등 이름
                rank.append("0")  # 2등 점수
                rank.append("3등 공석")  # 3등 이름
                rank.append("0")  # 3등 점수
                print(rank)
            elif cnt == 2:
                rank.clear()
                rank.append(rs[0][0])  # 1등 이름
                rank.append(rs[0][1])  # 1등 점수
                rank.append(rs[1][0])  # 2등 이름
                rank.append(rs[1][1])  # 2등 점수
                rank.append("3등 공석")  # 3등 이름
                rank.append("0")  # 3등 점수
                print(rank)

            else:
                rank.clear()
                rank.append(rs[0][0])  # 1등 이름
                rank.append(rs[0][1])  # 1등 점수
                rank.append(rs[1][0])  # 2등 이름
                rank.append(rs[1][1])  # 2등 점수
                rank.append(rs[2][0])  # 3등 이름
                rank.append(rs[2][1])  # 3등 점수
                print(rank)
    finally:
        conn.close()


# 접속한 IP 주소 삽입
def connectInsert(ip):
    conn = pymysql.connect(host='localhost', user='root', passwd='11386013', db='tcpip', charset='utf8')
    try:
        with conn.cursor() as curs:
            curs.execute("insert into connect values ('" + ip + "');")  # IP 주소
        conn.commit()
    finally:
        conn.close()


# 접속했던 IP 주소 삭제
def connectDelete(ip):
    conn = pymysql.connect(host='localhost', user='root', passwd='11386013', db='tcpip', charset='utf8')
    try:
        with conn.cursor() as curs:
            curs.execute("delete from connect where ip = '" + ip + "';")
        conn.commit()
    finally:
        conn.close()