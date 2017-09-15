import sys
import os

from robobrowser import Robobrowser

# 認証の情報は環境変数から取得する
AMAZON_EMAIL = os.environ['AMAZON_EMAIL']
AMAZON_PASSWORD = os.environ['AMAZON_PASSWORD']

# RoboBrowserオブジェクトを作成する
browser = Robobrowser(
	parser = 'html.parser', # Beautiful Soupで使用するパーサーを指定する
	# Cookieが使用できないと表示されてログインできない問題を回避するため、
	# 通常のブラウザのUser-Agent(ここではFirefoxのもの)を使う
	user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:45.0) Gecko/20100101 Firefox/45.0'
	)


def main():
	# 注文履歴のページを開く
	print('Navigating...', file=sys.stderr)
	browser.open('https://www.amazon.co.jp/gp/css/order-history')

	# サインインページにリダイレクトされていることを確認する
	assert 'Amazonサインイン' in browser.parsed.title.string

	# name="signIn"というサインインフォームを埋める
	# フォームのname属性の値はブラウザの開発者ツールで確認できる

	# 途中




def print_order_history():


if __name__ == '__main__':
		main()	