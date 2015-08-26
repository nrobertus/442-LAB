#include "OpenNI.h"
#include "iostream"
#include <opencv2/core/core.hpp> // Basic OpenCV structures (cv::Mat, Scalar)
#include <opencv2/highgui/highgui.hpp> 
#include <opencv2/imgproc/imgproc.hpp>
#include <stdio.h>
#include "NiTE.h"

#define width 320
#define height 240
#define LINE_THICKNESS 10

cv::Mat frame;
cv::Mat newFrame;
openni::VideoStream depth;
openni::RGB888Pixel *pColor;

void SwapPixels(int x1, int y1, int x2, int y2) {
	if (x1 < 0 || x1 >= width || y1 < 0 || y1 >= height || x2 < 0 || x2 >= width || y2 < 0 || y2 >= height) {
		return;
	}
	for (int y = 0; y < 2; y++) {
		if (y1 + y >= height || y2 + y >= height) {
			break;
		}
		openni::RGB888Pixel pix1 = pColor[frame.cols*(y1 + y) + x1];
		openni::RGB888Pixel pix2 = pColor[frame.cols*(y2 + y) + x2];
		newFrame.at<cv::Vec3b>((y1 + y), x1) = cv::Vec3b(pix2.b, pix2.g, pix2.r);
		newFrame.at<cv::Vec3b>((y2 + y), x2) = cv::Vec3b(pix1.b, pix1.g, pix1.r);
	}
}

