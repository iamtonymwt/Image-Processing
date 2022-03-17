#include <iostream>  
#include <opencv2/core/core.hpp>  
#include <opencv2/highgui/highgui.hpp>  

using namespace cv;
using namespace std;

const int size512 = 512;

void change2grey(Mat* in_img, Mat* grey_img) {

	unsigned char* optr = in_img->data;
	unsigned char* nptr = grey_img->data;

	for (int i = 0; i < size512 ; i++) {
		for (int j = 0; j < size512 ; j++) {
			*nptr = 0.11 * (float)*optr + 0.59 * (float)*(optr+1) + 0.3 * (float)*(optr+2);
			optr += 3;
			nptr += 1;
		}
	}

}

void displayImg(Mat* img, const char* name) {
	namedWindow(name);
	imshow(name, *img);
	waitKey(0);
	(* img).release();
	destroyWindow(name);
}

void histogram(int* data) {

}	 //todo

void statistic(Mat* img, int* data) {
	unsigned char* ptr = img->data;
	for (int i = 0; i < size512; i++) {
		for (int j = 0; j < size512; j++) {
			data[(int)*ptr] += 1;
			ptr += 1;
		}
	}
}

void balance(int* data, Mat* grey, Mat* balance) {
	int sum = 0;
	float p[256] = { 0 };
	float balance_range[256] = {0};
	for (int i = 0; i < 256; i++) {
		sum = 0;
		for (int j = i; j >= 0; j--) {
			sum += data[j];
		}
		p[i] = (float)sum / (float)(size512 * size512);
		balance_range[i] = p[i] * 255;
	}
	unsigned char* ptr1 = grey->data;
	unsigned char* ptr2 = balance->data;
	for (int i = 0; i < size512; i++) {
		for (int j = 0; j < size512; j++) {
			*ptr2 = balance_range[(int)*ptr1];
			ptr1++;
			ptr2++;
		}
	}
}

void linear_strech(int* data, Mat* grey, Mat* linear) {
	float min = 0, max = 0;
	for (int i = 0; i < 256; i++) {
		if (data[i] != 0) {
			min = i;
			break;
		}
	}
	for (int i = 255; i >= 0; i--) {
		if (data[i] != 0) {
			max = i;
			break;
		}
	}
	unsigned char* ptr1 = grey->data;
	unsigned char* ptr2 = linear->data;
	for (int i = 0; i < size512; i++) {
		for (int j = 0; j < size512; j++) {
			*ptr2 = (float)((*ptr1 - min)/(max-min)*(255-155))+155;
			ptr1++;
			ptr2++;
		}
	}
}

int main()
{
	Mat in_img;
	Mat grey_img(size512, size512, CV_8UC1), 
		balance_img(size512, size512, CV_8UC1),
		linear_img(size512, size512, CV_8UC1);
	int rows, colums = 0;
	int grey_num[256] = { 0 }, balance_num[256] = { 0 };


	//read img
	//in_img = imread("D:\\files\\北航\\大三下\\图像处理\\lenna.png",1);
	in_img = imread("D:\\files\\北航\\大三下\\图像处理\\snow.jpg", 1);
	rows = in_img.rows;
	colums = in_img.cols;

	//change2grey
	change2grey(&in_img, &grey_img);

	//statistic & histogram
	statistic(&grey_img, grey_num);

	//balance
	balance(grey_num, &grey_img, &balance_img);

	//linear_streach
	linear_strech(grey_num, &grey_img, &linear_img);


	//display
	displayImg(&in_img, "input");
	displayImg(&grey_img, "grey");
	displayImg(&balance_img, "balance");
	displayImg(&linear_img, "linear");

	return 0;
}