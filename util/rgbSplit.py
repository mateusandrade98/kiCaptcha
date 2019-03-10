from PIL import Image as png #importação da biblioteca de tratamento de imagemself.
from PIL import ImageFilter as filter  #importação da biblioteca de tratamento de imagemself.
import numpy as np #importação da biblioteca de criação de conjuntos multidimensionais.

def imageCrop(img):
	im = img.convert('RGBA')
	l  = im.load()
	x 	= int(im.size[0])
	y 	= int(im.size[1])
	for i in range(x):
		for j in range(y):
			print(l[i,j])

def imagePrepare(img):
	print('[!] Preparando pixels(binário) e dimessão 28x28...')
	im = img.convert('L')
	width = float(im.size[0])#obtem o tamanho em float horizontal
	height = float(im.size[1])#obtem o tamanho em float vertical
	newImage = png.new('L', (28, 28), (255)) #cria uma tela branca de 28x28 pixels

	#verifica qual dimensão é maior
	if width > height:
        #A largura é maior. Largura se torna 20 pixels.
		nheight = int(round((20.0/width*height),0)) #redimensionar altura de acordo com a largura da relação
		if(nheight == 0): #caso raro, mas o mínimo é de 1 pixel
			nheigth = 1
        #redimensionar e aguçando
		img = im.resize((20,nheight), png.ANTIALIAS).filter(filter.SHARPEN)
		wtop = int(round(((28 - nheight)/2),0)) #calcular a posição horizontal
		newImage.paste(img, (4, wtop)) #colar imagem redimensionada na tela branca
	else:
        #A altura é maior. A altura torna-se 20 pixels.
		nwidth = int(round((20.0/height*width),0)) #redimensionar a largura de acordo com a altura da relação
		if(nwidth == 0): #caso raro, mas o mínimo é de 1 pixel
			nwidth = 1
         #redimensionar e aguçando
		img = im.resize((nwidth,20), png.ANTIALIAS).filter(filter.SHARPEN)
		wleft = int(round(((28 - nwidth)/2),0)) #calcular a posição vertical
		newImage.paste(img, (wleft, 4)) #colar imagem redimensionada na tela branca

	tv = list(newImage.getdata()) #obtem os valores dos pixels

	#normaliza os pixels para 0 e 1. 0 é branco puro, 1 é preto puro.
	tva = [(255-x)*1.0/255.0 for x in tv]
	return tva

def setAlphaImageToPNG(img):
	imgg  =img.convert('RGBA')#converte RGB para RGBA - Red, Green, Blue, Alpha.
	datas=imgg.getdata()#obtem todos os pares ordenados de cada pixel.
	newData = []#cria uma lista para gerenciar os pares ordenados.
	for item in datas:#ler um par ordenado de cada vez.
		if item[0] == 255 and item[1] == 255 and item[2] == 255:#verifica se a cor é 255,255,255(branco).
			newData.append((255, 255, 255, 0))#caso caia na condição aplica RGB 255,255,255(branco) e um alpha 0 -> 100% transparente, e joga o resultado dentro da lista.
		else:
			newData.append(item)#caso a condição não se aplicar, resulta no RGB normal, no caos 0,0,0(preto).
		imgg.putdata(newData)#substitui os dados pelo os novos dentro da imagem.
	return imgg #retorna a nova imagem com fundo transparente.

def convertGray(path):
	im=png.open(path,'r')#abre a imagem, em modo de leitura.
	print('[!] Localizando e cortando números')
	imageCrop(im)
	print('[!] Convertendo imagem para binário(preto&branco)...')
	gray = im.convert('L')#converte a imagem para uma matriz do tipo L RGB GrayScale.
	bw = gray.point(lambda x: 255 if x<230 else 0, '1')#converte a imagem para Gray, conta os pixels e verifica se o RGB for maior que 230, no caso é uma cor braco e retorna 0, caso o contario é uma cor escura e é retornado 255.
	print('[!] Convertendo imagem para PNG com fundo branco...')
	alpha = setAlphaImageToPNG(bw)#converte imagem para um PNG com fundo transparente.
	alpha.save(path)#salva a imagem com a conversão binária(preto e branco).
	print('[+] Imagem tratada e salva com sucesso -> '+path)
	return path#retorna local da imagem.

def arrayImage(path):
	return imagePrepare(png.open(path,'r')) #retorna um array multidimensional em 4D RGB.

def dealImage(path):
	return arrayImage(convertGray(path))
