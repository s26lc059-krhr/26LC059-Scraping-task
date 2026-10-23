# 練習問題
# http://abehiroshi.la.coocan.jp/movie/eiga.htm のページから出演映画のタイトルを取得する。

import requests
from bs4 import BeautifulSoup

url = "http://abehiroshi.la.coocan.jp/movie/eiga.htm"
res = requests.get(url)

print(f'レスポンス: {res}')
print(f'レスポンスの型: {type(res)}')

html_soup = BeautifulSoup(res.content, 'html.parser')
print(f'html_soupの型: {type(html_soup)}')

