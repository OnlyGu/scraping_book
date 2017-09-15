# coding: utf-8

# MongoDBを起動してから実行
# sudo mongod --dbpath /data/db

import time # timeモジュールをインポート
import re # reモジュールをインポート

import requests
import lxml.html
from pymongo import MongoClient

def main():
	"""
	クローラのメイン処理
	"""
	client = MongoClient('localhost', 27017) # ローカルホストのMongoDBに接続する
	collection = client.scraping.ebooks # scrapingデータベースのebooksコレクションを得る
	# データを一意に識別するキーを格納するkeyフィールドにユニークなインデックスを作成する
	collection.create_index('key', unique=True)

	response = requests.get('https://gihyo.jp/dp') # 一覧ページを取得する
	# scrape_list_page()関数を呼び出し、ジェネレータイテレータを取得する
	urls = scrape_list_page(response) # 詳細ページのurl一覧を取得する
	for url in urls: # ジェネレータイテレータはlistなどと同様に繰り返し使用可能
		key = extract_key(url) # URLからキーを取得する

		ebook = collection.find_one({'key': key}) # MongoDBからkeyに該当するデータを探す
		if not ebook: # ebookに存在しない場合だけ、詳細ページをクロールする
			time.sleep(1)
			response = requests.get(url) # Sessionを使って詳細ページを取得する
			ebook = scrape_detail_page(response) # 詳細ページからスクレイピングして電子書籍の情報を得る
			collection.insert_one(ebook) # 電子書籍の情報をMongoDBに保存する

		print(ebook) # 電子書籍の情報を表示する


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
	    'key': extract_key(response.url), # URLから抜き出したキー
	    'title': root.cssselect('#bookTitle')[0].text_content(), # タイトル
	    'price': root.cssselect('.buy')[0].text, # 価格(.textで直接の子である文字列のみを取得)
	    'content': [normalize_spaces(h3.text_content()) for h3 in root.cssselect('#content > h3')], # 目次
	}
	return ebook # dictを返す


def extract_key(url):
	"""
	urlからキー（urlの末尾のISBN）を抜き出す
	"""
	m = re.search(r'/([^/]+)$', url)
	return m.group(1)

def normalize_spaces(s):
	"""
	連続する空白を1つのスペースに置き換え、前後の空白は削除した新しい文字列を取得する
	"""
	return re.sub(r'\s+',' ', s).strip()


if __name__ == '__main__':
	main()

