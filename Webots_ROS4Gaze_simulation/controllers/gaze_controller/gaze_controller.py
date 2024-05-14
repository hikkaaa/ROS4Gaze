#!/home/kai/miniforge3/envs/ros_env/bin/python3

"""yaw_controller controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot, Motor, Supervisor, Node
import math

# Set up basic logging
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# create the Robot instance.
supervisor = Supervisor()

# get the time step of the current world.
timestep = 256

# YAW_ANGLE = 20 
# PITCH_ANGLE = 30


cone = supervisor.getFromDef("gaze_tracker")

object = supervisor.getFromDef("ball")
    
cone.enableContactPointsTracking(timestep)


while supervisor.step(timestep) != -1:
    # Retrieve contact points for the object
    cone_contacts = cone.getContactPoints()
    
    if cone_contacts:
        print("Contact Detected.")
        print("Contact point location:", object.getPosition())
    else:
        print("No contact points detected")
    

        

# p_motor = supervisor.getDevice('pitch_gaze')
# y_motor = supervisor.getDevice('yaw_gaze')

# while supervisor.step(timestep) != -1:

    # p_motor.setPosition(math.radians(PITCH_ANGLE))
    # y_motor.setPosition(math.radians(YAW_ANGLE))

    # pass
# Enter here exit cleanup code.


