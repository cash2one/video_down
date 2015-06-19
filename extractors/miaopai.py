import sys
import os
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from urllib import request
import re

"""秒拍的视频处理"""
def getVideoObject(video_url=None, user_agent=None):
	"""
	is_user_agent:参数默认pc，为client表示客户端
	"""
	video_url0 = 'http://miaopai.com/show/5LPgnn12nqst7IoBAHCN1Q__.htm' # 测试用，正式发布需要删除
	if video_url:
		video_url0 = video_url

	user_agent0 = 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Mobile/12F70 MicroMessenger/6.2 NetType/WIFI Language/zh_CN'
	if user_agent:
		user_agent0 = user_agent

	try:
		headers = {'User-Agent' : user_agent0}
		req = request.Request(video_url0, headers = headers)
		my_response = request.urlopen(req)

		my_page = my_response.read()

		unicode_page = my_page.decode("utf-8")
		# print(unicode_page)

		title_search = re.search('<title>.*?</title>', unicode_page)

		video_name = "" # 视频名称
		if title_search :
			title_value_re = re.findall('<title>(.*?)</title>', title_search.group())
			if title_value_re is not None and len(title_value_re) > 0:
				video_name = title_value_re[0]

		result_search = re.search('<video.*?</video>', unicode_page)

		if result_search:
			video_str = result_search.group()
			video_src = re.findall("src=\'(.*?)\'", video_str)
			video_poster = re.findall("poster=\'(.*?)\'", video_str)
			video_src_value = ''
			video_poster_value = ''
			if video_src is not None and len(video_src) > 0:
				video_src_value = video_src[0]

			if video_poster is not None and len(video_poster) > 0:
				video_poster_value = video_poster[0]

			return {'code': 0, 'video': {'video_url' : video_src_value, 'video_poster' : video_poster_value, 'name': video_name, 'type': "秒拍"}}

	except Exception as e:
		return {'code': -1, 'msg':'抓取视频出错'}

	return {'code': -1, 'msg':'没有抓取到视频地址'}

if __name__ == "__main__":
	print(getVideoObject())
		