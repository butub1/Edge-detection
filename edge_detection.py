#coding : utf-8
'''
@author: butub
2019/6/8
'''
import matplotlib.pyplot as plt
import numpy as np
import cv2
from common import config
from skimage import data,filters,img_as_ubyte, feature
import skimage


'''
a plot class based on pyplot
prety useful for me to display gray images
'''
class Plot:
    def __init__(self, title="Title"):
        self.title = title
        self.mlist=[]
        self.mnamelist=[]
        self.i=0

    def show(self):
        num = len(self.mlist)
        row = np.sqrt(num)//1
        if num % row == 0:
            col = num // row
        else:
            col = num // row + 1
        fig = plt.figure()
        fig.suptitle( self.title )

        for i in range(1, num+1):
            ax = fig.add_subplot(row, col, i)
            ax.set_title(self.mnamelist[i-1])
            plt.imshow(self.mlist[i-1], cmap = 'gray')
        plt.show()

    def append(self, img, img_name=None):
        self.mlist.append(img)
        if img_name == None:
            self.mnamelist.append("%d" % self.i)
        else:
            self.mnamelist.append("["+  str(self.i)+ "] " + img_name)
        self.i = self.i + 1


def filter(src, btm,kernel = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]],  threshold = [0, 255]): 
    '''src--source, btm--bottom'''
    '''只处理3x3kernel'''
    src = src.copy().astype(np.float)# 一定要记得统一计算的精度为flaot
    kernel = np.array(kernel, dtype= np.float)
    src_row, src_col = src.shape
    btm_row, btm_col = btm.shape
    print("btm_shape:", btm.shape)
    for i in range(src_row):
        for j in range(src_col):
            src[i][j] = abs( np.sum( btm[i : i+3 , j: j+3] * kernel ))
    src_norm= (src*255 / src.max()).astype(np.int) # 用最大值归一化
    #src_clip = np.clip(src, 0, 255)
    #output = np.zeros_like(src)
    #output[ (src_norm >= threshold[0]) &  (src_norm <=threshold[1]) ] = 255 # 截断

    return src_norm
    
def gauss(src, padding, kernel = [[1,2,1],[2,4,2],[1,2,1]]):
    '''src--source, btm--bottom'''
    '''只处理3x3kernel'''
    btm = 0
    if padding :
        btm = cv2.copyMakeBorder(src, 1, 1, 1,1 ,cv2.BORDER_WRAP)

    src = src.copy().astype(np.float)
    kernel = np.array(kernel, dtype= np.float)
    src_row, src_col = src.shape
    btm_row, btm_col = btm.shape
    print("btm_shape:", btm.shape)
    for i in range(src_row):
        for j in range(src_col):
            src[i][j] = (btm[i : i+3 , j: j+3] * kernel ).sum()/16
    src = np.clip(src, 0, 255)
    return src



def sobel(img, padding = False, threshold=100):
    ps = Plot("sobel")
    ps.append(img, "default")
    #img = gauss(img,True)
    if padding:
        img_p = cv2.copyMakeBorder(img, 1, 1, 1,1 ,cv2.BORDER_WRAP)
        print("after padding:", img_p.shape)

    #img = gauss(img, img_p)
    img_s1 = filter(img, img_p, kernel =  [[-1, -2, -1], [0, 0, 0], [1, 2, 1]] )
    img_s2 = filter(img, img_p, kernel =  [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]] )
    img_s = abs(img_s1) + abs(img_s2) # s = |s1| + |s2|
    img_ss = np.sqrt(img_s1*img_s1 + img_s2*img_s2)

    img_std = cv2.Sobel(img,cv2.CV_16S,1,1)
    img_std = cv2.convertScaleAbs(img_std)
    img_diff = abs(img_ss - img_std)

    ps.append(img_s1, "sobel_x")
    ps.append(img_s2, "sobel_y")
    ps.append(img_s, "sobel: |x| + |y|")
    ps.append(img_ss, "sobel: sqrt(x^2+y^2)")
    ps.append(img_std, "standard")
    ps.append(img_diff, "diff:%.3f" % (img_diff.sum() / img.size))
    ps.show()
    
    '''
    cv2.imshow("imhsow1", img) # cv2.imshow seems hard to use
    cv2.imshow("imshow2",img_s1)
    cv2.imshow("imshow3",img_s2)
    cv2.imshow("imshow4",img_s)
    cv2.imshow("imshow5",img_ss)
    cv2.waitKey(0)
    '''
def sobel_sd(img, padding = False, threshold=100): # standard
    ps = Plot()
    if padding:
        img_p = cv2.copyMakeBorder(img, 1, 1, 1,1 ,cv2.BORDER_WRAP)
        print("after padding:", img_p.shape)
        print(img_p)

    img_s = filters.sobel(img)
    img_s = img_as_ubyte(img_s)
    ps.append(img, "defalut")
    ps.append(img_s, "standard")
    ps.show()

