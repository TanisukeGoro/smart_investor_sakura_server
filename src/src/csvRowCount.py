"""
指定した csv ファイルの行数をカウントしたり
csvを結合したりする
"""

from pathlib import Path
import os
import glob
import re
import pandas as pd
# Pathオブジェクトを生成
p = "/Users/abekeishi/Public/2.Programing/GsAcademy_講義資料/20190621/dev/有報_index"
file_list = sorted(glob.glob(p+'/*.csv'))
file_list = [s for s in file_list if re.match('.*有報のみ.*', s)]
list = []
for i in file_list :
    list.append(pd.read_csv(i))
df = pd.concat(list, sort=False)
df = df.reset_index(drop=True)
df.to_csv('全期間.csv', encoding='utf_8')
# print(len(pathlist))
# all_lines = 0
# for _path in pathlist:
#     print(_path)
#     # num_lines = sum(1 for line in open(_path))
#     # print(os.path.basename(_path), num_lines)
#     # all_lines += num_lines
#
# print(all_lines -len(pathlist) )
