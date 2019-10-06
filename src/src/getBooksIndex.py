from dateutil.parser import parse
import time, sys, json, requests
from datetime import datetime
from module.progress import progress_bar

# HTTPS認証の警告文を表示させない
import urllib3
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)

import re
import pandas as pd
# EDINET API URL
EDINET_URL = "https://disclosure.edinet-fsa.go.jp/api/v1/documents.json"
REQUEST_TYPE = 2

edinet_index_table = pd.DataFrame(columns=["data_ymd", "docID", "edinetCode", "secCode", "filerName", "docDescription", "disclosureStatus", "xbrlFlag"])

#
# reg_str = r'.*有価証券'
# reg_pattern = re.compile(reg_str)
# a = reg_pattern.search('有価証券報告書')
# print(a.group())
# datetime.fromtimestamp(string_to_unixTime('2020/2/29'))

# # unitx から 文字列 に逆変換
# # datetime.fromtimestamp(1469804400)

# # 検索区間からイテレーションの回数を取得
get_iteration = lambda _start, _end : (_end - _start) / 86400
# def get_iteration(_start,_end):
#     return (_end - _start) / 86400

isAnnualSecuritiesReport = lambda results_data : \
    True if results_data['docTypeCode'] == "120" and \
    not '投資' in results_data['docDescription']and \
    not '外国会社' in results_data['docDescription']and \
    not '信託' in results_data['docDescription'] else False


def string_to_unixTime(str: str):
    """
    convert string to unix time
    str : string  // YYYY-MM-DD, YYYY/MM/DD
    """
    _time = parse(str)
    _unix_time = int(time.mktime(_time.timetuple()))
    return _unix_time

# 処理の実行を開始する
def indexDoc_toCSV(res_data):
    for _submData in res_data :
        print(_submData['filerName'])

def convert_date_string(day, convert_String):
    """日付の文字列を変換する関数
    """
    _day_unix =string_to_unixTime(day)
    _time_stamp = datetime.fromtimestamp(_day_unix)
    return _time_stamp.strftime(convert_String)

def count_index(res_data):
    """
    検索区間で登録された有報をカウント
    """
    _count = 0
    for i in res_data:
        if isAnnualSecuritiesReport(i):
            _count += 1


    return _count

def index_to_table(res_data, date_ymd):
    global edinet_index_table
    for i in res_data:
        if isAnnualSecuritiesReport(i):
            tmp_series = pd.Series(
            [
                 date_ymd,
                 i["docID"],
                 i["edinetCode"],
                 i["secCode"],
                 i["filerName"],
                 i["docDescription"],
                 i["disclosureStatus"],
                 i["xbrlFlag"]
             ],
            index=edinet_index_table.columns )
            edinet_index_table = edinet_index_table.append( tmp_series, ignore_index=True )



def get_submitted_docIndex(first_day, last_day):
    """
        日ごとに提出されたドキュメントを取得する関数
    """
    max_ite = get_iteration(first_day,last_day)
    print(max_ite)
    _date = first_day
    _counter = 0
    _Nindex = 0
    flg = True
    while flg:
        json_res = ''
        date_str = datetime.fromtimestamp(_date)
        # print(date_str.strftime('%Y-%m-%d'))
        _curr_date = date_str.strftime('%Y-%m-%d')
        params = {"date": _curr_date,
                  "type": REQUEST_TYPE}
        res = requests.get(EDINET_URL, params=params, verify=False)
        response = res.text
        json_res = json.loads(response)
        # 404 status flg
        flg = (json_res['metadata']['status']=='200')
        # print(flg, json_res['metadata']['status'])
        if len(json_res['results']) > 0:
            # 検索区間の有報をカウントする用
            _Nindex += count_index(json_res['results'])

            # 検索区間の有報をcsvに保存する用
            index_to_table(json_res['results'], _curr_date)

        output_text = _curr_date + ' count : ' + str(json_res['metadata']['resultset']['count']) + ' Index : ' + str(_Nindex)
        # output_text = _curr_date + ' count : ' + str(json_res['metadata']['resultset']['count']) + ' Index : ' +json_res['results']['formCode']
        progress_bar(_counter, max_ite,output_text)

        # day, counter update
        _date += 86400
        _counter += 1

        # API requests waiting
        time.sleep(0.5)
        if last_day < _date:
            break


def main(START_DAY:str, END_DAY:str):
    print(START_DAY+ ' to ' + END_DAY)
    start_day_unix = string_to_unixTime(START_DAY)
    end_day_unix = string_to_unixTime(END_DAY)
    print(start_day_unix, end_day_unix)
    start_time = time.time()

    get_submitted_docIndex(start_day_unix, end_day_unix)

    elapsed_time = time.time() - start_time
    print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")

    file_name ='{0}_{1}.csv'.format(
        convert_date_string(START_DAY,'%Y%m%d'),
        convert_date_string(END_DAY,'%Y%m%d'))
    edinet_index_table.to_csv(file_name, mode='a')



