#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
EDINETから有報を取得するAPI

"""
from module.progress import progress_bar
from dateutil.parser import parse
from datetime import datetime
import time, os, json, requests, sys, io, re
from bs4 import BeautifulSoup as bs
import pandas as pd
import zipfile
from lxml.etree import XMLParser as etree_XMLParser
from lxml.etree import fromstring as etree_fromstring
import lxml.etree
import mojimoji # 半角全角変換
# HTTPS認証の警告文を表示させない
import urllib3
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)

# CONSTABT para

GETDOC_URL = "https://disclosure.edinet-fsa.go.jp/api/v1/documents/"
PARAMS = {"type": 1} # type : 1, 2, 3, 4
KEYS =[
    {'namespace' : 'jpcrp_cor', 'elementName' : 'FiscalYearCoverPage', 'id' : 'series_data', 'value' : ''
    },
    {'namespace' : 'jpcrp_cor', 'elementName' : 'CompanyNameCoverPage', 'id' : 'filerName', 'value' : ''
    },
    {'namespace' : 'jpcrp_cor', 'elementName' : 'NetSalesSummaryOfBusinessResults', 'id' : 'NetSales', 'value' : ''
    },
    {'namespace' : 'jpcrp_cor', 'elementName' : 'OrdinaryIncomeLossSummaryOfBusinessResults', 'id' : 'OrdinaryIncomeLoss', 'value' : ''
    },
    {'namespace' : 'jpcrp_cor', 'elementName' : 'ProfitLossAttributableToOwnersOfParentSummaryOfBusinessResults', 'id' : 'ProfitLoss', 'value' : ''
    },
    {'namespace' : 'jpcrp_cor', 'elementName' : 'NetAssetsSummaryOfBusinessResults', 'id' : 'NetAssets', 'value' : ''
    },
    {'namespace' : 'jpcrp_cor', 'elementName' : 'TotalAssetsSummaryOfBusinessResults', 'id' : 'tAssets', 'value' : ''
    },
    {'namespace' : 'jpcrp_cor', 'elementName' : 'NetAssetsPerShareSummaryOfBusinessResults', 'id' : 'psNetAssets', 'value' : ''
    },
    {'namespace' : 'jpcrp_cor', 'elementName' : 'BasicEarningsLossPerShareSummaryOfBusinessResults', 'id' : 'psBasicEarningsLoss', 'value' : ''
    },
    {'namespace' : 'jpcrp_cor', 'elementName' : 'RateOfReturnOnEquitySummaryOfBusinessResults', 'id' : 'ROE', 'value' : ''
    },
    {'namespace' : 'jpcrp_cor', 'elementName' : 'NetCashProvidedByUsedInOperatingActivitiesSummaryOfBusinessResults', 'id' : 'cfOperating', 'value' : ''
    },
    {'namespace' : 'jpcrp_cor', 'elementName' : 'NetCashProvidedByUsedInInvestingActivitiesSummaryOfBusinessResults', 'id' : 'cfInvesting', 'value' : ''
    },
    {'namespace' : 'jpcrp_cor', 'elementName' : 'NetCashProvidedByUsedInFinancingActivitiesSummaryOfBusinessResults', 'id' : 'cfFinancing', 'value' : ''
    },
    {'namespace' : 'jpcrp_cor', 'elementName' : 'CashAndCashEquivalentsSummaryOfBusinessResults', 'id' : 'CashEquivalents', 'value' : ''
    },
    {'namespace' : 'jpcrp_cor', 'elementName' : 'TotalNumberOfIssuedSharesSummaryOfBusinessResults', 'id' : 'tIssuedShares', 'value' : ''
    },
    {'namespace' : 'jpcrp_cor', 'elementName' : 'CapitalExpendituresOverviewOfCapitalExpendituresEtc', 'id' : 'Capex', 'value' : ''
    },
    {'namespace' : 'jppfs_cor', 'elementName' : 'Inventories', 'id' : 'Inventories', 'value' : ''
    },
    {'namespace' : 'jppfs_cor', 'elementName' : 'GrossProfit', 'id' : 'GrossProfit', 'value' : ''
    },
    {'namespace' : 'jppfs_cor', 'elementName' : 'OperatingIncome', 'id' : 'OperatingProfit', 'value' : ''
    },
    {'namespace' : 'jppfs_cor', 'elementName' : 'DepreciationSGA', 'id' : 'Depreciation', 'value' : ''
    },
    {'namespace' : 'jppfs_cor', 'elementName' : 'NotesAndAccountsReceivableTrade', 'id' : 'acReceivable', 'value' : ''
    },
    {'namespace' : 'jppfs_cor', 'elementName' : 'NotesAndAccountsPayableTrade', 'id' : 'acPayable', 'value' : ''
    },
    {'namespace' : 'jppfs_cor', 'elementName' : 'ShortTermBondsPayable', 'id' : 'stBonds', 'value' : ''
    },
    {'namespace' : 'jppfs_cor', 'elementName' : 'ShortTermLoansPayable', 'id' : 'stLoans', 'value' : ''
    },
    {'namespace' : 'jppfs_cor', 'elementName' : 'CommercialPapersLiabilities', 'id' : 'CP', 'value' : ''
    },
    {'namespace' : 'jppfs_cor', 'elementName' : 'CurrentPortionOfBonds', 'id' : 'cpBonds', 'value' : ''
    },
    {'namespace' : 'jppfs_cor', 'elementName' : 'CurrentPortionOfLongTermLoansPayable', 'id' : 'cpLoans', 'value' : ''
    },
    {'namespace' : 'jppfs_cor', 'elementName' : 'BondsPayable', 'id' : 'Bonds', 'value' : ''
    },
    {'namespace' : 'jppfs_cor', 'elementName' : 'LongTermLoansPayable', 'id' : 'ltLoans', 'value' : ''
    },
    {'namespace' : 'jppfs_cor', 'elementName' : 'ShareholdersEquity', 'id' : 'ShareholdersEquity', 'value' : ''
    },
    {'namespace' : 'jppfs_cor', 'elementName' : 'ValuationAndTranslationAdjustments', 'id' : 'Valuation', 'value' : ''
    }
]

ROE_Flg = True
ROE_TABLE_Flg =True
REQUESTS_Flg = True # リクエストが成功したか否か
MULTI_XBRL_Flg =False # 取得したXBRLファイルが複数の時

# KEYS[0]['value'] = [1,2,3,4]
# KEYS[0]['value'][2]
# indexするCSV_DB
index_db = '/Users/abekeishi/code/gs_team_dev_repositry/src/indexed_edinetDB_reduce.csv'
# デバッグ用
# index_db = '/Users/abekeishi/code/gs_team_dev_repositry/src/EDINET_indexDB.csv'

# 雛形になるCSV
report_db = '/Users/abekeishi/code/gs_team_dev_repositry/src/report_db.csv'
output_csv = '/Users/abekeishi/code/gs_team_dev_repositry/src/EDINET_DB_debug_win.csv'
REG_SEASON = r'.*第([0-9]*)期'
SEASON_PATTERN = re.compile(REG_SEASON)

REG_YEAR = r'([0-9]{4})年'
YEAR_PATTERN = re.compile(REG_YEAR)
JC_AC_PATTERN = re.compile(r'.*(明治|大正|昭和|平成|令和)([元0-9０-９]*)年.*')

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

    """ END Class　"""


def convart_JapaneseCalender_toAD(matches):
    if matches:
        era_name = matches.group(1)
        year = matches.group(2);
        if year == '元':
            year = 1
        else:
            if sys.version_info < (3, 0):
                year = year.decode('utf-8')
            year = int(year)

        if era_name == '明治':
            year += 1867
        elif era_name == '大正':
            year += 1911
        elif era_name == '昭和':
            year += 1925
        elif era_name == '平成':
            year += 1988
        elif era_name == '令和':
            year += 2018

        return year

    return None;

def is_int(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()

convart_intORfloat = lambda str : int(float(str)) if is_int(str) else float(str)

# get_ROE は オブジェクトを返す各期、対応する年、ROE
def get_ROE(htm_file:list)-> list:
    return 0

def get_report_requests(url:str, param: object)-> object:
    return requests.get(url, params=param, verify=False)

# HTMファイルからテーブルを探索する関数
def read_HTM(htm: list):
    print('')


def parse_file(file, file_data=None, recover=False):
    """XMLファイルを読み込む"""
    # 解析エラーを回復して続行するか否かの設定
    parser = etree_XMLParser(recover=True)
    if file_data is None:
        # ファイルパスから読み込む
        with open(file, 'rb') as f:
            return etree_fromstring(f.read(), parser=parser)
    else:
        # バイナリデータから読み込む
        xbrl = etree_fromstring(file_data, parser=parser)
        return  xbrl


def get_elemnt_contents(xbrl_text:str, ns:dict, xp:str):
    return xbrl_text.xpath(xp, namespaces=ns)

def get_seasonNo(season_text:str)->int:
    results = SEASON_PATTERN.findall(mojimoji.zen_to_han(season_text))
    season = int(results[0]) if len(results)>0 else None
    season
    return season

def get_yearNo(year_text:str)->int:
    """半角全角、西暦和暦を吸収しつつ西暦を返す"""
    results = YEAR_PATTERN.findall(mojimoji.zen_to_han(year_text))
    year = int(results[1]) if len(results)>0 else None
    # 和暦マッチ
    matches = JC_AC_PATTERN.match(year_text)
    # 和暦だったら変換して返す
    if matches : return convart_JapaneseCalender_toAD(matches)

    return year



def merge_dic(rep_dic, KEYS_dic):
    """二つのdicを統合してreport_dicを返す
    ==================
    Param
    ==================
    rep_dic : 出力用の辞書データ
    KEYS_dic: 取得したデータ群
    """
    for keys_index,  key_id in enumerate(KEYS_dic):
        # print(key_id['id'])
        new_list = KEYS_dic[keys_index]['value'][::-1]
        for index, out_dic in enumerate(reversed(rep_dic)):
            if index >= len(new_list): break
            out_dic[key_id['id']] = new_list[index]

                # # out_index[key_id] =
                # pass
    return rep_dic


def getElement_xbrl(xbrl_text:str, dic_list:list)-> dict:
    count = 0
    ns = xbrl_text.nsmap

    curr_year = get_elemnt_contents(
                xbrl_text,
                ns,
                "//*[contains(name(),'{0}')]".format('FiscalYearCoverPage'))
    try:
        tmp_text = curr_year[0].text.replace(u"\xa0",u"")
        tmp_text = tmp_text.replace('\n','')
        output_text = 'current : ' + mojimoji.zen_to_han(tmp_text)
    except IndexError:
        output_text = 'Parse Error'
        return False, output_text

    seasonNo = get_seasonNo(tmp_text) if len(curr_year)>0 else None
    yearNo = get_yearNo(tmp_text) if len(curr_year)>0 else None

    if type(seasonNo) == int and type(yearNo)==int:
        pre_seasonNo = seasonNo
        pre_yearNo = yearNo
        # print(pre_yearNo, pre_seasonNo)

        if len(dic_list) > 1:
            len_dic = len(dic_list) - 1
            for _index in range(len(dic_list)):
                # print(dic_list[len_dic - _index])
                dic_list[len_dic - _index]['year'] = pre_yearNo
                dic_list[len_dic - _index]['season'] = pre_seasonNo
                pre_seasonNo -= 1
                pre_yearNo -= 1
        else:
            dic_list[0]['year'] = pre_yearNo
            dic_list[0]['season'] = pre_seasonNo
    # print(dic_list)

    tmp_elem = []
    # print('\033[36mSeason No : ' + str(seasonNo) + "\033[0m")
    for jp in KEYS:
        # if count==len(KEYS): break
        # print('\033[36m' + jp['elementName'] + "\033[0m")
        # 指定したKeyのデータを取得しに行く
        elem = get_elemnt_contents(
                xbrl_text,
                ns,
                "//*[contains(name(),'{0}')]".format(jp['elementName'])
            )
        # なければ抜ける
        jp['value'] = [] #ちゃんと初期化
        if len(elem)==0: continue
        for i in elem:
            if i.text is not None:
                # print('\033[31m'+ i.attrib['contextRef']+'  ::  '+jp['elementName']+ ' : ' + i.text + "\033[0m")
                try :
                    jp['value'].append(convart_intORfloat(i.text))
                except ValueError:
                    if len(i.text) > 200:
                        jp['value'].append('long text')
                    else:
                        tmp_text = i.text.replace(u"\xa0",u"")
                        tmp_text = tmp_text.replace('\n','')
                        jp['value'].append(tmp_text)
                # print(i.attrib['contextRef'],i.text)
            else:
                # print(i.attrib['contextRef']+'  ::  '+ jp['elementName'], i.text)
                jp['value'].append(None)
            if 'CurrentYear' in i.attrib['contextRef'] : break

    return merge_dic(dic_list, KEYS),output_text


# そもそもZipで取れなかった時の判定を噛ませる

def exception_process(flg: str, dict: object):
    """再代入用のシリーズを作成して返す
    flg : エラーフラグを指定
    info_series : 現状わかっている
    """
    dict[flg] = 444
    return dict

def edinet_duplication(code_list: list, edinetCode:str)->list :
    """ 過去に取得したことのある会社なのか あればFalseを返す """
    if edinetCode in code_list:
        return False, code_list
    else:
        code_list.append(edinetCode)
        return True, code_list

def main():
    """DBの呼び出し, 処理実行リストの作成"""
    # CSVを読み込み
    index_csv = pd.read_csv(index_db,index_col=0).reset_index(drop=True)
    max_ite = len(index_csv) - 1
    # 出力用テーブルを作成
    tmp_csv = pd.read_csv(report_db)
    output_colums = pd.read_csv(output_csv)
    last_docID = list(output_colums.loc[:, 'docID'])
    last_docID = last_docID[len(last_docID)-1]
    edinet_code_list = list(set(list(output_colums.loc[:, 'edinetCode'])))
    # print(edinet_code_list)
    del(output_colums)

    _counter = index_csv.query('docID == "{}"'.format(last_docID)).index[0] + 1
    index_csv = index_csv.drop(range(0,_counter))

    # テンプレートのカラム名を取得
    tmp_columns = list(tmp_csv.columns)
    index_columns =list(index_csv.columns)

    tmp_columns
    # index_columns
    # 2つの共通要素を抜き出すためのリスト
    common_list = set(index_columns) & set(tmp_columns)
    # common_list
    # DBに突っ込む用のKEY_IDの設定
    # KEYS_ID_list = [_id['id'] for _id in KEYS]

    # 出力用
    report_list =[]



    companyFlg = True

    for index in index_csv.iterrows():
        report_df = pd.DataFrame([], columns=tmp_columns)
        output_text = ''
        companyFlg = True
        report_value = [None] * len(tmp_columns) #要素の数だけNone

        report_dic = dict(zip(tmp_columns, report_value))
        report_diclist = []
        companyFlg, edinet_code_list = edinet_duplication(edinet_code_list, index[1]['edinetCode'])
        # 共通リストの入力を行う
        for key in common_list:
            report_dic[key] = index[1][key]

        if index[1]['disclosureStatusFlg'] != 0:
            report_list.append(exception_process('disclosureStatusFlg',report_dic))
            progress_bar(_counter, max_ite,'count : '+str(_counter) + " | " +'flgError : ' + index[1]['docID'])
            _counter += 1
            continue
        if index[1]['xbrlFlg'] != 1:
            report_list.append(exception_process('xbrlFlg',report_dic))
            progress_bar(_counter, max_ite,'count : '+str(_counter) + " | " +'flgError : ' + index[1]['docID'])
            _counter += 1
            continue
        # print("companyFlg : {}".format(companyFlg))
        if companyFlg:
            for copy in range(5) : report_diclist.append(report_dic.copy())
        else:
            report_diclist.append(report_dic.copy())

        requestURL = GETDOC_URL + index[1]['docID']
        res = get_report_requests(requestURL,PARAMS)
        if res.status_code == 200:
            # zip クラスを呼び出してfileを読み込み
            _zip = Extract_zip(res.content)
            # _zip.save_zip('debug.zip') # デバッグ用にzipを展開する
            del(res)
            if len(_zip.get_xbrl_filename()) == 0:
                report_list.append(exception_process('ParseFlg',report_dic))
                # progress_bar(_counter, max_ite,'count : '+str(_counter) + " | " + output_text + index[1]['docID'])
                progress_bar(_counter, max_ite,'count : '+str(_counter) + " | " + index[1]['filerName'] + " :  " + index[1]['docID'])
                print('\r\036[K' + 'Parse Error' + "\033[0m")
                _counter += 1
                continue
            file = _zip.extract_file(_zip.get_xbrl_filename()[0])
            del(_zip)
            parser = etree_XMLParser(recover=True)
            parsed_xbrl = etree_fromstring(file, parser=parser)

            report_diclist, output_text = getElement_xbrl(parsed_xbrl,report_diclist)

            if report_diclist is False :
                report_list.append(exception_process('ParseFlg',report_dic))
                progress_bar(_counter, max_ite,'count : '+str(_counter) + " | " + index[1]['filerName'] + " :  " + index[1]['docID'])
                _counter += 1
                continue
            # print(report_diclist)
            # ns = parsed_xbrl.nsmap
            # xp = "//*[contains(name(),'{0}')]".format('ValuationAndTranslationAdjustments')
            # elem = parsed_xbrl.xpath(xp, namespaces=ns)

        else:
            del(res)
            report_list.append(exception_process('RequestFlg',report_dic))
            progress_bar(_counter, max_ite,'count : '+str(_counter) + " | " + 'Request Error')
            _counter += 1
            continue

        # progress_bar(_counter, max_ite,'count : '+str(_counter) + " | " + output_text + index[1]['docID'])
        progress_bar(_counter, max_ite,'count : '+str(_counter) + " | " + index[1]['filerName'] + " :  " + index[1]['docID'])
        _counter += 1
        # 全ての処理が終わって、dicができたらlist突っ込む

        for diclist in report_diclist:
            report_list.append(diclist)

        # print(report_list)
        # 自動保存
        if _counter%30 == 0:
            # print(report_list)
            report_df = pd.concat([report_df, pd.DataFrame.from_dict(report_list)], sort=True)
            # print(report_list)
            print('-----------{}------------'.format(index[1]['docID']))
            report_df.to_csv(output_csv, mode='a' , header=False)
            del(report_df)
            time.sleep(2)
            # print('debug-003')
            report_list = [] # concatで追記しないように初期化
            # except:
            #     import traceback
            #     traceback.print_exc()


    report_df = pd.concat([report_df, pd.DataFrame.from_dict(report_list)], sort=True)
    report_df.to_csv(output_csv, mode='a', header=False)

    return True

if __name__ == "__main__":
    main()
#
# print(res.encoding)
# print(res.headers)
# print(res.headers['Content-Type'])
# print('.html' in 'fafaa.htm')
#

# season_text = '第９期（自　2018年４月１日　至　2019年３月31日）'
# season_text = '第71期(自 平成30年4月1日 至 昭和40年3月31日)'
# YEAR_PATTERN.findall(mojimoji.zen_to_han(season_text))
# YEAR_PATTERN.findall(season_text)
# int(YEAR_PATTERN.findall(season_text)[0])
# matches = JC_AC_PATTERN.match(season_text)
# print(matches)
