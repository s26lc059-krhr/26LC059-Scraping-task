# 個別課題
# 武蔵野大学のWebサイトのサイトマップを抽出する

import csv
import time
from collections import deque
from urllib.parse import urljoin, urldefrag, urlparse

import requests
from bs4 import BeautifulSoup

URL = "https://www.musashino-u.ac.jp/"
ALLOWED_NETLOC = urlparse(URL).netloc
SLEEP_SEC = 1
MAX_PAGES = 20  # 測試用，確認沒問題後改成 None
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
SKIP_EXT = (".pdf", ".jpg", ".jpeg", ".png", ".gif", ".svg", ".zip",
            ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".mp4", ".mp3")

respon = requests.get(URL, headers=HEADERS)
respon.encoding = respon.apparent_encoding
with open('musashino.html', 'w', encoding='utf-8') as f:
  f.write(respon.text)    


sitemap = {}
visited = {URL}
queue = deque([URL])

while queue:
    if MAX_PAGES is not None and len(sitemap) >= MAX_PAGES:
        break

    url = queue.popleft()

    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
    except requests.exceptions.RequestException as e:
        print(f"取得失敗: {url} ({e})")
        time.sleep(SLEEP_SEC)
        continue

    if "text/html" not in res.headers.get("Content-Type", ""):
        time.sleep(SLEEP_SEC)
        continue

    res.encoding = res.apparent_encoding
    soup = BeautifulSoup(res.text, "html.parser")

    title = soup.title.get_text(strip=True) if soup.title else ""
    sitemap[url] = title
    print(f"[{len(sitemap)}] {url} : {title}")

    for a in soup.find_all("a", href=True):
        link, _ = urldefrag(urljoin(url, a["href"]))
        parsed = urlparse(link)
        if parsed.scheme not in ("http", "https"):
            continue
        if parsed.netloc != ALLOWED_NETLOC:
            continue
        if parsed.path.lower().endswith(SKIP_EXT):
            continue
        if link in visited:
            continue
        visited.add(link)
        queue.append(link)

    time.sleep(SLEEP_SEC)

with open("sitemap.csv", "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["url", "title"])
    for url, title in sitemap.items():
        writer.writerow([url, title])

print(f"完了: {len(sitemap)}ページ")
