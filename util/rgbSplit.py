from PIL import Image as png #importação da biblioteca de tratamento de imagemself.
from PIL import ImageFilter as filter  #importação da biblioteca de tratamento de imagemself.
from PIL import ImageDraw
import numpy as np #importação da biblioteca de criação de conjuntos multidimensionais.

def setGrayScale(img):
	gray        = img.convert('L')
	im          = gray.point(lambda x: 255 if x < 230 else 0, '1')
	rgba        = im.load()
	return rgba,im.size,im

def insertWhiteColor(img,x,y):
	imgg  =img.convert('RGBA')#converte RGB para RGBA - Red, Green, Blue, Alpha.
	size= x,y
	datas=imgg.getdata()#obtem todos os pares ordenados de cada pixel.
	newData = []#cria uma lista para gerenciar os pares ordenados.
	for item in datas:#ler um par ordenado de cada vez.
		if (item[0],item[1],item[2],item[3]) == (255,255,255,0):#verifica se a cor é 255,255,255(branco).
			newData.append((255, 255, 255, 255))#caso caia na condição aplica RGB 255,255,255(branco) e um alpha 0 -> 100% transparente, e joga o resultado dentro da lista.
		else:
			newData.append(item)#caso a condição não se aplicar, resulta no RGB normal, no caos 0,0,0(preto).
		imgg.putdata(newData)#substitui os dados pelo os novos dentro da imagem.
	imgg.thumbnail(size, png.ANTIALIAS)
	return imgg


def countPixels(img):
	total = 0
	rgba = img.load()#carrega o RGBA da imagem
	x,y  = img.size#pega o tamanho da imagem
	for i in range(x):
		for j in range(y):
			#verifica todos os pixels da imagem
			r,g,b,a = rgba[i,j]#obtem o tupla RGBA
			#if isBackgroundBlack == 0:
			#	if (r,g,b,a) == (0,0,0,255):#encontrou cor, alpha == 255
			#		total+=1#adiciona +1 no total
			if (r,g,b,a) == (0,0,0,255):#encontrou cor, alpha == 255
					total+=1#adiciona +1 no total
			#else:
			#	if (r,g,b,a) == (255,255,255,255):#encontrou cor, alpha == 255
			#		total+=1#adiciona +1 no total
	return total

def imageCropCognitive(imagem):

	rgba = imagem.load()
	x, y = imagem.size
	img2 = imagem
	ImageDraw.Draw(img2).rectangle((0, 0, x-1, y-1), outline=(255,255,255))
	imagens = []
	direita = 0
	posicoes = []

	while direita < x:

        # variáveis para recorte
		corte_xy = 0
		pos_xy = []
        #-----------------------

        # loop para corte do eixo x e depois eixo y
		for c in range(2):

			cont = 0

			eixo1 = y
			eixo2 = x
			inicio1 = 0
			inicio2 = direita

			if c == 0:

				eixo1 = x
				eixo2 = y
				inicio1 = direita
				inicio2 = 0


            # posicão eixo1, é x ou y (depende do valor de c)
			for ex1 in range(inicio1, eixo1):

				fim = False

                # posicão eixo1, é x ou y (depende do valor de c)
				for ex2 in range(inicio2, eixo2):

					corte_xy = ex1

					if c == 0:
						r, g, b, a = rgba[ex1, ex2]
					else:
						r, g, b, a = rgba[ex2, ex1]

                    # verifica se é o primeiro ou o segundo corte
					if cont == 0:

                        # verifica se o pixel é preto (não é necessário verificar o 'RGB' completo ...
                        # ... porque se for preto será R=0 G=0 B=0, então só analizei uma paleta de cor)

						if r == 0:
                            # salva o primeiro corte do eixo 1 (dependendo do valor de c pode ser o eixo x ou y)
							if ex1 >= 2:
								pos_xy.append(corte_xy - 2)
							else:
								pos_xy.append(corte_xy)
                            #-----------------------------------------------------------------------------------

							cont = 1

							break
                        #-------------------------------------------------------------------------------

					else:

						fim = True

                        # verifica se o pixel é preto (não é necessário verificar o 'RGB' completo ...
                        # ... porque se for preto será R=0 G=0 B=0, então só analizei uma paleta de cor)
						if r == 0:
							fim = False
							break
                        #-------------------------------------------------------------------------------


                    #---------------------------------------------


                # salva o ultimo corte do eixo 1 (dependendo do valor de c pode ser o eixo x ou y)
                #---------------------------------------------------------------------------------
				if fim:
					if ex1 <= eixo1 - 2:
						pos_xy.append(corte_xy + 2)
					else:
						pos_xy.append(corte_xy)
					break


        #------------------------------------------------------

		if len(pos_xy) == 4:
			img_corte = img2.crop((pos_xy[0], pos_xy[2], pos_xy[1], pos_xy[3]))
			imagens.append(img_corte)
			posicoes.append([pos_xy[0], pos_xy[1], pos_xy[2], pos_xy[3]])
			direita = pos_xy[1]
		else:
			break

	imagens_cortadas = []

	for p in range(len(posicoes)):

		im2 = imagem
		pos_xy = []
		corte = cont = 0

		for y in range(posicoes[p][2], posicoes[p][3]+1):

			fim = False

			for x in range(posicoes[p][0], posicoes[p][1]+1):

				corte = y

				r, g, b, a = rgba[x, y]

				if cont == 0:

                    # verifica se o pixel é preto (não é necessário verificar o 'RGB' completo ...
                    # ... porque se for preto será R=0 G=0 B=0, então só analizei uma paleta de cor)

					if r == 0:
                        # salva o primeiro corte do eixo 1 (dependendo do valor de c pode ser o eixo x ou y)
						if y >= 2:
							pos_xy.append(corte - 2)
						else:
							pos_xy.append(corte)
                        #-----------------------------------------------------------------------------------

						cont = 1

						break
                    #-------------------------------------------------------------------------------

				else:
					fim = True

                    # verifica se o pixel é preto (não é necessário verificar o 'RGB' completo ...
                    # ... porque se for preto será R=0 G=0 B=0, então só analizei uma paleta de cor)
					if r == 0:
						fim = False
						break
                    #-------------------------------------------------------------------------------


                #---------------------------------------------


            # salva o ultimo corte do eixo 1 (dependendo do valor de c pode ser o eixo x ou y)
			if fim:
				if y <= posicoes[p][3]-1:
					pos_xy.append(corte + 2)
				else:
					pos_xy.append(corte)
				break


		imagens_cortadas.append(img2.crop((posicoes[p][0], pos_xy[0], posicoes[p][1], pos_xy[1])))


	return imagens_cortadas


