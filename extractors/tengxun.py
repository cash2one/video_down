import sys
import os
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from urllib import request
import requests
import json
import re

def getVideoObject(video_url=None, user_agent=None):
	"""
	腾讯的视频处理 , 待续
	这是一个包含视频的封面和title的地址：
	http://ncgi.video.qq.com/tvideo/fcgi-bin/vp_iphone?plat=2&otype=json&vid=x0016kc6wor
	is_user_agent:参数默认pc，为client表示客户端
	"""

	video_url0 = 'http://m.v.qq.com/play/play.html?coverid=fb67wf0ood33ubp&vid=x0016kc6wor&type=5&noright=0&protype=3&charge=0&ptag=4_4.0.2.8756_wxf' # 测试用，正式发布需要删除


	tengxun_get_url = 'http://vv.video.qq.com/geturl?vid=%s&otype=xml&platform=1'
	tengxun_get_info = 'http://vv.video.qq.com/getinfo?otype=xml&vid=%s'

	video_vid_value = '' # 视频的vid
	video_url_value = '' # 存储视频地址
	video_name = '' # 视频名称
	video_poster = 'http://shp.qpic.cn/qqvideo_ori/0/%s_496_280/0' # 视频封面

	if video_url:
		video_url0 = video_url+'&'

	user_agent0 = 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Mobile/12F70 MicroMessenger/6.2 NetType/WIFI Language/zh_CN'
	if user_agent:
		user_agent0 = user_agent

	video_vid_re = re.findall('vid=(.*?)&', video_url0)

	if video_vid_re is not None and len(video_vid_re) > 0:
		video_vid_value = video_vid_re[0] # 取出url中的vid

		response = requests.get(tengxun_get_url % video_vid_value)

		response_video_name_xml = requests.get(tengxun_get_info % video_vid_value)
		video_name_re = re.findall('<ti>(.*?)</ti>', response_video_name_xml.text)
		if video_name_re and len(video_name_re) > 0:
			video_name = video_name_re[0]

		# print(jsonpickle.encode({"code":response.status_code, "msg": response.text}))
		if response is not None and response.status_code == 200:
			response_urls = re.findall('<url>(.*?)</url>', response.text)
			if response_urls:
				video_url_value = response_urls[0]

				return {'code': 0, 'video': {'video_url' : video_url_value, 'video_poster' : video_poster % video_vid_value, 'name': video_name, "type": "腾讯"}}

	return {'code': -1, 'msg':'没有抓取到视频地址'}

if __name__ == "__main__":
	print(getVideoObject())


