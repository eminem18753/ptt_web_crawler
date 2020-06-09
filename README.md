ptt beauty版網路爬蟲 <br /><br />

Part 1.Installed module:<br />
1.requests <br />
2.requests_html <br />
3.lxml <br />
4.PyQuery <br />
5.beautifulsoup4 (bs4) <br />
6.urllib <br />
7.time <br />
8.requests.packages.urllib3 <br />

Part 2.環境: <br />
windows 10+python 3.6 (anaconda spyder) <br />

Part 3.注意事項: <br />
對於每一個function都有計時器，會print出總執行時間(單位:秒) <br />

Part 4.執行方法: <br />
1.python web_crawler.py crawl <br />
->爬下2020年到現在的所有ptt beauty版文章連結，存到all_articles.txt。並將其中所有熱門文章存入all_popular.txt <br />
2.python web_crawler.py push start_date end_date (eg.python web_crawler.py push 304 609) <br />
->數推文和噓文並找出前10名最會推跟噓的人(304代表3月4日，1020代表6月9日) <br />
3.python web_crawler.py crawl popular start_date end_date (eg.python web_crawler.py popular 304 609) <br />
->找爆文和圖片URL，並將結果輸出txt檔 <br />
4.python web_crawler.py crawl keyword {keyword} start_date end_date (eg.python web_crawler.py keyword 正妹 304 609) <br />
->找內文中含有{keyword}的文章中的所有圖片 <br />
