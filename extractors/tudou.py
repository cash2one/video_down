import sys
import os
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

import requests
from urllib import request
import re

def get_tudou_vcode(url):
	# headers = {'User-Agent' : user_agent}
	req = request.Request(url)
	my_response = request.urlopen(req)
	my_page = my_response.read()

	unicode_page = my_page.decode("utf-8")
	vcode_re = re.search(r'vcode\s*[:=]\s*\'([^\']+)\'', unicode_page)

	if vcode_re:
		return vcode_re.group(1)


if __name__ == "__main__":
	get_tudou_vcode("http://www.tudou.com/albumplay/yKNjP5Tg2I8/9tOwnCJnATQ.html")
