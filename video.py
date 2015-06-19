from flask import Flask, request as flask_request
# from flask.ext import restful
from urllib import request
import re

app = Flask(__name__)
# api = restful.Api(app)

@app.route('/miaopai', methods=['GET'])
@app.route('/miaopai/<is_user_agent>', methods=['GET'])
def load_html(is_user_agent = "pc", video_url = 'http://miaopai.com/show/5LPgnn12nqst7IoBAHCN1Q__.htm'):
	"""
	is_user_agent:参数默认pc，为client表示客户端
	"""
	if flask_request.args['video_url'] is not None:
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

		result_search = re.search('<video.*?</video>', unicode_page)

		if result_search:
			video_str = result_search.group()
			video_src = re.findall("src=\'(.*?)\'", video_str)
			if video_src is not None and len(video_src) > 0:
				return video_src[0]

		# print(flask_request.headers["User-Agent"])
	except Exception as e:
		return '抓取视频出错'
	return '没有抓取到视频地址'


if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)