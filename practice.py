# 練習問題
# http://abehiroshi.la.coocan.jp/movie/eiga.htm のページから出演映画のタイトルを取得する。

import requests

url = "http://abehiroshi.la.coocan.jp/movie/eiga.htm"
res = requests.get(url)

print(f'レスポンス: {res}')
print(f'レスポンスの型: {type(res)}')
