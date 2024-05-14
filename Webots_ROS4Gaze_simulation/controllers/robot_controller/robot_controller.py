"""robot_controller_PYTHON controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot, Motor, Keyboard, InertialUnit, Camera

# create the Robot instance.
robot = Robot()

linear_actuator = Motor("linear motor")
rotational_motor = Motor("rotational motor")

    
# get the time step of the current world.
timestep = 256
    
kb = Keyboard()
kb.enable(timestep)

camera = robot.getCamera("camera")
camera.enable(timestep)
    
wheels = [None] * 4
wheels_names = ["wheel1", "wheel2", "wheel3", "wheel4"]
for i in range(4):
    wheels[i] = robot.getMotor(wheels_names[i])
    wheels[i].setPosition(float('inf'))
    wheels[i].setVelocity(0)

left_speed = 0.0
right_speed = 0.0
linear = 0.0
rotation = 0.0
    
while robot.step(timestep) != -1:
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

    wheels[0].setVelocity(left_speed)
    wheels[2].setVelocity(right_speed)
    wheels[1].setVelocity(left_speed)
    wheels[3].setVelocity(right_speed)

    if key == ord("U") or key == ord("u"):
        linear += 0.005
    elif key == ord("D") or key == ord("d"):
        linear -= 0.005
    else:
        linear += 0
        
    linear_actuator.setPosition(linear)
    
    if key == ord("A") or key == ord("a") and rotation < 1.57:
       rotation += 0.005
    elif key == ord("L") or key == ord("l") and rotation > 0:
        rotation -= 0.005  
    else:
        rotation += 0
    
    rotational_motor.setPosition(rotation)
        
        
        
        #print("X:", gp.getValues()[0])
        #print("Y:", gp.getValues()[1])
        #print("Z:", gp.getValues()[2])
        