def laplace(img, padding = False):
    pl = Plot("laplace")
    pl.append(img, "defalut")
    #img = gauss(img,True)
    if padding:
        img_p = cv2.copyMakeBorder(img, 1,1,1,1, cv2.BORDER_WRAP)
    img_l = filter(img, img_p, kernel = [[0, -1, 0], [-1, 4, -1], [0, -1, 0]])
    #img_l = filter(img, img_p, kernel = [[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])
    img_sharpening_add = img + img_l
    img_sharpening_add[img_sharpening_add > 255] = 255
    img_sharpening_sub = img - img_l
    img_sharpening_sub[img_sharpening_sub < 0] = 0
    #img_sd = filters.laplace(img) # 这个api的表现有点奇怪
    #img_sd = img_as_ubyte(img_sd)
    #img_sd = np.uint8(img_sd)
    img_sd = cv2.Laplacian(img, cv2.CV_64F, ksize = 3)    
    img_sd = cv2.convertScaleAbs(img_sd)    

    pl.append(img_l, "laplace")
    pl.append(img_sharpening_add, "sharpening: img+laplace")
    pl.append(img_sharpening_sub, "sharpening: img-laplace")
    pl.append(img_sd, "standard")
    pl.show()


def prewitt(img, padding= False):
    pp = Plot("prewitt")
    pp.append(img, "default")
    #img = gauss(img, True)
    if padding:
        img_p = cv2.copyMakeBorder(img ,1,1,1,1, cv2.BORDER_WRAP)
    img_p1 = filter(img, img_p, kernel = [[-1,-1,-1],[0,0,0],[1,1,1]])
    img_p2 = filter(img, img_p, kernel = [[-1,0,1],[-1,0,1],[-1,0,1]])
    img_pp = np.sqrt(img_p1*img_p1 + img_p2*img_p2).astype(np.int)
    img_sd = filters.prewitt(img)
    img_sd = np.uint8(img_sd)
    #img_sd = img_as_ubyte(img_sd)
    #pp.append(img_p)
    pp.append(img_p1, "prewitt_x")
    pp.append(img_p2, "prewitt_y")
    pp.append(img_pp, "prewitt: sqrt(x^2 + y^2)")
    pp.append(img_sd, "standard")
    pp.show()

def canny(img):
    pc = Plot("canny")
    gamma = [0,1,2,5,10]
    pc.append(img, "defalut")
    #img = gauss(img, True)
    for i in gamma:
        img_c = feature.canny(img, i, 50,100)
        pc.append(img_c, "gamma=%d"%i)
    pc.show()
    

def scharr(img, padding = False):
    ps = Plot("scharr")
    ps.append(img, "defalut")
    #img = gauss(img, True)
    if padding:
        img_p = cv2.copyMakeBorder(img, 1, 1, 1,1 ,cv2.BORDER_WRAP)

    #img = gauss(img, img_p)
    img_s1 = filter(img, img_p, kernel =  [[-3, -10, -3], [0, 0, 0], [3, 10, 3]] )
    img_s2 = filter(img, img_p, kernel =  [[-3, 0, 3], [-10, 0, 10], [-3, 0, 3]] )
    img_s = abs(img_s1) + abs(img_s2) # s = |s1| + |s2|
    img_ss = np.sqrt(img_s1*img_s1 + img_s2*img_s2)

    img_std_x = cv2.Sobel(img,cv2.CV_64F,0,1, ksize=-1)
    img_std_y = cv2.Sobel(img,cv2.CV_64F,1,0, ksize=-1)
    img_std = np.sqrt(img_std_x*img_std_x + img_std_y*img_std_y)
    img_std = cv2.convertScaleAbs(img_std)
    img_diff = abs(img_ss - img_std)

    ps.append(img_s1, "scharr_x")
    ps.append(img_s2, "scharr_y")
    ps.append(img_s, "|x| + |y|")
    ps.append(img_ss, "(x^2 + y^2)^0.5")
    ps.show()


def main():
    img = cv2.imread(config.img_path, 0)
    try:
        assert img.any()!=None
    except AssertionError :
        print("could not open: " + config.img_path)
    else:
        print(img , img.shape, type(img))
        img = img.astype(np.float)
        img = gauss(img, True)
        img = skimage.exposure.equalize_hist(img)
        sobel(img, True)
        laplace(img, True)
        prewitt(img, True)
        canny(img)
        scharr(img,True)
        #sobel_sd(img, True)

if __name__ == "__main__":
    main()
