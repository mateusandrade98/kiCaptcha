#-*- coding:utf-8 -*-
from util import DownloadCaptcha as dw #minha biblioteca para baixar arquivos
from util import rgbSplit as rgb #minha biblioteca para tratamento do captcha
from util import recognize as rc #minha biblioteca para mnist
import subprocess as sp #biblioteca para executar processos

"""
Projeto desenvolvido por Joandeson Andrade, estudante de ciência da computação, UFPB - campus IV, Rio Tinto-PB.
O kiCaptcha tem como objetivo acadêmico e para provar o quando os computadores estão inteligêntes, e que alguns sistemas feito para evitar ataques estão falhando miseravelmente.
Espero que este projeto seja melhorado, estudado, e usado para uma gama maior de tecnologia.
MUITO OBRIGADO!
"""


url='https://sigadmin.ufpb.br/admin/captcha.jpg'
captchaPath = 'captcha/captcha.png'
print('Iniciando kiCaptcha...')
if dw.startDownload(url) == True:
	print('[+] Captcha baixado com sucesso ->',captchaPath)
	execute_deal_image = input('Deseja tratar imagem? (S/n): ').lower()
	if execute_deal_image == "":
		execute_deal_image = 's'
	if execute_deal_image == "s":
		captcha = rgb.dealImage(captchaPath)
	else:
		captcha = rgb.arrayImage(captchaPath)
	execute_captcha = input('Deseja abrir o captcha? (s/N): ').lower()
	if execute_captcha == "s":
		print('[*] Visualizador de imagem...')
		sp.run('feh '+captchaPath,shell=True,check=True)

	execute_netneural = input('Deseja executar a rede neural? (S/n): ').lower()
	if execute_netneural == "":
		execute_netneural = 's'
	if execute_netneural != "s":
		exit()
	rc.initRecognize(captcha)
else:
	print('[-] Problema no download do captcha')
