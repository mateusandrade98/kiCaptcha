#-*- coding:utf-8 -*-
from util import DownloadCaptcha as dw
from util import rgbSplit as rgb
from util import recognize as rc
import subprocess as sp

url='https://sigadmin.ufpb.br/admin/captcha.jpg'
if dw.startDownload(url) == True:
	print('[+] Captcha baixado com sucesso -> captcha/001.jpg')
	print('[!] Convertendo imagem para binário(preto&branco)...')
	rgb.convertGray('captcha/001.jpg')
	execute_captcha = input('Deseja abrir o captcha? (s/N): ').lower()
	if execute_captcha == "s":
		print('[*] Visualizador de imagem...')
		sp.run('feh captcha/001.jpg',shell=True,check=True)
else:
	print('[-] Problema no download do captcha')
