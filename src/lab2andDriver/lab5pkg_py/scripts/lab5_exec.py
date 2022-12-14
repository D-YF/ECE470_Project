#!/usr/bin/env python

import sys
import copy
import time
import rospy

import numpy as np
from lab5_header import *
from lab5_func import *
from blob_search import *


# ========================= Student's code starts here =========================

# Position for UR3 not blocking the camera
go_away = [270*PI/180.0, -90*PI/180.0, 90*PI/180.0, -90*PI/180.0, -90*PI/180.0, 135*PI/180.0]

# Store world coordinates of green and yellow blocks
xw_yw_G = []
xw_yw_Y = []
xw_yw_R = []
xw_yw_B = [0.3+0.06, 0.2-0.05]

# target position in world coordinates
target_xy_w_G = [0.25 , 0.3]
target_xy_w_Y = [0.15 , 0.3]
target_xy_w_R = [0.4 , 0.35]
task_not_com = 4
is_green_red_saved = 0
is_human_saved = 0
human_pos = []
human_safe = 1

# ========================= Student's code ends here ===========================

################ Pre-defined parameters and functions no need to change below ################

# 20Hz
SPIN_RATE = 20

# UR3 home location
home = [0*PI/180.0, 0*PI/180.0, 0*PI/180.0, 0*PI/180.0, 0*PI/180.0, 0*PI/180.0]

# UR3 current position, using home position for initialization
current_position = copy.deepcopy(home)

thetas = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

digital_in_0 = 0
analog_in_0 = 0.0

suction_on = True
suction_off = False

current_io_0 = False
current_position_set = False

image_shape_define = False


"""
Whenever ur3/gripper_input publishes info this callback function is called.
"""
def input_callback(msg):

    global digital_in_0
    digital_in_0 = msg.DIGIN
    digital_in_0 = digital_in_0 & 1 # Only look at least significant bit, meaning index 0


"""
Whenever ur3/position publishes info, this callback function is called.
"""
def position_callback(msg):

    global thetas
    global current_position
    global current_position_set

    thetas[0] = msg.position[0]
    thetas[1] = msg.position[1]
    thetas[2] = msg.position[2]
    thetas[3] = msg.position[3]
    thetas[4] = msg.position[4]
    thetas[5] = msg.position[5]

    current_position[0] = thetas[0]
    current_position[1] = thetas[1]
    current_position[2] = thetas[2]
    current_position[3] = thetas[3]
    current_position[4] = thetas[4]
    current_position[5] = thetas[5]

    current_position_set = True


"""
Function to control the suction cup on/off
"""
def gripper(pub_cmd, loop_rate, io_0):

    global SPIN_RATE
    global thetas
    global current_io_0
    global current_position

    error = 0
    spin_count = 0
    at_goal = 0

    current_io_0 = io_0

    driver_msg = command()
    driver_msg.destination = current_position
    driver_msg.v = 1.0
    driver_msg.a = 1.0
    driver_msg.io_0 = io_0
    pub_cmd.publish(driver_msg)

    while(at_goal == 0):

        if( abs(thetas[0]-driver_msg.destination[0]) < 0.0005 and \
            abs(thetas[1]-driver_msg.destination[1]) < 0.0005 and \
            abs(thetas[2]-driver_msg.destination[2]) < 0.0005 and \
            abs(thetas[3]-driver_msg.destination[3]) < 0.0005 and \
            abs(thetas[4]-driver_msg.destination[4]) < 0.0005 and \
            abs(thetas[5]-driver_msg.destination[5]) < 0.0005 ):

            #rospy.loginfo("Goal is reached!")
            at_goal = 1

        loop_rate.sleep()

        if(spin_count >  SPIN_RATE*5):

            pub_cmd.publish(driver_msg)
            rospy.loginfo("Just published again driver_msg")
            spin_count = 0

        spin_count = spin_count + 1

    return error


