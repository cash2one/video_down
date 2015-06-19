from flask import Flask, request as flask_request
from flask.ext import restful
from urllib import request
import requests
import json
import jsonpickle
import re
import youku

app = Flask(__name__)
api = restful.Api(app)

class MiaoPai(restful.Resource):
	"""秒拍的视频处理"""
	def get(self, is_user_agent="pc"):
		"""
		is_user_agent:参数默认pc，为client表示客户端
		"""
		video_url = 'http://miaopai.com/show/5LPgnn12nqst7IoBAHCN1Q__.htm' # 测试用，正式发布需要删除
		if 'video_url' in flask_request.args and flask_request.args['video_url'] is not None:
			print(flask_request.args['video_url'])
			video_url = flask_request.args['video_url']

		myUrl = video_url
		user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Mobile/12F70 MicroMessenger/6.2 NetType/WIFI Language/zh_CN'
		if is_user_agent is not None and is_user_agent == "client":
			user_agent = flask_request.headers["User-Agent"]

		try:
			headers = {'User-Agent' : user_agent}
			req = request.Request(myUrl, headers = headers)
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

				return {'code': 0, 'video': {'video_url' : video_src_value, 'video_poster' : video_poster_value, 'name': video_name}}

			# print(flask_request.headers["User-Agent"])
		except Exception as e:
			return {'code': -1, 'msg':'抓取视频出错'}

		return {'code': -1, 'msg':'没有抓取到视频地址'}

class MeiPai(restful.Resource):
	"""美拍的视频处理"""
	def get(self, is_user_agent="pc"):
		"""
		is_user_agent:参数默认pc，为client表示客户端
		"""

		video_url = 'http://www.meipai.com/media/306869935' # 测试用，正式发布需要删除

		if 'video_url' in flask_request.args and flask_request.args['video_url'] is not None:
			print(flask_request.args['video_url'])
			video_url = flask_request.args['video_url']

		myUrl = video_url
		user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Mobile/12F70 MicroMessenger/6.2 NetType/WIFI Language/zh_CN'
		if is_user_agent is not None and is_user_agent == "client":
			user_agent = flask_request.headers["User-Agent"]

		try:
			headers = {'User-Agent' : user_agent}
			req = request.Request(myUrl, headers = headers)
			my_response = request.urlopen(req)

			my_page = my_response.read()

			unicode_page = my_page.decode("utf-8")

			title_search = re.search('<title>.*?</title>', unicode_page)
			video_name = "" # 视频名称
			if title_search :
				title_value_re = re.findall('<title>(.*?)</title>', title_search.group())
				if title_value_re is not None and len(title_value_re) > 0:
					video_name = title_value_re[0]

			result_search = re.search('data-video=.*?</div>', unicode_page, re.S)

			if result_search:
				video_str = result_search.group()
				video_src = re.findall("data-video=\"(.*?)\"", video_str)
				video_poster = re.findall('<img.*?id="fVideoImg".*?src=\"(.*?)\"', video_str)
				video_src_value = ''
				video_poster_value = ''
				if video_src is not None and len(video_src) > 0:
					video_src_value = video_src[0]

				if video_poster is not None and len(video_poster) > 0:
					video_poster_value = video_poster[0]

				return {'code': 0, 'video': {'video_url' : video_src_value, 'video_poster' : video_poster_value, 'name': video_name}}

		except Exception as e:
			return {'code': -1, 'msg':'抓取视频出错'}

		return {'code': -1, 'msg':'没有抓取到视频地址'}

class WeiBoShiPin(restful.Resource):
	"""微搏的视频处理 , 待续"""
	def get(self, is_user_agent="pc"):
		"""
		is_user_agent:参数默认pc，为client表示客户端
		"""

		video_url = 'http://m.weibo.cn/1644114654/3833409439019809/weixin?wm=3333_2001&sourcetype=weixin&from=singlemessage&isappinstalled=1' # 测试用，正式发布需要删除

		if 'video_url' in flask_request.args and flask_request.args['video_url'] is not None:
			print(flask_request.args['video_url'])
			video_url = flask_request.args['video_url']

		myUrl = video_url
		user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Mobile/12F70 MicroMessenger/6.2 NetType/WIFI Language/zh_CN'
		if is_user_agent is not None and is_user_agent == "client":
			user_agent = flask_request.headers["User-Agent"]

		try:
			headers = {'User-Agent' : user_agent}
			req = request.Request(myUrl, headers = headers)
			my_response = request.urlopen(req)

			my_page = my_response.read()

			unicode_page = my_page.decode("utf-8")

			print(unicode_page)
			return {"msg":"测试"}

			# todo : 新浪视频需要时再研究

			# result_search = re.search('\"h5_url\":\".*?\",', unicode_page, re.S)

			# print(result_search.group())
			# return {"msg":"测试"}

			# if result_search:
			# 	video_str = result_search.group()
			# 	video_src = re.findall("data-video=\"(.*?)\"", video_str)
			# 	video_poster = re.findall('<img.*?id="fVideoImg".*?src=\"(.*?)\"', video_str)
			# 	video_src_value = ''
			# 	video_poster_value = ''
			# 	if video_src is not None and len(video_src) > 0:
			# 		video_src_value = video_src[0]

			# 	if video_poster is not None and len(video_poster) > 0:
			# 		video_poster_value = video_poster[0]

			# 	return {'video_url' : video_src_value, 'video_poster' : video_poster_value}

		except Exception as e:
			return {'code': -1, 'msg':'抓取视频出错'}

		return {'code': -1, 'msg':'没有抓取到视频地址'}

