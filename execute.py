#-*- coding:utf-8 -*-
from util import DownloadCaptcha as dw #minha biblioteca para baixar arquivos
from util import rgbSplit as rgb #minha biblioteca para tratamento do captcha
#from util import recognize as rc #minha biblioteca para deep learning mnist(banco de dados de imagem de manuscrito para treinamento)
from util import preRecognize as pr#minha biblioteca para deep learning com treinamento já processado mnist(banco de dados de imagem de manuscrito para treinamento)
import subprocess as sp #biblioteca para executar processos
import threading#importação da biblioteca de thread
import time

"""
Projeto desenvolvido por Joandeson Andrade e Jessé Silva, estudantes de ciência da computação, UFPB - campus IV, Rio Tinto-PB.
O kiCaptcha tem como objetivo acadêmico e para provar o quando os computadores estão inteligêntes, e que alguns sistemas feito para evitar ataques estão falhando miseravelmente.
Espero que este projeto seja melhorado, estudado, e usado para uma gama maior de tecnologia.
MUITO OBRIGADO!
"""


class runnerNeuralThread(threading.Thread):
   def __init__(self, threadID):
      threading.Thread.__init__(self)
      self.threadID = threadID
   def run(self):
	   prevision = 0
	   captcha = rgb.arrayImage('captcha/00'+str(self.threadID+1)+'.png')
	   recognize = pr.initRecognize(captcha)[0]
	   self.prevision = recognize


url='https://sigadmin.ufpb.br/admin/captcha.jpg'
captchaPath = 'captcha/captcha.png'
print('Iniciando kiCaptcha...')
if dw.startDownload(url) == True:
	print('[+] Captcha baixado com sucesso ->',captchaPath)

	execute_deal_image = input('Deseja tratar imagem? (S/n): ').lower()[:1]
	if execute_deal_image == "":
		execute_deal_image = 's'
	if execute_deal_image != 's' and execute_deal_image != 'n':
		exit()
	if execute_deal_image == "s":
		captcha = rgb.dealImage(captchaPath)

	execute_captcha = input('Deseja abrir o captcha? (s/N): ').lower()[:1]
	if execute_captcha == '':
		execute_captcha = 'n'
	if execute_captcha != 's' and execute_captcha != 'n':
		exit()
	if execute_captcha == "s":
		print('[*] Visualizador de imagem...')
		sp.run('feh '+captchaPath,shell=True,check=True)

	execute_netneural = input('Deseja executar a rede neural? (S/n): ').lower()[:1]
	if execute_netneural == "":
		execute_netneural = 's'
	if execute_netneural != 's' and execute_netneural != 'n':
		exit()
	if execute_netneural != "s":
		exit()
	recognize=''
	#captcha = rgb.arrayImage('captcha/captcha.png')
	#recognize=rc.initRecognize(captcha)
	#for i in range(0,6):
	#	captcha = rgb.arrayImage('captcha/00'+str(i+1)+'.png')
	#	recognize=recognize+str(rc.initRecognize(captcha))
	print('[*] Iniciando threading... [6]')
	print('[!] Preparando pixels(binário) e dimessão 28x28...')

	ree  = []

	for i in range(0,6):#prepara o thread
		ree.insert(i,runnerNeuralThread(i))

	for th in ree:
		th.start()
		th.join()
		recognize=recognize+str(th.prevision)

	print(recognize)

	print('A previsão da númeração é:',recognize)
else:
	print('[-] Problema no download do captcha')
