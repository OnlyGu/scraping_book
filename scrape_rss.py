from xml.etree import ElementTree

# parse()関数でファイルを読み込んでElementTreeオブジェクトを得る
tree = ElementTree.parse('rss2.xml')
# getroot()メソッドでxmlのルート要素に対応するElementオブジェクトを得る
root = tree.getroot()

for item in root.findall('channel/item'):
	title = item.find('title').text
	url = item.find('link').text
	print(url, title)
	