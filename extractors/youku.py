import sys
import os
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

import requests
import json
import base64
import re
from urllib import parse,request
import time

fake_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'UTF-8,*;q=0.5',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:13.0) Gecko/20100101 Firefox/13.0'
}

class YouKu:
	# video_url = 'http://v.youku.com/v_show/id_XMTI2NDM1MzAyMA==.html?from=y1.3-idx-uhome-1519-20887.205805-205902.6-1' # 测试用，正式发布需要删除
	# youku_get_url = 'http://v.youku.com/player/getPlayList/VideoIDS/%s/Pf/4/ctype/12/ev/1'

	def __init__(self, video_url='', youku_get_url='http://v.youku.com/player/getPlayList/VideoIDS/%s/Pf/4/ctype/12/ev/1'):
		self.vid = self.youku_vid(video_url)
		self.video_url = video_url
		self.youku_get_url = youku_get_url

	def generate_ep(vid, ep):
		f_code_1 = 'becaf9be' 
		f_code_2 = 'bf7e5f01' 

		def trans_e(a, c):
		    f = h = 0
		    b = list(range(256))
		    result = ''
		    while h < 256:
		        f = (f + b[h] + ord(a[h % len(a)])) % 256
		        b[h], b[f] = b[f], b[h]
		        h += 1
		    q = f = h = 0
		    while q < len(c):
		        h = (h + 1) % 256
		        f = (f + b[h]) % 256
		        b[h], b[f] = b[f], b[h]
		        if isinstance(c[q], int):
		            result += chr(c[q] ^ b[(b[h] + b[f]) % 256])
		        else:
		            result += chr(ord(c[q]) ^ b[(b[h] + b[f]) % 256])
		        q += 1

		    return result

		e_code = trans_e(f_code_1, base64.b64decode(bytes(ep, 'ascii')))
		sid, token = e_code.split('_')
		new_ep = trans_e(f_code_2, '%s_%s_%s' % (sid, vid, token))
		return base64.b64encode(bytes(new_ep, 'latin')), sid, token

	def youku_vid(self, url):
		vid_search = re.search('id_(.*?).html', url)
		if vid_search:
			return vid_search.group(1)

		return None


	def parse_m3u8(m3u8):
	    return re.findall(r'(http://[^?]+)\?ts_start=0', m3u8)

	def getYouKuUrl(self):
		youku_response = requests.get(self.youku_get_url % self.vid)

		if youku_response.status_code == 200:
			youku_response_text_dict = json.loads(youku_response.text)

			if not youku_response_text_dict['data']:
				print("没有抓取到数据data")
			metadata0 = youku_response_text_dict['data'][0]
			self.title = metadata0['title']
			self.img = metadata0['logo']
			self.ep = metadata0['ep']
			self.ip = metadata0['ip']

			new_ep, sid, token = self.__class__.generate_ep(self.vid, self.ep)
			# print("new_ep=%s, sid=%s, token=%s" % (new_ep, sid, token))

			m3u8_query = parse.urlencode(dict(
	            ctype=12,
	            ep=new_ep,
	            ev=1,
	            keyframe=1,
	            oip=self.ip,
	            sid=sid,
	            token=token,
	            ts=int(time.time()),
	            type='mp4',
	            vid=self.vid,
	        ))
			m3u8_url = 'http://pl.youku.com/playlist/m3u8?' + m3u8_query

			# print(m3u8_url)
			m3u8_url_response = requests.get(m3u8_url)
			# print(m3u8_url_response.text)

			m3u8_list_url = self.__class__.parse_m3u8(m3u8_url_response.text)

			return {'name':self.title, 'video_poster': self.img, 'video_urls':m3u8_list_url}			

if __name__ == "__main__":
	youku_obj = YouKu(video_url='http://v.youku.com/v_show/id_t8fXOcZsyPQ.html?from=y1.2-2.4.9')
	print(youku_obj.getYouKuUrl())

	# print(youku_obj.vid)
