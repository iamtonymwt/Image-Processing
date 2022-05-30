from numpy import place, size
import jpeg
import Huffman
import matplotlib.pyplot as plt
import cv2 as cv

if __name__ == '__main__':
    original_img = cv.imread(r"./lenna.bmp", cv.IMREAD_COLOR)
    jpeg_imgs = []
    quality_list = [1, 5, 10, 15]
    places = [2, 3, 4, 5]

    for quality in quality_list:
        # temptree = Huffman.tree()
        # kjpeg = jpeg.KJPEG(quality)
        # kjpeg.Compress("./lenna.bmp")
        # temptree.encodefile("lenna"+str(quality)+".txt")
        # kjpeg.Decompress("./lenna"+str(quality)+".txt")
        
        img_path = './result'+str(quality)+'.bmp'
        img = cv.imread(img_path, cv.IMREAD_COLOR)
        jpeg_imgs.append(img)

    for i in range(len(quality_list)):
        plt.subplot(1, 5, places[i])
        plt.title('x'+str(quality_list[i]))
        jpeg_imgs[i] = jpeg_imgs[i][:,:,[2,1,0]]
        plt.imshow(jpeg_imgs[i])

    plt.subplot(1, 5, 1)
    plt.title('ori')
    original_img = original_img[:,:,[2,1,0]]
    plt.imshow(original_img)

    plt.show()

    name_list = ["ori", "x1", "x5", "x10", "x15"]
    size_list = [768, 65, 51, 44, 41]
    percent_list = [1, 65/768, 51/768, 44/768, 41/768]
    
    plt.subplot(121)
    plt.bar(name_list, size_list)
    for a, b in zip(name_list, size_list):
	    plt.text(a, b + 0.1, '%.0f' % b, ha='center', va='bottom', fontsize=7)
    plt.title('image size comparison')
    
    plt.subplot(122)
    plt.bar(name_list, percent_list)
    for a, b in zip(name_list, percent_list):
	    plt.text(a, b + 0.001, '%.3f' % b, ha='center', va='bottom', fontsize=7)
    plt.title('image size percentage comparison')

    plt.show()
    



