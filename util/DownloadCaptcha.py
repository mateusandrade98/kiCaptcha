import requests

def startDownload(url):
	r = requests.get(url)
	with open('captcha/001.jpg','wb') as f:
		f.write(r.content)
	return True
