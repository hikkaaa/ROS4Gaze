#!/home/kai/miniforge3/envs/ros_env/bin/python3

from controller import Robot, Motor, Keyboard, Camera
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import numpy as np
import cv2

# Create the Robot instance.
robot = Robot()

# Get the time step of the current world.
timestep = 256

# Initialize and enable the camera
camera = robot.getDevice("camera")
camera.enable(timestep)

# Initialize the ROS node
rospy.init_node('webots_camera_publisher', anonymous=True)

# Create a ROS publisher for camera images
image_publisher = rospy.Publisher('/camera/image_raw', Image, queue_size=10)

# Initialize the CvBridge to convert between ROS and OpenCV images
bridge = CvBridge()

# Set up basic logging
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize motors and wheels
linear_motor = Motor("linear_motor")
rotational_motor = Motor("rotational_motor")

wheels = [None] * 4
wheels_names = ["wheel1", "wheel2", "wheel3", "wheel4"]
for i in range(4):
    wheels[i] = robot.getDevice(wheels_names[i])
    wheels[i].setPosition(float('inf'))
    wheels[i].setVelocity(0)

# Initialize the keyboard
kb = Keyboard()
kb.enable(timestep)

# Speed and rotation variables
left_speed = 0.0
right_speed = 0.0
linear = 0.0
horizontal_rotation = 0
vertical_rotation = 0

try:
    # Main control loop
    while robot.step(timestep) != -1 and not rospy.is_shutdown():
        
        # Get image from Webots camera
        image = camera.getImage()
        if image:
            # Convert it to an OpenCV image
            height = camera.getHeight()
            width = camera.getWidth()
            frame = np.frombuffer(image, np.uint8).reshape(height, width, 4)

            # Convert RGBA to BGR for OpenCV
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

            # Convert the image to a ROS message and publish it
            ros_image = bridge.cv2_to_imgmsg(frame, encoding="bgr8")
            image_publisher.publish(ros_image)

            # Log the info
            rospy.loginfo("Camera image published")
        else:
            logging.warning("Failed to receive image from camera.")
        
        # Check for keyboard inputs for robot movement
        key = kb.getKey()
        
        if key == Keyboard.UP:
            left_speed = 1.0
            right_speed = 1.0
        elif key == Keyboard.DOWN:
            left_speed = -1.0
            right_speed = -1.0
        elif key == Keyboard.LEFT:
            left_speed = 1.0
            right_speed = -1.0
        elif key == Keyboard.RIGHT:
            left_speed = -1.0
            right_speed = 1.0
        else:
            left_speed = 0.0
            right_speed = 0.0

        # Set wheels velocity based on keyboard input
        wheels[0].setVelocity(left_speed)
        wheels[2].setVelocity(right_speed)
        wheels[1].setVelocity(left_speed)
        wheels[3].setVelocity(right_speed)

        # Adjust linear motor based on 'U' and 'D'
        if key == ord("U") or key == ord("u"):
            linear += 0.005
        elif key == ord("D") or key == ord("d"):
            linear -= 0.005

        linear_motor.setPosition(linear)

        # Adjust rotational motor based on 'A', 'L', 'W', 'S'
        if key == ord("A") or key == ord("a") and horizontal_rotation < 1.57:
            horizontal_rotation += 0.005
        elif key == ord("L") or key == ord("l") and horizontal_rotation > 0:
            horizontal_rotation -= 0.005
        elif key == ord("W") or key == ord("w") and vertical_rotation < 1.57:
            vertical_rotation += 0.005
        elif key == ord("S") or key == ord("s") and vertical_rotation > -1.57:
            vertical_rotation -= 0.005
        
        rotational_motor.setPosition(horizontal_rotation)
        rotational_motor.setPosition(vertical_rotation)

except Exception as e:
    logging.error(f"An error occurred: {str(e)}")

finally:
    cv2.destroyAllWindows()
    rospy.signal_shutdown("Shutting down")

if __name__ == '__main__':
    rospy.spin()
