# -*- coding: utf-8 -*-

"""
__title__ = ''
__author__ = 'MoTuii'
__mtime__ = '2017/10/1'
# code is far away from bugs with the god animal protecting
I love animals. They taste delicious.

 ┏┓   ┏┓
┏┛┻━━━┛┻┓
┃   ☃   ┃
┃ ┳┛ ┗┳ ┃
┃   ┻   ┃
┗━┓   ┏━┛
  ┃   ┗━━━┓
  ┃神兽保佑 ┣┓
  ┃永无BUG！┏┛
  ┗┓┓┏━ ┳┓┏┛
   ┃┫┫  ┃┫┫
   ┗┻┛  ┗┻┛
"""
import re
import urllib2
from json import loads
# 设置系统默认编码为utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def getUrlList():
	# 获取淘女郎主页信息
	html = urllib2.urlopen('https://mm.taobao.com/tstar/search/tstar_model.do?_input_charset=utf-8')
	html = html.read().decode('GBK').encode('utf-8')
	# print html
	return loads(html)['data']['searchDOList']

def getAlbumList(user_id):
	# 获取相册信息
	html = urllib2.urlopen('https://mm.taobao.com/self/album/open_album_list.htm?_charset=utf-8&user_id%20={}'.format(user_id)).read()
	html = html.decode('gbk').encode('utf-8')

	# 获取相册链接
	reg = r'<a class="mm-first" href="(.*?)" target="_blank">'
	albumList = re.findall(reg,html)
	return albumList

def getPhoto(user_id,album_id):
	# 获取照片链接
	html = urllib2.urlopen('https://mm.taobao.com/album/json/get_album_photo_list.htm?user_id={}&album_id={}&top_pic_id=0&cover=%2F%2Fimg.alicdn.com%2Fimgextra%2Fi2%2F176817195%2FTB1i8OAKXXXXXXUXpXXXXXXXXXX_!!0-tstar.jpg&page=1&_ksTS=1506857619298_187&callback='.format(user_id,album_id)).read().decode('gbk').encode('utf-8')
	# print html
	return loads(html)['picList']

if __name__ == "__main__":
	for user_info in getUrlList():#获取模特ID
		# 姓名和身高
		print user_info
		user_name = user_info['realName']
		user_id = user_info['userId']
		user_city = user_info['city']
		user_height = user_info['height']
		user_weight = user_info['weight']
		albumList = getAlbumList(user_id)#获取相册ID

		# 下载淘女郎信息
		with open("D:\mm_taobao\{}.txt".format(user_name).decode('utf-8').encode('gbk'),'wb')as f:
			str_info = '姓名:{}\t身高:{}体重:{}\t城市:{}'.format(user_name,user_height,user_weight,user_city)+str(user_info).encode('utf-8')
			# print str_info

			# 写入信息
			f.write(str_info)
			f.flush()

		# 下载照片
		for album_url in albumList[::2]:
			temp_index = album_url.find('album_id=')
			start_index = temp_index + len('album_id=')
			end_index = album_url.find('&',start_index)
			album_id = album_url[start_index:end_index]
			photoList = getPhoto(user_id,album_id)
			count = 0
			for photo_info in photoList:
				picUrl = 'http:'+photo_info['picUrl']
				start_index = picUrl.find('http:')
				end_index = picUrl.find('tstar.') + 9
				picUrl = picUrl[start_index:end_index]
				# print picUrl
				try:
					# 下载图片
					photo_data = urllib2.urlopen(picUrl)
				finally:
					pass
				# print photo_data

				# 保存图片
				with open('D:\mm_taobao\pic_data\{}{}{}.jpg'.format(user_name,album_id,count).decode('utf-8').encode('gbk'),'wb') as f:
					f.write(photo_data.read())
					f.flush()

				count += 1








