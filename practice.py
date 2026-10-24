# 練習問題
# http://abehiroshi.la.coocan.jp/movie/eiga.htm のページから出演映画のタイトルを取得する。

# --- ライブラリの読み込み ---
import requests                # Webページを取得するためのライブラリ
from bs4 import BeautifulSoup  # HTMLを解析するためのライブラリ
import csv                     # CSVファイルを書き出すための標準ライブラリ

# --- 取得先のURLとヘッダーの設定 ---
url = "http://abehiroshi.la.coocan.jp/movie/eiga.htm"
header = {
  # ブラウザからのアクセスに見せかけるための User-Agent
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# --- ページの取得 ---
res = requests.get(url, headers=header)  # GETリクエストを送信
res.encoding = 'cp932'                   # 文字化け対策：Shift_JIS系の文字コードを指定
                                         # （res.apparent_encoding でも可だが、まれに外れる）

# --- HTMLの解析 ---
# res.text を渡す（res.content だと上のencoding設定が反映されない）
html_soup = BeautifulSoup(res.text, 'html.parser')

# --- 取得したHTMLをファイルに保存（確認用） ---
# print(f'レスポンスボディ: {res.text}')   # 画面に出力したいときはこの行を有効にする
with open('abehiroshi.html', 'w', encoding='utf-8') as f:
  f.write(res.text)                        # UTF-8で保存（開いたときに文字化けしないように）

# --- 映画タイトルの抽出 ---
titles = []  # タイトルを入れるリスト

# border="1" のテーブル（映画一覧のテーブル）だけを対象にする
for table in html_soup.find_all('table', border="1"):
    for tr in table.find_all('tr'):    # テーブルの各行を順に処理
        tds = tr.find_all('td')        # その行のセル（列）をすべて取得
        if len(tds) >= 2:              # 2列以上ある行だけ処理（列が足りない行を除外）
            # 2列目（インデックス1）がタイトル。前後の空白は strip=True で除去
            title = tds[1].get_text(strip=True)
            if title:                  # 空文字でなければリストに追加
                titles.append(title)

# --- 結果の表示 ---
for t in titles:
    print(t)                           # タイトルを1件ずつ出力
print(f'合計: {len(titles)}件')        # 取得できた件数を出力

# --- CSVファイルへの保存 ---
# utf-8-sig：Excelで開いても文字化けしない形式
# newline=''：Windowsで空行が入るのを防ぐ
with open('movies.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)             # CSV書き込み用オブジェクトを作成
    writer.writerow(['title'])         # 1行目：ヘッダー（列名）
    for t in titles:
        writer.writerow([t])           # タイトルを1行ずつ書き込む
