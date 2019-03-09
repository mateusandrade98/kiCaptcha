import requests

def startDownload(url):
	r = requests.get(url) #abre a url da imagem
	with open('captcha/001.jpg','wb') as f: #abre um arquivo para escrita em binário
		f.write(r.content)#escreve o conteúdo da imagem
	return True#retorna verdadeiro
