// ConsoleApplication1.cpp : Defines the entry point for the console application.
//
#define _CRT_SECURE_NO_WARNINGS

#include <tchar.h>
#include "OpenNI.h"
#include "iostream"
#include <opencv2/core/core.hpp> // Basic OpenCV structures (cv::Mat, Scalar)
#include <opencv2/highgui/highgui.hpp> 
#include <opencv2/imgproc/imgproc.hpp>
#include "NiTE.h"

/*******************************************************************************
*                                                                              *
*   PrimeSense NiTE 2.0 - Simple Skeleton Sample                               *
*   Copyright (C) 2012 PrimeSense Ltd.                                         *
*                                                                              *
*******************************************************************************/

#include "NiTE.h"

#include "C:/Program Files (x86)/PrimeSense/NiTE2/Samples/Common/NiteSampleUtilities.h"

#define MAX_USERS 10
bool g_visibleUsers[MAX_USERS] = { false };
nite::SkeletonState g_skeletonStates[MAX_USERS] = { nite::SKELETON_NONE };

#define USER_MESSAGE(msg) \
	{printf("[%08llu] User #%d:\t%s\n",ts, user.getId(),msg);}

void updateUserState(const nite::UserData& user, unsigned long long ts)
{
	if (user.isNew())
		USER_MESSAGE("New")
	else if (user.isVisible() && !g_visibleUsers[user.getId()])
	USER_MESSAGE("Visible")
	else if (!user.isVisible() && g_visibleUsers[user.getId()])
	USER_MESSAGE("Out of Scene")
	else if (user.isLost())
	USER_MESSAGE("Lost")

	g_visibleUsers[user.getId()] = user.isVisible();


	if (g_skeletonStates[user.getId()] != user.getSkeleton().getState())
	{
		switch (g_skeletonStates[user.getId()] = user.getSkeleton().getState())
		{
		case nite::SKELETON_NONE:
			USER_MESSAGE("Stopped tracking.")
				break;
		case nite::SKELETON_CALIBRATING:
			USER_MESSAGE("Calibrating...")
				break;
		case nite::SKELETON_TRACKED:
			USER_MESSAGE("Tracking!")
				break;
		case nite::SKELETON_CALIBRATION_ERROR_NOT_IN_POSE:
		case nite::SKELETON_CALIBRATION_ERROR_HANDS:
		case nite::SKELETON_CALIBRATION_ERROR_LEGS:
		case nite::SKELETON_CALIBRATION_ERROR_HEAD:
		case nite::SKELETON_CALIBRATION_ERROR_TORSO:
			USER_MESSAGE("Calibration Failed... :-|")
				break;
		}
	}
}



int _tmain(int argc, _TCHAR* argv[])
{

	/*
		OPENNI SETUP STUFF
	*/
	nite::UserTracker userTracker;
	nite::Status niteRc;

	nite::NiTE::initialize();

	niteRc = userTracker.create();
	if (niteRc != nite::STATUS_OK)
	{
		printf("Couldn't create user tracker\n");
		return 3;
	}
	printf("\nStart moving around to get detected...\n(PSI pose may be required for skeleton calibration, depending on the configuration)\n");

	nite::UserTrackerFrameRef userTrackerFrame;


	/*
		OPENCV SETUP STUFF
	*/
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
	// min and max vals for z range
	int minZ = 0;
	int maxZ = 5000;

	// scale for gradiant
	float scaleZ = (255.0 / float(maxZ));

	// counter for printing off depth pixles
	int counter = 0;


	while (!wasKeyboardHit())
	{
		
		/*
			OPEN CV STUFF - OUR WORKING CODE
		*/
		// set up depth and color arrays for each new image
		color.readFrame(&pFrame);
		depth.readFrame(&dep);	
		openni::RGB888Pixel *pColor = (openni::RGB888Pixel *) pFrame.getData();
		openni::DepthPixel* pDepth = (openni::DepthPixel *) dep.getData();


		/* PRINT OFF DEPTH OF point and middle bottom of screen

		// Code for printing off depth at 20 and 40 pixles up from the bottom of the image
		// All of this data varies too much to be of any real value to us as far as i can tell
		counter++;
		// This will keep it from printing off too much data
		if (counter == 10){
			counter = 0;
			// get depth at 20 pixles up
			openni::DepthPixel depthOne = pDepth[(frame.cols * 200) + 120];
			// get depth at 40 pixles up
			openni::DepthPixel depthTwo = pDepth[(frame.cols * 220) + 120];
			// get difference
			int difference = depthOne - depthTwo;
			printf("depthOne %d\ndepthTwo %d\ndifference %d\n\n", depthOne, depthTwo, difference);
		}
		*/
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
				copy.at<cv::Vec3b>(frame.rows - 20, 160) = cv::Vec3b(0, 0, 255);
				copy.at<cv::Vec3b>(frame.rows - 40, 160) = cv::Vec3b(0, 0, 255);

				//This is hunter's code
				/*
				openni::RGB888Pixel pix = pColor[frame.cols*i + j];
				frame.at<cv::Vec3b>(i, j) = cv::Vec3b(pix.r, pix.g, pix.b);
				bw = cv::Mat(cv::Size(320, 240), CV_16UC1, (void*)pDepth);
				*/

			}

		}
		/*
		OPENNI STUFF
		*/
		niteRc = userTracker.readFrame(&userTrackerFrame);
		if (niteRc != nite::STATUS_OK)
		{
			printf("Get next frame failed\n");
			continue;
		}

		const nite::Array<nite::UserData>& users = userTrackerFrame.getUsers();
		for (int i = 0; i < users.getSize(); ++i)
		{
			const nite::UserData& user = users[i];
			updateUserState(user, userTrackerFrame.getTimestamp());
			if (user.isNew())
			{
				userTracker.startSkeletonTracking(user.getId());
			}
			else if (user.getSkeleton().getState() == nite::SKELETON_TRACKED)
			{
				const nite::SkeletonJoint& head = user.getSkeleton().getJoint(nite::JOINT_HEAD);
				if (head.getPositionConfidence() > .5)
					printf("%d. (%5.2f, %5.2f, %5.2f)\n", user.getId(), ((1280 / 2) + head.getPosition().x)*.25, ((1024 / 2) + head.getPosition().y)*.234, head.getPosition().z);
					cv::circle(frame, cv::Point((int)((1280/2)+head.getPosition().x)*0.25, 240-((int)((1024/2)+head.getPosition().y))*0.234), 10, (255, 0, 0), 1, 8, 0);
			}
		}
		
		// display painted images
		cv::imshow("depth", frame);
		cv::imshow("color", copy);
		cv::imshow("niteFrame", niteRc);

		// Code for exit
		c = cv::waitKey(10);
		if (c == 27)
			break;
	}
	// Shut down nite
	nite::NiTE::shutdown();
	return 0;

}