# エントリーポイント
if __name__ == "__main__":
    sys.argv.pop(0)
    START_DAY =sys.argv[0]
    END_DAY =sys.argv[1]
    main(START_DAY, END_DAY)

# string_to_unixTime('2015年3月3日')





#
# print("\033[36mPrefecture   : " + df[0].iat[0, 1] + "\033[0m")
# print("\033[36mCategory     : " + df[0].iat[1, 1] + "\033[0m")
# print("\033[36mPage         : " + str(last_page) + "\033[0m")
# progress_bar(1, last_page)
#
#
# {'seqNumber': 1,
# 'docID': 'S1002L3M',
# 'edinetCode': 'E09666',
# 'secCode': None,
# 'JCN': '9010001062807',
# 'filerName': 'アムンディ・ジャパン株式会社',
# 'fundCode': 'G10540',
# 'ordinanceCode': '030',
# 'formCode': '04A000',
# 'docTypeCode': '030',
# 'periodStart': None,
# 'periodEnd': None,
# 'submitDateTime': '2014-08-04 09:01',
# 'docDescription': '有価証券届出書（内国投資信託受益証券）',
# 'issuerEdinetCode': None,
# 'subjectEdinetCode': None,
# 'subsidiaryEdinetCode': None,
# 'currentReportReason': None,
# 'parentDocID': None,
# 'opeDateTime': None,
# 'withdrawalStatus': '0',
# 'docInfoEditStatus': '0',
# 'disclosureStatus': '0',
# 'xbrlFlag': '1',
# 'pdfFlag': '1',
# 'attachDocFlag': '1',
# 'englishDocFlag': '0'},
#
#
# {"seqNumber": 100,
# "docID": "S100FU3Z"
#  "edinetCode": "E03473"
#  "secCode": "30300"
#  "JCN": "8010001087103"
#  "filerName": "株式会社ハブ"
#  "fundCode": None
#  "ordinanceCode": "010"
#  "formCode": "030000"
#  "docTypeCode": "120"
#  "periodStart": "2018-03-01"
#  "periodEnd": "2019-02-28"
#  "submitDateTime": "2019-05-23 10: 35"
#  "docDescription": "有価証券報告書－第21期(平成30年3月1日－平成31年2月28日)"
#  "issuerEdinetCode": None
#  "subjectEdinetCode": None
#  "subsidiaryEdinetCode": None
#  "currentReportReason": None
#  "parentDocID": None
#  "opeDateTime": None
#  "withdrawalStatus": "0"
#  "docInfoEditStatus": "0"
#  "disclosureStatus": "0"
#  "xbrlFlag": "1"
#  "pdfFlag": "1"
#  "attachDocFlag": "1"
#  "englishDocFlag": "0"
# progress bar test
# def test_progress_bar():
#     for i in range(0, 100):
#         progress_bar(i, 99)
#         time.sleep(0.5)
#
#
# def test(str):
#     params = {"date": str, "type": 2}
#     res = requests.get(EDINET_URL, params=params, verify=False)
#     response = res.text
#     json_res = json.loads(response)
#     res = json_res['results']
#     # print(res)
#     _count = 0
#     for i in res:
#         # print(i['docDescription'] )
#         if isAnnualSecuritiesReport(i):
#             print(str, i["docID"], i["edinetCode"], i["secCode"], i["filerName"], i["docDescription"], i["disclosureStatus"], i["xbrlFlag"])
#
#     return _count
#
# # test("2018-06-20")

# def gettable_oldest_date(first_day, last_day):
#     """指定した区間で遡れる日付を返す
#     """
#     max_ite = get_iteration(first_day,last_day)
#     _date = first_day
#     _counter = 0
#     _Nindex = 0
#     flg = True
#     while flg:
#         json_res = ''
#         date_str = datetime.fromtimestamp(_date)
#         # print(date_str.strftime('%Y-%m-%d'))
#         _curr_date = date_str.strftime('%Y-%m-%d')
#         params = {"date": _curr_date,
#                   "type": REQUEST_TYPE}
#         res = requests.get(EDINET_URL, params=params, verify=False)
#         response = res.text
#         json_res = json.loads(response)
#         # 404 status flg
#         flg = (json_res['metadata']['status']=='200')
#         print(_curr_date)
#         if not flg:
#             return _curr_date
#
#         # day, counter update
#         _date += 86400
#         _counter += 1
#         if last_day < _date:
#             break
#
#     return 'available All day'
#

# gettable_oldest_date(string_to_unixTime('2019-06-01'), string_to_unixTime('2019-06-30'))