def imagePrepare(img):
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
	x 	= int(imgg.size[0])
	y 	= int(imgg.size[1])
	size= 300,300
	datas=imgg.getdata()#obtem todos os pares ordenados de cada pixel.
	newData = []#cria uma lista para gerenciar os pares ordenados.
	for item in datas:#ler um par ordenado de cada vez.
		if (item[0],item[1],item[2],item[3]) == (255,255,255,255):#verifica se a cor é 255,255,255(branco).
			newData.append((255, 255, 255, 255))#caso caia na condição aplica RGB 255,255,255(branco) e um alpha 0 -> 100% transparente, e joga o resultado dentro da lista.
		else:
			newData.append(item)#caso a condição não se aplicar, resulta no RGB normal, no caos 0,0,0(preto).
		imgg.putdata(newData)#substitui os dados pelo os novos dentro da imagem.
	imgg.thumbnail(size, png.ANTIALIAS)
	return imgg #retorna a nova imagem com fundo transparente.

def convertGray(path):
	im=png.open(path,'r')#abre a imagem, em modo de leitura.
	execute_crop = input('Deseja cortar os elementos de um conjunto de números? (S/n): ').lower()
	print('[!] Convertendo imagem para binário(preto&branco)...')
	#gray = im.convert('L')#converte a imagem para uma matriz do tipo L RGB GrayScale.
	#back = backgroundColor(gray)
	#if back == 0:
	#	bw = gray.point(lambda x: 255 if x < 230 else 0, '1')#converte a imagem para Gray, conta os pixels e verifica se o RGB for maior que 230, no caso é uma cor braco e retorna 0, caso o contario é uma cor escura e é retornado 255.
	#bw = gray.point(lambda x: 255 if x < 230 else 0, '1')
	#else:
	#	bw = gray.point(lambda x: 255 if x>230 else 0, '1')
	v,vv,bw = setGrayScale(im)
	print('[!] Convertendo imagem para PNG com fundo branco...')
	alpha = setAlphaImageToPNG(bw)#converte imagem para um PNG com fundo transparente.
	#alpha = alpha.filter(filter.GaussianBlur(1))
	alpha.save(path)#salva a imagem com a conversão binária(preto e branco).
	print('[+] Imagem tratada e salva com sucesso -> '+path)
	if execute_crop == "":
		execute_crop = 's'
	if execute_crop == "s":
		print('[!] Localizando e cortando números')
		imagens = imageCropCognitive(alpha)
		bb=0
		for image in imagens:
			bb+=1
			image = image.filter(filter.GaussianBlur(0.8))
			image.save('captcha/00'+str(bb)+'.png')
	return path#retorna local da imagem.

def arrayImage(path):
	return imagePrepare(png.open(path,'r')) #retorna um array multidimensional em 4D RGB.

def dealImage(path):
	return arrayImage(convertGray(path))
