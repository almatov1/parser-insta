import os
import threading
import time

def start_robot(robot_id,login,password):
    os.system("robot.py " + robot_id + " " + login + " " + password)
    
t3 = threading.Thread(target=start_robot, args=('3','',''),)       

t3.start()
t3.join()
print("3 bot finish.")

print("finish")