void SwapHeads(nite::UserTracker* pUserTracker, const nite::Array<nite::UserData>& users) {
	openni::VideoFrameRef dep;
	depth.readFrame(&dep);
	openni::DepthPixel* pDepth = (openni::DepthPixel *) dep.getData();
	const nite::SkeletonJoint& joint1 = users[0].getSkeleton().getJoint(nite::JOINT_HEAD);
	const nite::SkeletonJoint& joint2 = users[1].getSkeleton().getJoint(nite::JOINT_HEAD);
	if (joint1.getPositionConfidence() < 0.5f || joint2.getPositionConfidence() < 0.5f) {
		return;
	}
	float head1Coords[2];
	float head2Coords[2];

	pUserTracker->convertJointCoordinatesToDepth(joint1.getPosition().x, joint1.getPosition().y, joint1.getPosition().z, &head1Coords[0], &head1Coords[1]);
	pUserTracker->convertJointCoordinatesToDepth(joint2.getPosition().x, joint2.getPosition().y, joint2.getPosition().z, &head2Coords[0], &head2Coords[1]);
	cv::Point head1(head1Coords[0], head1Coords[1]);
	cv::Point head2(head2Coords[0], head2Coords[1]);
	if (head1.x < 0 || head1.x >= width || head1.y < 0 || head1.y >= height || head2.x < 0 || head2.x >= width || head2.y < 0 || head2.y >= height) {
		return;
	}
	int previousDepth = pDepth[width*head1.y + head1.x];
	int currentDepth = previousDepth;
	int topOfHead, leftOfHead, rightOfHead, bottomOfHead;
	for (int i = head1.y; i >= 0; i--) {
		if (abs(currentDepth - previousDepth) > 200 && currentDepth != 0) {
			topOfHead = i;
			//std::cout << "Y: " << i << " Depth: " << currentDepth << std::endl;
			break;
		}
		//std::cout << "Y: " << i << " Depth: " << currentDepth << std::endl;
		previousDepth = currentDepth;
		while ((currentDepth = pDepth[width*i + head1.x]) == 0) { i--; }
	}

	previousDepth = pDepth[width*head1.y + head1.x];
	currentDepth = previousDepth;
	for (int i = head1.x; i >= 0; i--) {
		if (abs(currentDepth - previousDepth) > 200 && currentDepth != 0) {
			leftOfHead = i;
			//std::cout << "X: " << i << " Depth: " << currentDepth << std::endl;
			break;
		}
		//std::cout << "X: " << i << " Depth: " << currentDepth << std::endl;
		previousDepth = currentDepth;
		while ((currentDepth = pDepth[width*head1.y + i]) == 0) { i--; }
	}

	previousDepth = pDepth[width*head1.y + head1.x];
	currentDepth = previousDepth;
	for (int i = head1.x; i < width; i++) {
		if (abs(currentDepth - previousDepth) > 200 && currentDepth != 0) {
			rightOfHead = i;
			//std::cout << "X: " << i << " Depth: " << currentDepth << std::endl;
			break;
		}
		//std::cout << "X: " << i << " Depth: " << currentDepth << std::endl;
		previousDepth = currentDepth;
		while ((currentDepth = pDepth[width*head1.y + i]) == 0) { i++; }
	}

	previousDepth = pDepth[width*head1.y + head1.x];
	currentDepth = previousDepth;
	for (int i = head1.y; i < height; i++) {
		if (abs(currentDepth - previousDepth) > 20 && currentDepth != 0) {
			bottomOfHead = i;
			//std::cout << "Y: " << i << " Depth: " << currentDepth << std::endl;
			break;
		}
		//std::cout << "Y: " << i << " Depth: " << currentDepth << std::endl;
		previousDepth = currentDepth;
		while ((currentDepth = pDepth[width*i + head1.x]) == 0) { i++; }
	}
	std::cout << bottomOfHead << std::endl;
	if (bottomOfHead > head1.y + 50 || bottomOfHead < 0) {
		bottomOfHead = head1.y + (abs(head1.y - topOfHead));
	}
	if (topOfHead < 0 || topOfHead >= height || leftOfHead < 0 || leftOfHead >= width) {
		return;
	}

	for (int i = topOfHead; i < topOfHead + 6; i++) {
		for (int j = leftOfHead; j < leftOfHead + 6; j++) {
			frame.at<cv::Vec3b>(i, j) = cv::Vec3b(255, 255, 255);
		}
	}

	bool headFound = false;
	previousDepth = pDepth[width*topOfHead + leftOfHead];
	currentDepth = previousDepth;
	for (int i = topOfHead; i < bottomOfHead; i++) {
		previousDepth = pDepth[width*i + leftOfHead];
		currentDepth = previousDepth;
		for (int j = leftOfHead; j < rightOfHead; j++) {
			switch (headFound) {
			case true:
				if (abs(previousDepth - currentDepth) > 200 && currentDepth != 0) {
					headFound = false;
					j = rightOfHead;
					continue;
				}
				else {
					SwapPixels(j, i, head2.x - (head1.x - j), head2.y - (head1.y - i));
				}
				break;

			case false:
				if (abs(previousDepth - currentDepth) > 200 && currentDepth != 0) {
					headFound = true;
					SwapPixels(j, i, head2.x - (head1.x - j), head2.y - (head1.y - i));
				}
				break;
			}
			previousDepth = currentDepth;
			currentDepth = pDepth[width*i + j];
		}
	}
}
/* from sample code */
void DrawLimb(nite::UserTracker* pUserTracker, const nite::SkeletonJoint& joint1, const nite::SkeletonJoint& joint2, int thickness, int user)
{
	printf("userID: %d\n", user);
	float coordinates[6] = { 0 };
	pUserTracker->convertJointCoordinatesToDepth(joint1.getPosition().x, joint1.getPosition().y, joint1.getPosition().z, &coordinates[0], &coordinates[1]);
	pUserTracker->convertJointCoordinatesToDepth(joint2.getPosition().x, joint2.getPosition().y, joint2.getPosition().z, &coordinates[3], &coordinates[4]);
	if (joint1.getPositionConfidence() > 0.5f && joint2.getPositionConfidence() > 0.5f)
	{
		if (user == 1){
			cv::line(newFrame, cv::Point((int)coordinates[0], (int)coordinates[1]), cv::Point((int)coordinates[3], (int)coordinates[4]), cv::Scalar(0, 0, 255), thickness);
		}
		else if(user == 2){
			cv::line(newFrame, cv::Point((int)coordinates[0], (int)coordinates[1]), cv::Point((int)coordinates[3], (int)coordinates[4]), cv::Scalar(0, 255, 0), thickness);
		}
		else{
			cv::line(newFrame, cv::Point((int)coordinates[0], (int)coordinates[1]), cv::Point((int)coordinates[3], (int)coordinates[4]), cv::Scalar(120, 120, 120), thickness);
		}
		
	}
}
/* from sample code */
void DrawSkeleton(nite::UserTracker* pUserTracker, const nite::UserData& userData)
{
	//DrawLimb(pUserTracker, userData.getSkeleton().getJoint(nite::JOINT_HEAD), userData.getSkeleton().getJoint(nite::JOINT_NECK), LINE_THICKNESS, userData.getId());

	DrawLimb(pUserTracker, userData.getSkeleton().getJoint(nite::JOINT_LEFT_SHOULDER), userData.getSkeleton().getJoint(nite::JOINT_LEFT_ELBOW), LINE_THICKNESS, userData.getId());
	DrawLimb(pUserTracker, userData.getSkeleton().getJoint(nite::JOINT_LEFT_ELBOW), userData.getSkeleton().getJoint(nite::JOINT_LEFT_HAND), LINE_THICKNESS, userData.getId());

	DrawLimb(pUserTracker, userData.getSkeleton().getJoint(nite::JOINT_RIGHT_SHOULDER), userData.getSkeleton().getJoint(nite::JOINT_RIGHT_ELBOW), LINE_THICKNESS, userData.getId());
	DrawLimb(pUserTracker, userData.getSkeleton().getJoint(nite::JOINT_RIGHT_ELBOW), userData.getSkeleton().getJoint(nite::JOINT_RIGHT_HAND), LINE_THICKNESS, userData.getId());

	DrawLimb(pUserTracker, userData.getSkeleton().getJoint(nite::JOINT_LEFT_SHOULDER), userData.getSkeleton().getJoint(nite::JOINT_RIGHT_SHOULDER), LINE_THICKNESS, userData.getId());

	DrawLimb(pUserTracker, userData.getSkeleton().getJoint(nite::JOINT_LEFT_SHOULDER), userData.getSkeleton().getJoint(nite::JOINT_LEFT_HIP), LINE_THICKNESS, userData.getId());
	DrawLimb(pUserTracker, userData.getSkeleton().getJoint(nite::JOINT_RIGHT_SHOULDER), userData.getSkeleton().getJoint(nite::JOINT_RIGHT_HIP), LINE_THICKNESS, userData.getId());

	//DrawLimb(pUserTracker, userData.getSkeleton().getJoint(nite::JOINT_TORSO), userData.getSkeleton().getJoint(nite::JOINT_LEFT_HIP), LINE_THICKNESS, userData.getId());
	//DrawLimb(pUserTracker, userData.getSkeleton().getJoint(nite::JOINT_TORSO), userData.getSkeleton().getJoint(nite::JOINT_RIGHT_HIP), LINE_THICKNESS, userData.getId());
	
	//DrawLimb(pUserTracker, userData.getSkeleton().getJoint(nite::JOINT_TORSO), userData.getSkeleton().getJoint(nite::JOINT_LEFT_SHOULDER), LINE_THICKNESS, userData.getId());
	//DrawLimb(pUserTracker, userData.getSkeleton().getJoint(nite::JOINT_TORSO), userData.getSkeleton().getJoint(nite::JOINT_RIGHT_SHOULDER), LINE_THICKNESS, userData.getId());

	DrawLimb(pUserTracker, userData.getSkeleton().getJoint(nite::JOINT_LEFT_HIP), userData.getSkeleton().getJoint(nite::JOINT_RIGHT_HIP), LINE_THICKNESS, userData.getId());


	DrawLimb(pUserTracker, userData.getSkeleton().getJoint(nite::JOINT_LEFT_HIP), userData.getSkeleton().getJoint(nite::JOINT_LEFT_KNEE), LINE_THICKNESS, userData.getId());
	DrawLimb(pUserTracker, userData.getSkeleton().getJoint(nite::JOINT_LEFT_KNEE), userData.getSkeleton().getJoint(nite::JOINT_LEFT_FOOT), LINE_THICKNESS, userData.getId());

	DrawLimb(pUserTracker, userData.getSkeleton().getJoint(nite::JOINT_RIGHT_HIP), userData.getSkeleton().getJoint(nite::JOINT_RIGHT_KNEE), LINE_THICKNESS, userData.getId());
	DrawLimb(pUserTracker, userData.getSkeleton().getJoint(nite::JOINT_RIGHT_KNEE), userData.getSkeleton().getJoint(nite::JOINT_RIGHT_FOOT), LINE_THICKNESS, userData.getId());
}


