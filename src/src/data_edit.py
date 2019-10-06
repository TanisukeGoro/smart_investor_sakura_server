"""
有価証券報告書以外は削除する
実際はgetBooksIndex.pyを修正したのでもう使用しないと思う。
"""

import pandas as pd
import sys
import os


def clear_others(file_name):
    df_index = pd.read_csv(file_path+'.csv', header=0,index_col=0)
    # 有価証券報告書をdocuDescriptionに含まないrowを取得
    # print(df_index.query('docDescription.str.match("[^有価証券報告書]")', engine='python'))
    out = df_index.query('docDescription.str.match("有価証券報告書")', engine='python')
    out = out.reset_index(drop=True)
    out.to_csv(file_path+'_有報のみ.csv')

# df_index.drop(df_index.query('docDescription.str.match("[^有価証券報告書]")', engine='python'))

if __name__ == "__main__":
    sys.argv.pop(0)
    file_path = sys.argv[0]
    file_path = os.path.splitext(file_path)[0]
    clear_others(os.path.basename(file_path))
