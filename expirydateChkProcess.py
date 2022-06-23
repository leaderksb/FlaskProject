#-*- coding: utf-8 -*-

# AM 00:01마다 해당 일자를 확인한 뒤, 이전 일자 유통기한을 가진 제품 정보 삭제

import pymysql
import logging
import logging.handlers

def expirydateChkSelect():  # 유통기한 지난 제품 코드 조회
    conn = pymysql.connect(host='10.0.155.2', user='admin', passwd='fresh-maria', db='intern', charset='utf8')
    # conn = pymysql.connect(host='localhost', user='root', passwd='maria', db='intern', charset='utf8')

    try:
        with conn.cursor() as curs:
            curs.execute("select code from expirydate where expirydate < now();")
            rs = curs.fetchall()
            # print(rs)
            expirydateChkList = []
            for row in rs:
                expirydateChkList.append(row)
            rsLen = len(rs)
            # print("rsLen", rsLen)
            resultChkList = []
            for l in range(rsLen):
                # print(expirydateChkList[l][0])
                resultChkList.append(expirydateChkList[l][0])
            return resultChkList
    finally:
        conn.close()  # DB 종료

codeList = expirydateChkSelect()  # 유통기한 지난 제품 코드 리스트

def log(codeList):  # 로그
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(pathname)s %(processName)s %(thread)d %(funcName)s %(name)s %(message)s')

    streamhandler = logging.StreamHandler()
    streamhandler.setFormatter(formatter)
    logger.addHandler(streamhandler)

    logger.debug(codeList)
    # logger.info("INFO 모드")
    # logger.warn("WARN 모드")

    timedfilehandler = logging.handlers.TimedRotatingFileHandler(filename='./cron/cron.log', when='M', interval=1, encoding='utf-8')
    timedfilehandler.setFormatter(formatter)
    timedfilehandler.suffix = "%Y%m%d"

    logger.addHandler(timedfilehandler)

log(codeList)

def expirydateDelete():  # 지난 유통기한 삭제
    conn = pymysql.connect(host='10.0.155.2', user='admin', passwd='fresh-maria', db='intern', charset='utf8')
    # conn = pymysql.connect(host='localhost', user='root', passwd='maria', db='intern', charset='utf8')

    try:
        with conn.cursor() as curs:
            curs.execute("delete from expirydate where expirydate < now();")
        conn.commit()
    finally:
        conn.close()

def productDelete(codeList):  # 유통기한 지난 제품 삭제
    conn = pymysql.connect(host='10.0.155.2', user='admin', passwd='fresh-maria', db='intern', charset='utf8')
    # conn = pymysql.connect(host='localhost', user='root', passwd='maria', db='intern', charset='utf8')
    try:
        with conn.cursor() as curs:
            #print(codeList)
            cLen = len(codeList)
            for c in range(cLen):
                curs.execute("delete from product where code = '" + codeList[c] + "';")
        conn.commit()
    finally:
        conn.close()

expirydateDelete()
productDelete(codeList)

#print("expirydateChkProcess")