class TengXun(restful.Resource):
	"""
	腾讯的视频处理 , 待续
	这是一个包含视频的封面和title的地址：
	http://ncgi.video.qq.com/tvideo/fcgi-bin/vp_iphone?plat=2&otype=json&vid=x0016kc6wor
	"""
	def get(self, is_user_agent="pc"):
		"""
		is_user_agent:参数默认pc，为client表示客户端
		"""

		video_url = 'http://m.v.qq.com/play/play.html?coverid=fb67wf0ood33ubp&vid=x0016kc6wor&type=5&noright=0&protype=3&charge=0&ptag=4_4.0.2.8756_wxf' # 测试用，正式发布需要删除


		tengxun_get_url = 'http://vv.video.qq.com/geturl?vid=%s&otype=xml&platform=1'
		tengxun_get_info = 'http://vv.video.qq.com/getinfo?otype=xml&vid=%s'

		video_vid_value = '' # 视频的vid
		video_url_value = '' # 存储视频地址
		video_name = '' # 视频名称
		video_poster = 'http://shp.qpic.cn/qqvideo_ori/0/%s_496_280/0' # 视频封面

		if 'video_url' in flask_request.args and flask_request.args['video_url'] is not None:
			video_url = flask_request.args['video_url']

		myUrl = video_url = video_url+'&'
		user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Mobile/12F70 MicroMessenger/6.2 NetType/WIFI Language/zh_CN'
		if is_user_agent is not None and is_user_agent == "client":
			user_agent = flask_request.headers["User-Agent"]

		video_vid_re = re.findall('vid=(.*?)&', video_url)

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

					return {'code': 0, 'video': {'video_url' : video_url_value, 'video_poster' : video_poster % video_vid_value, 'name': video_name}}

		return {'code': -1, 'msg':'没有抓取到视频地址'}

class YouKu(restful.Resource):
	"""
	优酷的视频处理 
	这是优酷的地门地址：
	http://v.youku.com/player/getPlayList/VideoIDS/XMTI2NDIyMDkxMg==
	"""

	def get(self, is_user_agent="pc"):
		"""
		is_user_agent:参数默认pc，为client表示客户端
		"""

		video_url = 'http://v.youku.com/v_show/id_XNzQwOTkzNTM2.html?from=y1.3-idx-uhome-1519-20887.205905.1-1.1-8-1-1-0' # 测试用，正式发布需要删除

		# youku_get_url = 'http://v.youku.com/player/getPlayList/VideoIDS/%s/Pf/4/ctype/12/ev/1'


		if 'video_url' in flask_request.args and flask_request.args['video_url'] is not None:
			video_url = flask_request.args['video_url']

		user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Mobile/12F70 MicroMessenger/6.2 NetType/WIFI Language/zh_CN'
		if is_user_agent is not None and is_user_agent == "client":
			user_agent = flask_request.headers["User-Agent"]

		try:
			youku_obj = youku.YouKu(video_url=video_url)
			video_json_dict = youku_obj.getYouKuUrl()
			return {'code': 0, 'video':video_json_dict}
		except Exception as e:
			return {'code': -1, 'msg':'抓取视频出错'}

		return {'code': -1, 'msg':'没有抓取到视频地址'}

	def youku_vid(self, url):
		vid_search = re.search('id_(.*?).html', url)
		if vid_search:
			return vid_search.group(1)

		return None


api.add_resource(MiaoPai, '/miaopai/<string:is_user_agent>')
api.add_resource(MeiPai, '/meipai/<string:is_user_agent>')
api.add_resource(WeiBoShiPin, '/weiboshipin/<string:is_user_agent>')
api.add_resource(TengXun, '/tengxun/<string:is_user_agent>')
api.add_resource(YouKu, '/youku/<string:is_user_agent>')

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5001, debug=True)