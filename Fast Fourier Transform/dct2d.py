from cmath import cos
from cv2 import sqrt
import numpy as np
import math
import matplotlib.pyplot as plt
from numpy.fft import *
from PIL import Image as IMG
import cv2 as cv

##################################################### DCT #######################################################
def OneD_DCT(pic_line):#一维离散余弦变换n^2
    pic_line=np.squeeze(pic_line)
    n=pic_line.size
    w= np.array([[(math.cos(k*np.pi/n*(i+0.5))) for k in range(0,n)]  for i in range(0,n)])
    for i in range(0,n):
        w[i,0] = w[i,0] / math.sqrt(2)
    return pic_line.dot(w)

def DCT(img):
    return np.array([OneD_DCT(img[i, :]) for i in range(img.shape[0])])

def TwoD_DCT(img):
    n=img.shape[1]
    return DCT(DCT(img).T).T * 2 / math.sqrt(n*n)

################################################### iDCT #########################################################
def OneD_iDCT(pic_line):#一维离散反余弦变换n^2
    pic_line=np.squeeze(pic_line)
    n=pic_line.size
    w= np.array([[(cos(k*np.pi/n*(i+0.5))) for i in range(0,n)]  for k in range(0,n)])
    for i in range(0,n):
        w[0,i] = w[0,i] / math.sqrt(2)
    return pic_line.dot(w) 

def iDCT(img):
    return np.array([OneD_iDCT(img[i, :]) for i in range(img.shape[0])])

def TwoD_iDCT(img):
    return iDCT(iDCT(img).T).T 

##################################################################################################################


if __name__ == '__main__':
    img = cv.imread(r"./lenna.png", cv.IMREAD_COLOR)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gray=gray[0:1024,0:1024]

    plt.subplot(3, 3, 1)                         #原图
    plt.title('Gray')
    plt.imshow(gray,'gray')

    ori_dct = TwoD_DCT(gray)                    #原图dct
    plt.subplot(3, 3, 2)
    plt.title('ori_dct')
    plt.imshow(20 * np.log(abs(ori_dct)),'gray')

    ori_idct = TwoD_iDCT(ori_dct)                    #原图idct
    plt.subplot(3, 3, 3)
    plt.title('ori_idct')
    plt.imshow(abs(ori_idct),'gray')
    
    low_dct_1 = ori_dct.copy()
    low_dct_2 = ori_dct.copy()
    high_dct = ori_dct.copy()

    # for i in range(low_dct_1.shape[0]):
    #     for j in range(low_dct_1.shape[1]):
    #         if i > 32 or j > 32:
    #             low_dct_1[i, j] = 0  # 裁剪的实质为像素置0
    #         if i > 64 or j > 64:
    #             low_dct_2[i, j] = 0  # 裁剪的实质为像素置0
    #         if i < 32 or j < 32:
    #             high_dct[i, j] = 0  # 裁剪的实质为像素置0

    for i in range(low_dct_1.shape[0]):
        for j in range(low_dct_1.shape[1]):
            if i > 32 or j > 32:
                low_dct_1[i, j] = 0  # 裁剪的实质为像素置0
            if i > 128 or j > 128:
                low_dct_2[i, j] = 0  # 裁剪的实质为像素置0
            if i < 32 and j < 32:
                high_dct[i, j] = 0  # 裁剪的实质为像素置0

    plt.subplot(3, 3, 4)
    plt.title('low_dct_1')
    plt.imshow(20 * np.log(abs(low_dct_1)),'gray')

    plt.subplot(3, 3, 5)
    plt.title('low_dct_2')
    plt.imshow(20 * np.log(abs(low_dct_2)),'gray')

    plt.subplot(3, 3, 6)
    plt.title('high_dct')
    plt.imshow(20 * np.log(abs(high_dct)),'gray')


    low_idct_1 = TwoD_iDCT(low_dct_1)                #low1 idct
    plt.subplot(3, 3, 7)
    plt.title('low_idct_1')
    plt.imshow(abs(low_idct_1),'gray')

    low_idct_2 = TwoD_iDCT(low_dct_2)                #low2 idct
    plt.subplot(3, 3, 8)
    plt.title('low_idct_2')
    plt.imshow(abs(low_idct_2),'gray')

    high_idct = TwoD_iDCT(high_dct)                #high idct
    plt.subplot(3, 3, 9)
    plt.title('high_idct')
    plt.imshow(abs(high_idct),'gray')


    plt.show()