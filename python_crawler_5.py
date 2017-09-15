import re # reモジュールをインポート

import requests
import lxml.html

def main():
	"""
	クローラのメイン処理
	"""
	session = requests.Session() # 複数のページをクロールするのでSessionを使う
	response = requests.get('https://gihyo.jp/dp')
	# scrape_list_page()関数を呼び出し、ジェネレータイテレータを取得する
	urls = scrape_list_page(response)
	for url in urls: # ジェネレータイテレータはlistなどと同様に繰り返し使用可能
	    response = session.get(url) # Sessionを使って詳細ページを取得する
	    ebook = scrape_detail_page(response) # 詳細ページからスクレイピングして電子書籍の情報を得る
	    print(ebook) # 電子書籍の情報を表示する
	    break # まず1ページだけで試すため、break分でループを抜ける


def scrape_list_page(response):
	"""
	一覧ページのResponseから詳細ページのURLを抜き出すジェネレータ関数
	"""
	root = lxml.html.fromstring(response.content)
	root.make_links_absolute(response.url) # すべてのリンクを絶対URLに変換する

	# id="listBook"である要素の子孫のa要素のみを取得する
	for a in root.cssselect('#listBook a[itemprop="url"]'):
		url = a.get('href')
		yield url # yield文でジェネレータイテレータの要素を返す


def scrape_detail_page(response):
	"""
	詳細ページのResponseから電子書籍の情報をdictで取得する
	"""
	root = lxml.html.fromstring(response.content)
	ebook = {
	    'url': response.url, # URL
	    'title': root.cssselect('#bookTitle')[0].text_content(), # タイトル
	    'price': root.cssselect('.buy')[0].text, # 価格(.textで直接の子である文字列のみを取得)
	    'content': [normalize_spaces(h3.text_content()) for h3 in root.cssselect('#content > h3')], # 目次
	}
	return ebook # dictを返す


def normalize_spaces(s):
	"""
	連続する空白を1つのスペースに置き換え、前後の空白は削除した新しい文字列を取得する
	"""
	return re.sub(r'\s+',' ', s).strip()


if __name__ == '__main__':
	main()

