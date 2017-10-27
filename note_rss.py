import sys
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import feedgenerator


def main():
    """
    メインの処理
    """

    driver = webdriver.PhantomJS() # PhantomJSのWebDriverオブジェクトを作成する
    driver.set_window_size(800, 600) # ウィンドウサイズを設定する

    navigate(driver) # noteのトップページに遷移する
    posts = scrape_posts(driver) # 文章コンテンツのリストを取得する

    # RSSフィードとして保存する
    with open('recomend.rss', 'w') as f:
        save_as_feed(f, posts)


def save_as_feed(f, posts):
    """
    文章コンテンツのリストをフィードとして保存する
    """

    # フィードを表すRss201rev2Feedオブジェクトを作成する
    feed = feedgenerator.Rss201rev2Feed(
        title='おすすめノート', # フィードのタイトル
        link='https://note.mu/', # フィードに対応するWebサイトのURL
        description='おすすめノート' # フィードの概要
        )

    for post in posts:
        # フィードにアイテムを追加する
        # キーワード引数unique_idは、アイテムを一位に識別するユニークなIDを指定する
        # 必須ではないが、このIDを指定しておくとRSSリーダーがアイテムの重複なく扱える
        # 可能性が高まるので、ここではコンテンツのURLを指定している

        feed.add_item(title=post['title'], link=post['url'],
            description=post['description'], unique_id=post['url'])


    feed.write(f, 'utf-8') # ファイルオブジェクトに書き込む。第2引数にエンコーディングを指定する


if __name__ == '__main__':
    main()