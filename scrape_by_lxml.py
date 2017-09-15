import lxml.html

# htmlファイルを読み込み、getroot()メソッドでhtmlelementオブジェクトを得る
tree = lxml.html.parse('index.html')
html = tree.getroot()

# cssselect()メソッドでa要素のリストを取得して、個々のa要素に対して処理を行う
for a in html.cssselect('a'):
	# href属性とリンクのテキストを取得して表示する
	print(a.get('href'), a.text)