#!/home/kai/miniforge3/envs/ros_env/bin/python3

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import numpy as np
import cv2

# Initialize the ROS node
rospy.init_node('webcam_publisher', anonymous=True)

# Create a ROS publisher for camera images
image_publisher = rospy.Publisher('/camera/image_raw', Image, queue_size=10)

# Initialize the CvBridge to convert between ROS and OpenCV images
bridge = CvBridge()

# Set up basic logging
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Open a connection to the webcam
cap = cv2.VideoCapture('/dev/media0')

if not cap.isOpened():
    logging.error("Error: Could not open webcam.")
    exit()

try:
    # Main control loop
    while not rospy.is_shutdown():
        ret, frame = cap.read()
        if ret:
            # Convert the image to a ROS message and publish it
            ros_image = bridge.cv2_to_imgmsg(frame, encoding="bgr8")
            image_publisher.publish(ros_image)

            # Log the info
            rospy.loginfo("Webcam image published")

            # Display the image for debugging purposes (optional)
            cv2.imshow('Webcam', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            logging.warning("Failed to receive image from webcam.")
        
except Exception as e:
    logging.error(f"An error occurred: {str(e)}")

finally:
    cap.release()
    cv2.destroyAllWindows()
    rospy.signal_shutdown("Shutting down")

if __name__ == '__main__':
    rospy.spin()

