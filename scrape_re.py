import re
from html import unescape

# 前節でDLしたファイルを開き、中身を変数htmlに格納する
with open('dp.html') as f:
	html = f.read()

# re.findall()を使って書籍1冊分に相当する部分のhtmlを取得する
for partial_html in re.findall(r'<a itemprop="url".*?</ul>\s*</a></li>', html, re.DOTALL):
	url = re.search(r'<a itemprop="url" href="(.*?)">', partial_html).group(1)
	url = 'http://sample.scraping-book.com' + url

	title = re.search(r'<p itemprop="name".*?</p>', partial_html).group(0)
	title = title.replace('<br/>', ' ')
	title = re.sub(r'<.*?>', '', title)
	title = unescape(title)

	print(url, title)