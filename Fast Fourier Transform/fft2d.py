import numpy as np
import math
import matplotlib.pyplot as plt
from numpy.fft import *
from PIL import Image as IMG
import cv2 as cv

##################################################### FFT #######################################################
def dft(pic_line):#一维离散傅里叶变换n^2
    pic_line=np.squeeze(pic_line)
    n=pic_line.size
    w=np.array([[np.exp(-1j*2*np.pi*i*k/n) for k in range(0,n) ] for i in range(0,n)]).T#系数矩阵，生成之后需要转置
    return pic_line.dot(w)

def Butterfly_operation(seq1,seq2):#蝶形运算 seq1为偶序列，seq2为奇序列
    n=seq1.size
    N=n*2
    seq1=np.squeeze(seq1)#降维
    seq2=np.squeeze(seq2)
    res=np.zeros(2*n,dtype=seq1.dtype)
    for i in range(0,n):
        res[i]+=seq1[i]+np.exp(-1j*2*np.pi*i/N)*seq2[i]
        res[n+i]=seq1[i]-np.exp(-1j*2*np.pi*i/N)*seq2[i]
    return  res

def fft(img):#递归分治实现fft,只对图像的每一行做fft
    n=img.shape[1]
    if(n%2!=0):
        return ValueError("图片大小不是2的次幂")#因为fft分治时每次都分为等大的奇数列和偶数列
    if(n<=8):#n足够小，直接n方对每行求dft
        return np.array([dft(img[i, :]) for i in range(img.shape[0])])
    res_odd=fft(img[:,1::2])
    res_even=fft(img[:,0::2])
    return  np.array([Butterfly_operation(res_even[i:i+1,:],res_odd[i:i+1,:]) for i in range(0,img.shape[0])])

def TwoD_fft(img):
    return fft(fft(img).T).T

def FFT_SHIFT(img):
    M, N = img.shape
    M = int(M / 2)
    N = int(N / 2)
    return np.vstack((np.hstack((img[M:, N:], img[M:, :N])), np.hstack((img[:M, N:], img[:M, :N]))))

###################################################### iFFT ########################################################
def idft(fft_line):#一维离散傅里叶反变换n^2
    fft_line=np.squeeze(fft_line)
    n=fft_line.size
    w=np.array([[np.exp(1j*2*np.pi*i*k/n) for k in range(0,n) ] for i in range(0,n)]).T#系数矩阵，生成之后需要转置
    return fft_line.dot(w)

def iButterfly_operation(seq1,seq2):#蝶形运算 seq1为偶序列，seq2为奇序列
    n=seq1.size
    N=n*2
    seq1=np.squeeze(seq1)#降维
    seq2=np.squeeze(seq2)
    res=np.zeros(2*n,dtype=seq1.dtype)
    for i in range(0,n):
        res[i]+=seq1[i]+np.exp(1j*2*np.pi*i/N)*seq2[i]
        res[n+i]=seq1[i]-np.exp(1j*2*np.pi*i/N)*seq2[i]
    return  res

def ifft(img):#递归分治实现ifft,只对fft的每一行做ifft
    n=img.shape[1]
    if(n<=8):#n足够小，直接n方对每行求idft
        return np.array([idft(img[i, :]) for i in range(img.shape[0])])
    res_odd=ifft(img[:,1::2])
    res_even=ifft(img[:,0::2])
    return  np.array([iButterfly_operation(res_even[i:i+1,:],res_odd[i:i+1,:]) for i in range(0,img.shape[0])])

def TwoD_ifft(img):
    n=img.shape[1]
    return ifft(ifft(img).T).T /n/n

####################################################################################################################
if __name__ == '__main__':
    img = cv.imread(r"./lenna.png", cv.IMREAD_COLOR)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gray=gray[0:1024,0:1024]

    plt.subplot(2, 2, 1)                         #原图
    plt.title('Gray')
    plt.imshow(gray,'gray')

    ori_fft = TwoD_fft(gray)     #原图fft
    plt.subplot(2, 2, 3)
    plt.title('ori_fft')
    plt.imshow(np.log(1 + abs(FFT_SHIFT(ori_fft))),'gray')

    cows, cols = ori_fft.shape                          #低频滤波fft
    mask = np.ones((cows, cols), int)
    mask[int(cows/2+100):int(cows/2+105), int(cols/2+100):int(cols/2+105)] = 500
    mask[int(cows/2-105):int(cows/2-100), int(cols/2-105):int(cols/2-100)] = 500
    low_fft = FFT_SHIFT(ori_fft) * mask 
    plt.subplot(2, 2, 4)
    plt.title('mark_fft')
    plt.imshow(np.log(1 + abs(low_fft)),'gray')

    low_ifft = TwoD_ifft(FFT_SHIFT(low_fft))  #低频滤波图
    plt.subplot(2, 2, 2)
    plt.title('mark_ifft')
    plt.imshow(abs(low_ifft),'gray')


    # rows, cols = ori_fft.shape         #高频滤波fft
    # crows, ccols =int(rows/2), int(cols/2)
    # high_fft = FFT_SHIFT(ori_fft)
    # high_fft[crows-30:crows+30, ccols-30:ccols+30] = 0
    # plt.subplot(2, 3, 5)
    # plt.title('high_fft')
    # plt.imshow(np.log(1 + abs(high_fft)),'gray')


    # high_ifft = TwoD_ifft(FFT_SHIFT(high_fft))  #高频滤波图
    # plt.subplot(2, 3, 2)
    # plt.title('high_ifft')
    # plt.imshow(abs(high_ifft),'gray')

    # cows, cols = ori_fft.shape                          #低频滤波fft
    # mask = np.zeros((cows, cols), np.uint8)
    # mask[int(cows/2-30):int(cows/2+30), int(cols/2-30):int(cols/2+30)] = 1
    # low_fft = FFT_SHIFT(ori_fft) * mask 
    # plt.subplot(2, 3, 6)
    # plt.title('low_fft')
    # plt.imshow(np.log(1 + abs(low_fft)),'gray')

    # low_ifft = TwoD_ifft(FFT_SHIFT(low_fft))  #低频滤波图
    # plt.subplot(2, 3, 3)
    # plt.title('low_ifft')
    # plt.imshow(abs(low_ifft),'gray')


    # target = abs(fftshift(fft2(gray)))        #numpy_fft
    # plt.subplot(2,2,3)
    # plt.title('numpy.fft2')
    # plt.imshow(np.log(1+target),'gray')

    plt.show()