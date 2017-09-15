from bs4 import BeautifulSoup
import lxml

# htmlファイルを読み込んでBeautifulSoupオブジェクトを得る
# 第二引数はパーサの指定、html.parserは追加のライブラリが不要、lxmlは高速、html5libはHTML5の仕様通りにパースできる
with open('index.html') as f:
	soup = BeautifulSoup(f, 'lxml')

# find_all()メソッドでa要素のリストを取得して、個々のa要素に対して処理を行う
for a in soup.find_all('a'):
	print(a.get('href'), a.text)