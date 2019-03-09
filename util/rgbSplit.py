from PIL import Image as jpg
import numpy as np

def convertGray(path):
	im=jpg.open(path,'r')#abre a imagem
	gray = im.convert('L')#converte a imagem para uma matriz do tipo L
	bw = gray.point(lambda x: 0 if x<230 else 255, '1')#converte a imagem para Gray, conta os pixels e verifica se o RGB for maior que 230, no caso é uma cor braco e retorna 255, caso o contario é uma cor escura e é retornado 0
	bw.save(path)#salva a imagem com a conversão binária(preto e branco)
	return True#retorna verdadeiro
