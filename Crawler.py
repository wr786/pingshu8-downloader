# -*- coding:utf-8 -*-
# author: wr786
import urllib.request
import re
import time
import os
from selenium import webdriver

def DEBUG(x):
	print('[Debug] ' + str(x))

if __name__ == '__main__':

	if not os.path.exists('output'):
		os.mkdir('output')

	baseUrl = 'pingshu8.com'
	downloadUrl = input("请输入恁要下载的有声小说的详情页:\n>>> ")
	downloadUrl = downloadUrl[:-6]
	prefix = 'https://www.'
	suffix = '.htm'
	pages = int(input("请输入恁要下载的有声小说的详情页总页数：\n>>> "))
	print("[Start] Processing...")
	startTime = time.time()

	option = webdriver.ChromeOptions()
	option.add_argument('disable-infobars')
	abspath = os.path.join(os.path.abspath('.'), 'chromedriver.exe')
	browser = webdriver.Chrome(abspath)

	f = open(r'.\output\links.txt', 'w')
	downloadPageLst = []

	for i in range(1, pages+1):
		url = downloadUrl + '_' + str(i) + suffix
		print("[Crawling] 正在处理第" + str(i) + '页...')
		# response = urllib.request.urlopen(url)
		# data = response.read().decode('gb2312', 'ignore')
		browser.get(url)
		data = browser.page_source.encode('UTF-8').decode()
		pattern = re.compile(r'<li class="a2"><a href="(.*?)" target="_blank">')
		items = re.findall(pattern, data)
		for item in items:
			downloadPageLst.append(prefix + baseUrl + item)
			# f.write(baseUrl + item + '\n')

	for idx, page in enumerate(downloadPageLst):
		print("[Simulating] 正在模拟点击中...第" + str(idx+1) + "集")
		browser.get(page)
		downloadButton = browser.find_element_by_xpath('//*[@id="clickina"]/img')
		downloadButton.click()
		browser.switch_to.window(browser.window_handles[1])
		f.write(browser.current_url + '\n')
		browser.close()
		browser.switch_to.window(browser.window_handles[0])

	browser.quit()
	f.close()

	endTime = time.time()
	print("[End] 在" + str(endTime - startTime) + 's内爬取完成！')