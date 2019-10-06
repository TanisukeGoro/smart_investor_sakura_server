# 重複したデータを削除するスクリプト

import pandas as pd
from pathlib import Path
# Pathオブジェクトを生成
# p = Path("/Users/abekeishi/Public/2.Programing/Python3/Wi2Map/out_put_data/")
#
# pathlist = list(p.glob("*.csv"))
#
# print(len(pathlist))
# all_lines = 0
# for _path in pathlist:
# hoge = pd.read_table('/Users/abekeishi/code/gs_team_dev_repositry/src/financial_report.csv',index_col=1)
hoge = pd.read_csv('/Users/abekeishi/code/gs_team_dev_repositry/src/financial_report.csv').reset_index(drop=True)

# hoge = pd.read_csv('/Users/abekeishi/code/gs_team_dev_repositry/src/API_TEST/test.csv')
print(hoge)
hoge.sort_values(by=['edinetCode','year'])
no_duplicated_hoge = hoge.drop_duplicates(subset=['edinetCode','year'],keep='first')
no_duplicated_hoge.to_csv('/Users/abekeishi/code/gs_team_dev_repositry/src/financial_report_duplicates.csv', index=True)
