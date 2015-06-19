import sys
import os
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

import requests
from urllib import request
import re
from extractors.youku import YouKu

def get_tudou_vcode(url):
	# headers = {'User-Agent' : user_agent}
	req = request.Request(url)
	my_response = request.urlopen(req)
	my_page = my_response.read()

	unicode_page = my_page.decode("utf-8")
	vcode_re = re.search(r'vcode\s*[:=]\s*\'([^\']+)\'', unicode_page)

	if vcode_re:
		return vcode_re.group(1)


def getVideoObject(video_url=None, user_agent=None):
	"""
	土豆的视频处理 
	这是土豆直接解析地址，不分格式:
	http://cnc.v2.tudou.com/f?id=233753311
	"""

	video_url0 = 'http://www.tudou.com/albumplay/yKNjP5Tg2I8/9tOwnCJnATQ.html' # 测试用，正式发布需要删除

	if video_url:
		video_url0 = video_url+'&'

	user_agent0 = 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Mobile/12F70 MicroMessenger/6.2 NetType/WIFI Language/zh_CN'
	if user_agent:
		user_agent0 = user_agent

	try:
		vcode = get_tudou_vcode(video_url0)
		if vcode:
			youku_obj = YouKu(video_url="http://v.youku.com/v_show/id_%s.html" % vcode)
			video_json_dict = youku_obj.getYouKuUrl()
			video_json_dict['type'] = "土豆"
			return {'code': 0, 'video':video_json_dict}
		else:
			{'code': -1, 'msg':'不支持解析'}
	except Exception as e:
		return {'code': -1, 'msg':'抓取视频出错'}

	return {'code': -1, 'msg':'没有抓取到视频地址'}

if __name__ == "__main__":
	# get_tudou_vcode("http://www.tudou.com/albumplay/yKNjP5Tg2I8/9tOwnCJnATQ.html")
	print(getVideoObject())
