from dateutil.parser import parse
import json
import requests
from datetime import datetime
import time


# #↓エンドポイント
# #バージョンが変わるたびに”v1"の部分を変更する必要がある模様
url = "https://disclosure.edinet-fsa.go.jp/api/v1/documents.json"
# currtime = datetime.now()
# currtime.strftime('%Y-%m-%d')
#
# oldetime = parse("2016-07-30")
# olde_unixtime = int(time.mktime(oldetime.timetuple()))
# print(olde_unixtime)
# olde_unixtime += 86400*3
# olde_time = datetime.fromtimestamp(olde_unixtime)
# olde_time.strftime('%Y-%m-%d')
#
#
# #必須パラメータのdateをぶちこむ
# #出力結果を変えるためにtypeを2にする（type=1だとmetadataしか出力されない）
# params = {"date": olde_time.strftime('%Y-%m-%d'), "type": 2}
params = {"date": '2014-07-30', "type": 2}
#
# #このAPIはREST APIなのでverifyをFalseにして接続するときのSSLを無効化する
res = requests.get(url, params=params, verify=False)
#
response = res.text
print(type(response))
json_res = json.loads(response)
print(json_res)
print(json_res['metadata'])
print(json_res['metadata']['status']=='200')
#
# flg = (json_res['metadata']['status']=='200')
# print(flg)
#
#
# curr_unixtime = int(time.mktime(currtime.timetuple()))
# print(curr_unixtime)
#
#
#
#
#
#
# def get_oldest_data(first_day, last_day):
#     """APIの取得可能な期間を取得
#     """
#     url = "https://disclosure.edinet-fsa.go.jp/api/v1/documents.json"
#     date = first_day
#     print('first_day',date)
#     flg = True
#     while flg:
#         date_str = datetime.fromtimestamp(date)
#         print(date_str.strftime('%Y-%m-%d'))
#         params = {"date": date_str.strftime('%Y-%m-%d'),
#                   "type": 2}
#         res = requests.get(url, params=params, verify=False)
#         response = res.text
#         json_res = json.loads(response)
#         print(json_res['metadata']['resultset']['count'])
#         flg = (json_res['metadata']['status']=='200')
#         date += 86400
#         if last_day<date:
#             print('exit')
#             break
#     print(date)
#
# print(1406646000, 1406646010)
# get_oldest_data(1469804400, 1470236400)
#
#

{'seqNumber': 1,
'docID': 'S1002L3M',
'edinetCode': 'E09666',
'secCode': None,
'JCN': '9010001062807',
'filerName': 'アムンディ・ジャパン株式会社',
'fundCode': 'G10540',
'ordinanceCode': '030',
'formCode': '04A000',
'docTypeCode': '030',
'periodStart': None,
'periodEnd': None,
'submitDateTime': '2014-08-04 09:01',
'docDescription': '有価証券届出書（内国投資信託受益証券）',
'issuerEdinetCode': None,
'subjectEdinetCode': None,
'subsidiaryEdinetCode': None,
'currentReportReason': None,
'parentDocID': None,
'opeDateTime': None,
'withdrawalStatus': '0',
'docInfoEditStatus': '0',
'disclosureStatus': '0',
'xbrlFlag': '1',
'pdfFlag': '1',
'attachDocFlag': '1',
'englishDocFlag': '0'},


{"seqNumber": 100,
"docID": "S100FU3Z"
 "edinetCode": "E03473"
 "secCode": "30300"
 "JCN": "8010001087103"
 "filerName": "株式会社ハブ"
 "fundCode": None
 "ordinanceCode": "010"
 "formCode": "030000"
 "docTypeCode": "120"
 "periodStart": "2018-03-01"
 "periodEnd": "2019-02-28"
 "submitDateTime": "2019-05-23 10: 35"
 "docDescription": "有価証券報告書－第21期(平成30年3月1日－平成31年2月28日)"
 "issuerEdinetCode": None
 "subjectEdinetCode": None
 "subsidiaryEdinetCode": None
 "currentReportReason": None
 "parentDocID": None
 "opeDateTime": None
 "withdrawalStatus": "0"
 "docInfoEditStatus": "0"
 "disclosureStatus": "0"
 "xbrlFlag": "1"
 "pdfFlag": "1"
 "attachDocFlag": "1"
 "englishDocFlag": "0"






url = "https://disclosure.edinet-fsa.go.jp/api/v1/documents/S10046RE"

#書類取得APIにはtypeパラメータが４つある。２はPDFを出力してくれる。
params = {"type": 1}

#出力先ファイル
file_name = "test.zip"

class Extract_zip:
    def __init__(self, zip_obj):
        self.zip_obj = zip_obj
        self.post = ''

    def save_zip(self, file_name: str):
        try:
            with open(file_name, 'wb') as f:
                f.write(self.zip_obj)
            f.close()
            return True
        except:
            return False

    def extract_zip(self):
        byte_res = io.BytesIO(self.zip_obj) # メモリ上でバイトファイルを扱うため
        try:
            with zipfile.ZipFile(byte_res, 'r') as _post:
                self.post = _post
            return self.post
        except zipfile.BadZipfile:
            REQUESTS_Flg =False
            # 終了処理
            return False

    def get_xbrl_filename(self)-> list:
        """getting xbrl file"""
        self.post = self.extract_zip()
        if not self.post : return False
        xbrl_doc = []
        for info in self.post.infolist():
            if 'XBRL/PublicDoc/' in info.filename:
                if '.xbrl' in info.filename : xbrl_doc.append(info.filename)
        return xbrl_doc

    def get_htm_filename(self)-> list:
        """getting htm file"""
        post = self.extract_zip()
        if not post : return False
        htm_doc = []
        for info in post.infolist():
            if 'XBRL/PublicDoc/' in info.filename:
                if '.htm' in info.filename : htm_doc.append(info.filename)
        return htm_doc

    def extract_file(self,file_name:str):
        # self.post = self.extract_zip()
        byte_res = io.BytesIO(self.zip_obj) # メモリ上でバイトファイルを扱うため
        try :
            with zipfile.ZipFile(byte_res, 'r') as _post:
                with _post.open(file_name) as file:
                    return file.read()
        except:
            return False

#先ほどと同じ接続方法に加えて、取得ファイルが大きいときのために
#stream=Trueにすることでメモリに優しい接続方法にしておく
import sys
res = requests.get(url, params=params, verify=False)
print(type(res))
print(res.encoding)
print(res.headers)
print(res.headers['Content-Type'])
zipObj = Extract_zip(res.content)
zipObj.save_zip('S10046RE.zip')
print(res.status_code)
if res.status_code == 200:
    with open('test.zip', 'wb') as f:
        f.write(res.content)
