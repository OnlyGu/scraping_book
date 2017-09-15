import requests
from cachecontrol import CacheControl


session = requests.session()
cached_session = CacheControl(session) # sessionをラップしたcached_sessionを作る

# 1回目はキャッシュがないので、サーバーから取得しキャッシュする
response = cached_session.get('https://docs.python.org/3/')
print(response.from_cache) # False

# 2回目はETagとLase-Modifiedの値を使って更新されているかをかくにんする
# 更新されていない場合のコンテンツはキャッシュから取得するので高速に処理できる
response = cached_session.get('https://docs.python.org/3/')
print(response.from_cache) # True