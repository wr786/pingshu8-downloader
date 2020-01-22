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
	downloadUrl = downloadUrl[:-6] # Unsafe!
	prefix = 'https://www.'
	suffix = '.htm'

	pagesStr = input("请输入恁要下载的有声小说的详情页的起始与结束页数(示例: 1 8)：\n>>> ")
	try:
		pages = pagesStr.split(' ')
		startPage = int(pages[0])
		endPage = int(pages[1])
	except Exception as e:
		print('[ERROR] 请按正确格式输入页码! ' + e)
	except StandardError as e:
		print('[ERROR] 请按正确格式输入页码! ' + e)

	fileName = (input("请输入恁想要保存下载链接的文件名(示例: 文学少女)：\n>>> "))
	print("[Start] Processing...")
	startTime = time.time()

	option = webdriver.ChromeOptions()
	option.add_argument('disable-infobars')
	abspath = os.path.join(os.path.abspath('.'), 'chromedriver.exe')
	browser = webdriver.Chrome(abspath)

	f = open('.\\output\\' + fileName + '_' + str(startPage) + '_' + str(endPage) + '.txt', 'w')
	downloadPageLst = []

	for i in range(startPage, endPage):
		try:
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
		except Exception as e:
			print("[ERROR] 第" + str(i) + '页处理失败: ' + e)

	for idx, page in enumerate(downloadPageLst):
		try:
			print("[Simulating] 正在模拟点击中...第" + str(idx+1) + "集")
			browser.get(page)
			downloadButton = browser.find_element_by_xpath('//*[@id="clickina"]/img')
			downloadButton.click()
			browser.switch_to.window(browser.window_handles[1])
			f.write(browser.current_url + '\n')
			browser.close()
			browser.switch_to.window(browser.window_handles[0])
		except Exception as e:
			print("[ERROR] 第" + str(i) + "集获取出现异常: " + e)

	browser.quit()
	f.close()

	endTime = time.time()
	print("[End] 在" + str(endTime - startTime) + 's内爬取完成！')