import requests
from bs4 import BeautifulSoup
import time

url = 'https://www.musashino-u.ac.jp'

# これからアクセスするURLのリスト
url_list = [url]

# URLをキー、ページタイトルを値として保存する辞書
site_map = {}

# url_listに新しいURLを追加すると、順番に巡回できる
for url in url_list:
    # 連続アクセスを避ける
    time.sleep(1)
    print('アクセス中：', url)

    try:
        res = requests.get(url, timeout=15)
        res.encoding = 'utf-8'
    except requests.exceptions.RequestException as e:
        print('通信エラー：', e)
        continue

    print(f"ステータスコード：{res.status_code}")
    print(f"ステータスメッセージ：{res.reason}")

    # HTMLのソースコードをBeautifulSoupオブジェクトに変換する処理
    html_soup = BeautifulSoup(res.content, 'html.parser')
    print("html_soupの型：{type(html_soup)}")

    # <title>タグの文字列を辞書に格納する
    title = html_soup.find('title')

    # URLとタイトルを辞書に保存
    if title is not None:
        site_map[url] = title.text.strip()
        print('タイトル：', title.text.strip())

    # <a>タグのリンク先をすべて調べる
    a_list = html_soup.find_all('a')
    for a in a_list:
        href = a.get('href')

        # リンク先（href）が存在する場合のみ処理実行
        if href is not None:
            # 相対URLを絶対URLに変換
            next_url = requests.compat.urljoin(url, href)

            # リンク先が武蔵野大学のWebサイト内かどうかを確認
            if next_url.startswith('https://www.musashino-u.ac.jp/'):
                # 取得したURLが、まだurl_listに登録されていないか確認
                if next_url not in url_list:
                    # 重複していないURLをリストに追加し、次の巡回対象にする
                    url_list.append(next_url)

# 辞書の結果をCSVに保存する
with open('sitemap.csv', 'w', encoding='utf-8-sig') as f:
    f.write('URL,Title\n')
    for url, title in site_map.items():
        # カンマやダブルクォーテーションを含むタイトルでもCSV形式で保存できる
        url = url.replace('"', '""')
        title = title.replace('"', '""').replace('\n', ' ').replace('\r', ' ')
        f.write(f'"{url}","{title}"\n')

print('sitemap.csv に保存しました')