from flask import *
from pymongo import MongoClient

#idChkDictionary = {}  # ID : 해당 ID가 존재하면 1 존재하지 않으면 0

# DB 연동
conn = MongoClient('mongodb://localhost:27017/')  # MongoDB IP : 127.0.0.1, PORT : 27017, use information
# DB 생성
informationDB = conn['information']
# collections 생성
# collect = db.information
# 값 출력
# result = collect.find()
# for docs in result :
#     print(docs)

# for docs in db.information.find():
#     print(docs)

def idChk(id):
    x = informationDB.information.count_documents( {"id":id} )  # 조회된 값 개수
    return x

def login(id, pw):
    # 접속 속도 우선순위 : 1) 고객 2) 직원 3) 관리자
    resultCustomer = informationDB.information.count_documents(  # 조회된 값 개수
        {"power": "customer", "id": id, "pw": pw}
    )
    resultStaff = informationDB.information.count_documents(  # 조회된 값 개수
        {"power": "staff", "id": id, "pw": pw}
    )
    resultManager = informationDB.information.count_documents(  # 조회된 값 개수
        {"power": "manager", "id": id, "pw": pw}
    )

    if resultCustomer == 1:
        return "resultCustomer"
    elif resultStaff == 1:
        return "resultStaff"
    elif resultManager == 1:
        return "resultManager"
    else:
        return "error"

    print(resultCustomer, resultStaff, resultManager)

    # x = informationDB.information.count_documents(  # 조회된 값 개수
    #     {"id": id, "pw": pw}
    # )
    # return x

def signupInsert(name, id, pw, phone, gender, age):
    # DB 연동
    # conn = MongoClient('mongodb://localhost:27017/')  # MongoDB IP : 127.0.0.1, PORT : 27017, use information
    # # DB 생성
    # informationDB = conn['information']
    # 삽입된 문서의 ID를 보유 하는 InsertOneResult 객체를 반환. _id 필드를 지정 하지 않으면 MongoDB가 필드를 추가 하고 각 문서에 고유한 ID를 할당.
    informationDB.information.insert_one( {"power": "customer", "name": name, "id": id, "pw": pw, "phone": phone, "gender": gender, "age": age} )
    # DB 종료
    # conn.close(se)

def closeDB():
    conn.close()
