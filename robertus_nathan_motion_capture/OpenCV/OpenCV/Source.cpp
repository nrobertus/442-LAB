// ConsoleApplication1.cpp : Defines the entry point for the console application.
//
#define _CRT_SECURE_NO_WARNINGS

#include <tchar.h>
#include <opencv2/core/core.hpp> // Basic OpenCV structures (cv::Mat, Scalar)
#include <opencv2/highgui/highgui.hpp> 
#include <opencv2/imgproc/imgproc.hpp> 
using namespace cv;
using namespace std;


int main(int argc, char* argv[])
{

	
    VideoCapture cap(1);
    Mat frame1;
    cap.read(frame1);
	Mat frame;
	Mat original;

    Mat gray = cv::Mat(frame1.size(), CV_8UC1);
	Mat color = cv::Mat(frame1.size(), CV_32FC3);
	Mat image1 = frame1.clone();
	Mat diff = cv::Mat(frame1.size(), CV_8UC3);

	frame1.convertTo(color, CV_32F);
	frame.copyTo(image1);
	frame.copyTo(diff);

    while(1){

        cap.read(frame);
		cap.read(original);

		Mat HSV;
		Mat threshold;
		Mat edges;

		Scalar hsv_min = cvScalar(0, 200, 170, 0);
		Scalar hsv_max = cvScalar(200, 250, 256, 0);
		cvtColor(frame, HSV, CV_BGR2HSV);
		inRange(HSV, hsv_min, hsv_max, threshold);
		GaussianBlur(threshold, threshold, Size(7, 7), 1.5);
		Canny(threshold, edges, 10, 350, 3, false);

		imshow("thr", threshold);
		imshow("original", HSV);
		imshow("edges", edges);

		moveWindow("original", 100, 150);
		moveWindow("thr", 800, 150);


        waitKey(1);
    }
}
