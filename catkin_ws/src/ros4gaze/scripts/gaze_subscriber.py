#!/home/kai/miniforge3/envs/ros_env/bin/python3

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
from l2cs import Pipeline, render
import os
import torch
import threading
import logging

# Load the model for gaze detection
downloaded_file = os.path.expanduser('~/Downloads/L2CSNet_gaze360.pkl')
gaze_pipeline = Pipeline(
    weights=downloaded_file,
    arch='ResNet50',
    device=torch.device('cpu')  # Adjust to 'gpu' if available and supported
)

def gaze_detection(data):
    bridge = CvBridge()
    try:
        current_frame = bridge.imgmsg_to_cv2(data, "bgr8")
        if current_frame is None or current_frame.size == 0:
            logging.error("Received an empty or invalid frame.")
            return
        logging.info(f"Processing frame of shape {current_frame.shape}")
        
        # Apply gaze algorithm on current frame
        gaze_results = gaze_pipeline.step(current_frame)
        
        # Use data from gaze_results to process the image
        if gaze_results:
            # Print pitch, yaw, and scores
            print("Pitch:", gaze_results.pitch)
            print("Yaw:", gaze_results.yaw)
            print("Scores:", gaze_results.scores)
            
            # Example: Use bounding boxes and landmarks for some processing
            for bbox, landmark in zip(gaze_results.bboxes, gaze_results.landmarks):
                # Draw bounding boxes and landmarks on the frame
                # Assuming bounding box format: [x, y, width, height]
                cv2.rectangle(current_frame, (int(bbox[0]), int(bbox[1])), 
                              (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3])), 
                              (0, 255, 0), 2)
                # Assuming landmarks are (x, y) points
                for point in landmark.reshape(-1, 2):
                    cv2.circle(current_frame, (int(point[0]), int(point[1])), 5, (0, 0, 255), -1)

        # Display image
        cv2.imshow('Webcam', current_frame)
        cv2.waitKey(1)
    except Exception as e:
        logging.error(f"Error processing frame: {str(e)}")

def main():
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Initialize the ROS node in the main thread
    rospy.init_node('webcam_gaze_subscriber', anonymous=True)

    # Set up subscriber
    rospy.Subscriber('/camera/image_raw', Image, gaze_detection)

    try:
        # Run the ROS spin loop
        rospy.spin()
    except KeyboardInterrupt:
        rospy.signal_shutdown("Subscriber node shut down gracefully")
    finally:
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

	