int main(int argc, char* argv[])
{

	int c = 100;
	openni::Status rc = openni::STATUS_OK;
	openni::Device device;
	openni::VideoStream color;
	openni::VideoFrameRef pFrame, dep;
	nite::UserTracker* m_pUserTracker;
	openni::Device		m_device;
	nite::UserTrackerFrameRef userTrackerFrame;

	const char* deviceURI = openni::ANY_DEVICE;
	for (int i = 1; i < argc - 1; ++i)
	{
		if (strcmp(argv[i], "-device") == 0)
		{
			deviceURI = argv[i + 1];
			break;
		}
	}

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

	rc = m_device.open(deviceURI);
	if (rc != openni::STATUS_OK)
	{
		printf("Failed to open device\n%s\n", openni::OpenNI::getExtendedError());
		return rc;
	}

	nite::NiTE::initialize();

	m_pUserTracker = new nite::UserTracker;

	if (m_pUserTracker->create() != nite::STATUS_OK) {
		return nite::STATUS_ERROR;
	}

	cv::namedWindow("OpenCV", 1);
	frame = cv::Mat(cv::Size(width, height), CV_8UC3);
	newFrame = cv::Mat(cv::Size(width, height), CV_8UC3);

	cv::Mat finish = cv::Mat(cv::Size(width, height), CV_8UC3);
	int totalLeftDepth = 0;
	int alc = 0;
	int totalCenterDepth = 0;
	int acc = 0;
	int totalRightDepth = 0;
	int arc = 0;

	int cameraRow = 0; //the row of pixels that will be used for the depths
	int sameRowDepthCount = 0;

	int ignoreDepth = 1600; //Ignore all values after 4ft

	float objectDepths[10];
	int runningTotal = 0;
	int runningCount = 0;
	int objectCount = 0;
	bool foundObject = false;

	while (1)
	{
		nite::Status rc = m_pUserTracker->readFrame(&userTrackerFrame);
		color.readFrame(&pFrame);
		depth.readFrame(&dep);
		pColor = (openni::RGB888Pixel *) pFrame.getData();
		openni::DepthPixel* pDepth = (openni::DepthPixel *) dep.getData();
		for (int i = 0; i < frame.rows; i++) {
			for (int j = 0; j < frame.cols; j++) {
				openni::RGB888Pixel pix = pColor[frame.cols*i + j];
				frame.at<cv::Vec3b>(i, j) = cv::Vec3b(pix.b, pix.g, pix.r);
				newFrame.at<cv::Vec3b>(i, j) = cv::Vec3b(0, 0, 0);
			}
		}

		const nite::Array<nite::UserData>& users = userTrackerFrame.getUsers();
		for (int i = 0; i < users.getSize(); ++i)
		{
			const nite::UserData& user = users[i];

			if (user.isNew())
			{
				m_pUserTracker->startSkeletonTracking(user.getId());
			}
			else if (!user.isLost())
			{
				if (users[i].getSkeleton().getState() == nite::SKELETON_TRACKED)
				{
					if (i == 1) {
						SwapHeads(m_pUserTracker, users);
					}
					DrawSkeleton(m_pUserTracker, user);		
				}
			}
		}

		c = cv::waitKey(10);
		if (c == 112) {
			printf("Objects: %d\n", objectCount);
			for (int y = 0; y < objectCount; y++) {
				std::cout << "Object " << (y + 1) << " Avg Depth: " << objectDepths[y] << std::endl;
			}
		}

		cv::imshow("newFrame", newFrame);
		cv::imshow("depth", frame);
		c = cv::waitKey(10);
		if (c == 27)
			break;
	}

	return 0;

}