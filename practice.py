# 練習問題
# http://abehiroshi.la.coocan.jp/movie/eiga.htm のページから出演映画のタイトルを取得する。

import requests
from bs4 import BeautifulSoup

url = "http://abehiroshi.la.coocan.jp/movie/eiga.htm"
header = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}
res = requests.get(url, headers=header)
res.encoding = res.apparent_encoding

html_soup = BeautifulSoup(res.content, 'html.parser')

# print(f'レスポンスボディ: {res.text}')
with open('abehiroshi.html', 'w', encoding='utf-8') as f:
  f.write(res.text)

titles = []
for table in html_soup.find_all('table', border="1"): 
    for tr in table.find_all('tr'):
        tds = tr.find_all('td')
        if len(tds) >= 2:
            title = tds[1].get_text(strip=True)
            if title:
                titles.append(title)

for t in titles:
    print(t)
print(f'合計: {len(titles)}件')
