from PIL import Image as jpg
import numpy as np

def convertGray(path):
	im=jpg.open(path,'r')
	gray = im.convert('L')	
	bw = gray.point(lambda x: 0 if x<230 else 255, '1')
	bw.save(path)
	return True
