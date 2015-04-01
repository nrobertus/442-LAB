// ConsoleApplication1.cpp : Defines the entry point for the console application.
//
#define _CRT_SECURE_NO_WARNINGS

#include <tchar.h>
#include "OpenNI.h"
#include "iostream"
#include <opencv2/core/core.hpp> // Basic OpenCV structures (cv::Mat, Scalar)
#include <opencv2/highgui/highgui.hpp> 
#include <opencv2/imgproc/imgproc.hpp>
//#include "NiTE.h"


int _tmain(int argc, _TCHAR* argv[])
{

	int c = 100;
	openni::Status rc = openni::STATUS_OK;
	openni::Device device;
	openni::VideoStream depth, color;
	openni::VideoFrameRef pFrame, dep;

	const char* deviceURI = openni::ANY_DEVICE;

	rc = openni::OpenNI::initialize();

	printf("After initialization:\n%s\n", openni::OpenNI::getExtendedError());

	rc = device.open(deviceURI);
	if (rc != openni::STATUS_OK)
	{

		int a = 0;
		printf("SimpleViewer: Device open failed:\n%s\n", openni::OpenNI::getExtendedError());
		openni::OpenNI::shutdown();
		std::cin >> a;
		return 1;

	}

	rc = depth.create(device, openni::SENSOR_DEPTH);

	if (rc == openni::STATUS_OK)

	{

		rc = depth.start();
		if (rc != openni::STATUS_OK)
		{
			printf("SimpleViewer: Couldn't start depth stream:\n%s\n", openni::OpenNI::getExtendedError());
			depth.destroy();
		}
	}
	else
	{
		printf("SimpleViewer: Couldn't find depth stream:\n%s\n", openni::OpenNI::getExtendedError());
	}

	rc = color.create(device, openni::SENSOR_COLOR);
	if (rc == openni::STATUS_OK)
	{
		rc = color.start();
		if (rc != openni::STATUS_OK)
		{
			printf("SimpleViewer: Couldn't start color stream:\n%s\n", openni::OpenNI::getExtendedError());
			color.destroy();
		}
	}
	else
	{
		printf("SimpleViewer: Couldn't find color stream:\n%s\n", openni::OpenNI::getExtendedError());
	}

	if (!depth.isValid() || !color.isValid())
	{
		printf("SimpleViewer: No valid streams. Exiting\n");
		openni::OpenNI::shutdown();
		return 2;
	}
	cv::namedWindow("OpenCV", 1);

	// Set up mats
	cv::Mat frame = cv::Mat(cv::Size(320, 240), CV_8UC3);
	cv::Mat copy = cv::Mat(cv::Size(320, 240), CV_8UC3);
	cv::Mat bw = cv::Mat(cv::Size(320,240), CV_16UC1);
	cv::Mat bw;

	// min and max vals for z range
	int minZ = 200;
	int maxZ = 3500;

	// scale for gradiant
	float scaleZ = (255.0 / float(maxZ));

	// counter for printing off depth pixles
	int counter = 0;

	while (1)
	{
		// set up depth and color arrays for each new image
		color.readFrame(&pFrame);
		depth.readFrame(&dep);	
		openni::RGB888Pixel *pColor = (openni::RGB888Pixel *) pFrame.getData();
		openni::DepthPixel* pDepth = (openni::DepthPixel *) dep.getData();

		// Code for printing off depth at 20 and 40 pixles up from the bottom of the image
		// All of this data varies too much to be of any real value to us as far as i can tell
		counter++;
		// This will keep it from printing off too much data
		if (counter == 10){
			counter = 0;
			// get depth at 20 pixles up
			openni::DepthPixel depthOne = pDepth[frame.cols * 300 + 120];
			// get depth at 40 pixles up
			openni::DepthPixel depthTwo = pDepth[frame.cols * 280 + 120];
			// get difference
			int difference = depthOne - depthTwo;
			printf("depthOne %d\ndepthTwo %d\ndifference %d\n\n", depthOne, depthTwo, difference);
		}

		// Put all of the mat painting in this double for loop
		for (int i = 0; i<frame.rows; i++)
		{
			for (int j = 0; j<frame.cols; j++)
			{
				// get depth and pixle color at pixle i, j. 
				openni::DepthPixel dep = pDepth[frame.cols*i + j];
				openni::RGB888Pixel pix = pColor[frame.cols*i + j];

				/*
				//Our non- working solution for detecting objects
				if (i > 20){
					openni::DepthPixel dep2 = pDepth[frame.cols*(i-20) + j];
					// check to see if pixle is on the floor or off
					if (dep < (dep2 - 45) && dep >(dep2 + 45)){
						// if in range, paint color of pixle from camera
						frame.at<cv::Vec3b>(i, j) = cv::Vec3b(pix.b, pix.g, pix.r);
						copy.at<cv::Vec3b>(i, j) = cv::Vec3b(pix.b, pix.g, pix.r);
					}
					else {
						// else, paint red 
						frame.at<cv::Vec3b>(i, j) = cv::Vec3b(100, 100, 255);
						copy.at<cv::Vec3b>(i, j) = cv::Vec3b(100, 100, 255);
					}
				}
				*/

				//This is our code for the gradiant depth.
				
				if (dep >= minZ && dep < maxZ){
					// If in range, paint the pixles on frame and gradiant on copu
					frame.at<cv::Vec3b>(i, j) = cv::Vec3b(pix.b, pix.g, pix.r);
					copy.at<cv::Vec3b>(i, j) = cv::Vec3b((256 - int(scaleZ*dep)), (256 - int(scaleZ*dep)), (256 - int(scaleZ*dep)));
				}
				else{
					// If not in range, paint black on both
					frame.at<cv::Vec3b>(i, j) = cv::Vec3b(0, 0, 0);
					copy.at<cv::Vec3b>(i, j) = cv::Vec3b(0, 0, 0);
				}
				

				//This is hunter's code
				/*
				openni::RGB888Pixel pix = pColor[frame.cols*i + j];
				frame.at<cv::Vec3b>(i, j) = cv::Vec3b(pix.r, pix.g, pix.b);
				bw = cv::Mat(cv::Size(320, 240), CV_16UC1, (void*)pDepth);
				*/
			}

		}

		// display painted images
		cv::imshow("depth", frame);
		cv::imshow("color", copy);

		// Code for exit
		c = cv::waitKey(10);
		if (c == 27)
			break;
	}
	return 0;

}
