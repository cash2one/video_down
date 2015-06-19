from flask import Flask, request as flask_request
from flask.ext import restful
from urllib import request
import requests
import json
import jsonpickle
import re
from extractors import youku
from extractors.tudou import get_tudou_vcode

app = Flask("videoapi")
api = restful.Api(app)

# sites = [{"id": "miaopai.com", "name":"秒拍"}]

class Video(restful.Resource):
	"""公共的视频处理"""
	def get(self, is_user_agent="pc"):
		"""
		is_user_agent:参数默认pc，为client表示客户端
		"""
		video_url = 'http://www.tudou.com/albumplay/yKNjP5Tg2I8/9tOwnCJnATQ.html' # 测试用，正式发布需要删除
		if 'video_url' in flask_request.args and flask_request.args['video_url'] is not None:
			video_url = flask_request.args['video_url']

		user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Mobile/12F70 MicroMessenger/6.2 NetType/WIFI Language/zh_CN'
		if is_user_agent is not None and is_user_agent == "client":
			user_agent = flask_request.headers["User-Agent"]

		if video_url.find("miaopai.com") > -1:
			from extractors.miaopai import getVideoObject
		if video_url.find("meipai.com") > -1:
			from extractors.meipai import getVideoObject
		if video_url.find("qq.com") > -1:
			from extractors.tengxun import getVideoObject
		if video_url.find("youku.com") > -1:
			from extractors.youku import getVideoObject
		if video_url.find("tudou.com") > -1:
			from extractors.tudou import getVideoObject
		
		return getVideoObject(video_url=video_url)


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


# class Tudou(restful.Resource):
# 	"""
# 	土豆的视频处理 
# 	这是土豆直接解析地址，不分格式:
# 	http://cnc.v2.tudou.com/f?id=233753311
# 	"""

# 	def get(self, is_user_agent="pc"):
# 		"""
# 		is_user_agent:参数默认pc，为client表示客户端
# 		"""

# 		video_url = 'http://www.tudou.com/albumplay/yKNjP5Tg2I8/9tOwnCJnATQ.html' # 测试用，正式发布需要删除

# 		if 'video_url' in flask_request.args and flask_request.args['video_url'] is not None:
# 			video_url = flask_request.args['video_url']

# 		user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Mobile/12F70 MicroMessenger/6.2 NetType/WIFI Language/zh_CN'
# 		if is_user_agent is not None and is_user_agent == "client":
# 			user_agent = flask_request.headers["User-Agent"]

# 		try:
# 			vcode = get_tudou_vcode(video_url)
# 			if vcode:
# 				youku_obj = youku.YouKu(video_url="http://v.youku.com/v_show/id_%s.html" % vcode)
# 				video_json_dict = youku_obj.getYouKuUrl()
# 				return {'code': 0, 'video':video_json_dict}
# 			else:
# 				{'code': -1, 'msg':'不支持解析'}
# 		except Exception as e:
# 			return {'code': -1, 'msg':'抓取视频出错'}

# 		return {'code': -1, 'msg':'没有抓取到视频地址'}


# api.add_resource(MiaoPai, '/miaopai/<string:is_user_agent>')
# api.add_resource(MeiPai, '/meipai/<string:is_user_agent>')
api.add_resource(WeiBoShiPin, '/weiboshipin/<string:is_user_agent>')
# api.add_resource(TengXun, '/tengxun/<string:is_user_agent>')
# api.add_resource(YouKu, '/youku/<string:is_user_agent>')
# api.add_resource(Tudou, '/tudou/<string:is_user_agent>')
api.add_resource(Video, '/video/<string:is_user_agent>')

if __name__ == '__main__':
	app.run(host='0.0.0.0')