"""
Move robot arm from one position to another
"""
def move_arm(pub_cmd, loop_rate, dest, vel, accel):

    global thetas
    global SPIN_RATE

    error = 0
    spin_count = 0
    at_goal = 0

    driver_msg = command()
    driver_msg.destination = dest
    driver_msg.v = vel
    driver_msg.a = accel
    driver_msg.io_0 = current_io_0
    pub_cmd.publish(driver_msg)

    loop_rate.sleep()

    global xw_yw_Y
    global human_pos
    global human_safe

    while(at_goal == 0):
        
        def distance_cal(pos1, pos2):
            dis = ((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)**0.5
            return dis

        # Check whether collide into human
        if xw_yw_Y and human_pos:
            dis = distance_cal(xw_yw_Y[0], human_pos[0])
            print("The distance between human and robot is {}".format(dis))
            if dis < 0.35:
                print("There is a human, do not hurt him!!!")
                human_safe = 0                
                break
                raise SystemExit(0)


        if( abs(thetas[0]-driver_msg.destination[0]) < 0.0005 and \
            abs(thetas[1]-driver_msg.destination[1]) < 0.0005 and \
            abs(thetas[2]-driver_msg.destination[2]) < 0.0005 and \
            abs(thetas[3]-driver_msg.destination[3]) < 0.0005 and \
            abs(thetas[4]-driver_msg.destination[4]) < 0.0005 and \
            abs(thetas[5]-driver_msg.destination[5]) < 0.0005 ):

            at_goal = 1
            #rospy.loginfo("Goal is reached!")

        loop_rate.sleep()

        if(spin_count >  SPIN_RATE*5):

            pub_cmd.publish(driver_msg)
            rospy.loginfo("Just published again driver_msg")
            spin_count = 0

        spin_count = spin_count + 1

    # if not human_safe:
    #     raise SystemExit(0)

    return error

################ Pre-defined parameters and functions no need to change above ################


def move_block(pub_cmd, loop_rate, start_xw_yw_zw, target_xw_yw_zw, vel = 4.0, accel = 4.0):

    """
    start_xw_yw_zw: where to pick up a block in global coordinates
    target_xw_yw_zw: where to place the block in global coordinates

    hint: you will use lab_invk(), gripper(), move_arm() functions to
    pick and place a block

    """

    #check whether path will collide into obstacle
    # if yes, 
    def check_collision_free(o, r, p1, p2):
        o = np.array(o)
        p1 = np.array(p1)
        p2 = np.array(p2)
        v = p2 - p1
        a = v.dot(v)
        b = 2*v.dot(p1 - o)
        c = p1.dot(p1) + o.dot(o) - 2*p1.dot(o) - r**2
        disc = b**2 - 4*a*c
        print('o: ' + str(o)  )
        print('p1:'+ str(p1) )
        print('p2: '+ str(p2) )
        print('a: ' + str(a)  )
        print('b: ' + str(b)  )
        print('c: ' + str(c) )
        print('disc: ' + str(disc) )
        if disc < 0:
            return True
        else:
            sqrt_disc = np.sqrt(disc)
            t1 = (-b+sqrt_disc)/2/a
            t2 = (-b-sqrt_disc)/2/a
            if not (0 <= t1 <= 1 or 0 <= t2 <= 1):
                return True
        return False

    # ========================= Student's code starts here =========================
    error = 0

    # global variable1
    # global variable2
    global xw_yw_B
    rad = 0.03

    collision_free = check_collision_free(xw_yw_B, rad, start_xw_yw_zw, target_xw_yw_zw)
    print("The checking result is {}".format(collision_free))

    height_screw = 0.035
    height_table = 0.052
    height_safe_offset = 0.085
    pre_pick_joints_angle = lab_invk(start_xw_yw_zw[0], start_xw_yw_zw[1], height_safe_offset, 0)
    pick_screw_angle = lab_invk(start_xw_yw_zw[0], start_xw_yw_zw[1], height_screw, 0)

    pre_place_joints_anlge = lab_invk(target_xw_yw_zw[0], target_xw_yw_zw[1], height_safe_offset, 0)
    place_joints_anlge = lab_invk(target_xw_yw_zw[0], target_xw_yw_zw[1], height_table, 0)
   

    rospy.loginfo("Ready to grasp!")
    # prepare to pick up screws
    move_arm(pub_cmd, loop_rate, pre_pick_joints_angle, vel, accel)
    # pick up screw
    move_arm(pub_cmd, loop_rate, pick_screw_angle, vel/8, accel/8)
    gripper(pub_cmd, loop_rate, suction_on)
    time.sleep(0.5)

    # Suction Feedback to determine if a block is held by the gripper
    if(digital_in_0==1):
        rospy.loginfo("Suck up successfully!")
        error = 0
    else:
        error = 1
        rospy.loginfo("Nothing gets sucked up")
        gripper(pub_cmd, loop_rate, suction_off)
        move_arm(pub_cmd, loop_rate, go_away, vel, accel)
        sys.exit()

    move_arm(pub_cmd, loop_rate, pre_pick_joints_angle, vel, accel)


    while not collision_free:
        theta = float(np.random.rand(1)*np.pi - np.pi/2)
        r = 0.04+float(np.random.rand(1)*0.01)
        middle_point = [xw_yw_B[0]+r*math.cos(theta), xw_yw_B[1]+r*math.sin(theta)]
        print('middle point: ' + str(middle_point))
        check_mid1 = check_collision_free(xw_yw_B, rad, start_xw_yw_zw, middle_point)
        check_mid2 = check_collision_free(xw_yw_B, rad, target_xw_yw_zw, middle_point)
        if check_mid1 and check_mid2:
            collision_free = True
            mid_angle = lab_invk(middle_point[0], middle_point[1], height_safe_offset, 0)
            move_arm(pub_cmd, loop_rate, mid_angle, vel, accel)
            time.sleep(2)


    # prepare to place screws
    move_arm(pub_cmd, loop_rate, pre_place_joints_anlge, vel, accel)

    # place screws
    move_arm(pub_cmd, loop_rate, place_joints_anlge, vel/8, accel/8)
    gripper(pub_cmd, loop_rate, suction_off)

    # go to home position
    move_arm(pub_cmd, loop_rate, go_away, vel, accel)

    rospy.loginfo("Moving done!!")
    # ========================= Student's code ends here ===========================

    return error


class ImageConverter:

    def __init__(self, SPIN_RATE):

        self.bridge = CvBridge()
        self.image_pub = rospy.Publisher("/image_converter/output_video", Image, queue_size=10)
        self.image_sub = rospy.Subscriber("/cv_camera_node/image_raw", Image, self.image_callback)
        self.loop_rate = rospy.Rate(SPIN_RATE)

        # Check if ROS is ready for operation
        while(rospy.is_shutdown()):
            print("ROS is shutdown!")


    def image_callback(self, data):

        global xw_yw_G # store found green blocks in this list
        global xw_yw_Y # store found yellow blocks in this list
        global xw_yw_R # store found yellow blocks in this list
        global xw_yw_B
        global human_pos
        global is_human_saved
        global is_green_red_saved

        try:
          # Convert ROS image to OpenCV image
            raw_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

        cv_image = cv2.flip(raw_image, -1)
        cv2.line(cv_image, (0,50), (640,50), (0,0,0), 5)

        # You will need to call blob_search() function to find centers of green blocks
        # and yellow blocks, and store the centers in xw_yw_G & xw_yw_Y respectively.

        # If no blocks are found for a particular color, you can return an empty list,
        # to xw_yw_G or xw_yw_Y.

        # Remember, xw_yw_G & xw_yw_Y are in global coordinates, which means you will
        # do coordinate transformation in the blob_search() function, namely, from
        # the image frame to the global world frame.
        
        # if not xw_yw_G:
        if not is_green_red_saved:
            xw_yw_G = blob_search(cv_image, "green")
            # xw_yw_R = blob_search(cv_image, "red")
            x_table = 0.3
            y_table = 0.2
            x_off = 0.09-0.005
            y_off = 0.165-0.005-0.001
            xw_yw_R = [[x_table+x_off, y_table+y_off], [x_table+x_off, y_table-y_off],[x_table-x_off, y_table+y_off],[x_table-x_off, y_table-y_off]]
        
        # if not is_human_saved:
        #     human_pos = blob_search(cv_image, "human")
        #     print("The human position is {}".format(human_pos))
        #     if human_pos:
        #         is_human_saved = 1
        human_pos = blob_search(cv_image, "human")
        # print("The human position is {}".format(human_pos))
        xw_yw_Y = blob_search(cv_image, "yellow")
        # xw_yw_B = blob_search(cv_image,'blue')
        # print("The gripper position is {}".format(xw_yw_Y))
                
        # def distance_cal(pos1, pos2):
        #     dis = ((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)**0.5
        #     return dis

        # if xw_yw_Y and human_pos:
        #     dis = distance_cal(xw_yw_Y[0], human_pos[0])
        #     print("The distance between human and robot is {}".format(dis))
        #     if dis < 0.1:
        #         print("There is a human, do not hurt him!!!")
        #         sys.exit()
        



"""
Program run from here
"""
def main():

    global go_away
    global xw_yw_R
    global xw_yw_G
    global xw_yw_R
    global target_xy_w

    # global variable1
    # global variable2

    # Initialize ROS node
    rospy.init_node('lab5node')

    # Initialize publisher for ur3/command with buffer size of 10
    pub_command = rospy.Publisher('ur3/command', command, queue_size=10)

    # Initialize subscriber to ur3/position & ur3/gripper_input and callback fuction
    # each time data is published
    sub_position = rospy.Subscriber('ur3/position', position, position_callback)
    sub_input = rospy.Subscriber('ur3/gripper_input', gripper_input, input_callback)

    # Check if ROS is ready for operation
    while(rospy.is_shutdown()):
        print("ROS is shutdown!")

    # Initialize the rate to publish to ur3/command
    loop_rate = rospy.Rate(SPIN_RATE)

    vel = 2.0
    accel = 2.0
    move_arm(pub_command, loop_rate, go_away, vel, accel)

    ic = ImageConverter(SPIN_RATE)
    time.sleep(5)

    # ========================= Student's code starts here =========================

    """
    Hints: use the found xw_yw_G, xw_yw_Y to move the blocks correspondingly. You will
    need to call move_block(pub_command, loop_rate, start_xw_yw_zw, target_xw_yw_zw, vel, accel)
    """
    global task_not_com
    global is_green_red_saved

    while  task_not_com:
        if len(xw_yw_G)==4 & task_not_com & len(xw_yw_R)==4:
            is_green_red_saved = 1
            for i in range(len(xw_yw_G)):
                move_block(pub_command, loop_rate, xw_yw_G[i], xw_yw_R[i])
                task_not_com = task_not_com - 1
        # if len(xw_yw_Y) & task_not_com_Y:
        #     move_block(pub_command, loop_rate, xw_yw_Y, target_xy_w_Y)
        #     task_not_com_Y = task_not_com_Y - 1
        # if len(xw_yw_R) & task_not_com_R:
        #     move_block(pub_command, loop_rate, xw_yw_R, target_xy_w_R)
        #     task_not_com_R = task_not_com_R - 1
    
    # if len(xw_yw_G):
    #     move_block(pub_command, loop_rate, xw_yw_G, target_xy_w_G)
    # if len(xw_yw_Y):
    #     move_block(pub_command, loop_rate, xw_yw_Y, target_xy_w_Y)
            
    # ========================= Student's code ends here ===========================

    move_arm(pub_command, loop_rate, go_away, vel, accel)
    rospy.loginfo("Task Completed!")
    print("Use Ctrl+C to exit program")
    rospy.spin()

if __name__ == '__main__':

    try:
        main()
    # When Ctrl+C is executed, it catches the exception
    except rospy.ROSInterruptException:
        pass
