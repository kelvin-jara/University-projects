import matplotlib.pyplot as plt
import roboticstoolbox as rtb
import spatialmath as sp
import numpy as np

robot = rtb.models.DH.Planar2()
robot.links[0].a = 20
robot.links[1].a = 21.5
# Similation parameters
Kp = 15
dt = 0.01

# Link lengths
l1 =  20
l2 = 21.5

# Set initial goal position to the initial end-effector position
x = 35.0
y = 35

show_animation = True

if show_animation:
    plt.ion()

def ang_diff(theta1, theta2):
    # Returns the difference between two angles in the range -pi to +pi
    return (theta1 - theta2 + np.pi) % (2 * np.pi) - np.pi

def two_joint_arm(GOAL_TH=0.0, theta1=0.0, theta2=0.0, xin = 0.0, yin = 0.0):
    """
    Computes the inverse kinematics for a planar 2DOF arm
    When out of bounds, rewrite x and y with last correct values
    """
    x, y = xin, yin
    x_prev, y_prev = None, None
    while True:
        print(x, y)
        try:
            if x is not None and y is not None:
                x_prev = x
                y_prev = y
            if np.sqrt(x**2 + y**2) > (l1 + l2):
                theta2_goal = 0
            else:
                theta2_goal = np.arccos(
                    (x**2 + y**2 - l1**2 - l2**2) / (2 * l1 * l2))
            tmp = np.math.atan2(l2 * np.sin(theta2_goal),
                                (l1 + l2 * np.cos(theta2_goal)))
            theta1_goal = np.math.atan2(y, x) - tmp

            if theta1_goal < 0:
                theta2_goal = -theta2_goal
                tmp = np.math.atan2(l2 * np.sin(theta2_goal),
                                    (l1 + l2 * np.cos(theta2_goal)))
                theta1_goal = np.math.atan2(y, x) - tmp

            theta1 = theta1 + Kp * ang_diff(theta1_goal, theta1) * dt
            theta2 = theta2 + Kp * ang_diff(theta2_goal, theta2) * dt
        except ValueError as e:
            print("Unreachable goal"+e)
        except TypeError:
            x = x_prev
            y = y_prev

        wrist = plot_arm(theta1, theta2, x, y)

        # check goal
        d2goal = None
        if x is not None and y is not None:
            d2goal = np.hypot(wrist[0] - x, wrist[1] - y)

        if abs(d2goal) < GOAL_TH and x is not None:

            return theta1, theta2

angles = []
def plot_arm(theta1, theta2, target_x, target_y):  # pragma: no cover
    shoulder = np.array([0, 0])
    elbow = shoulder + np.array([l1 * np.cos(theta1), l1 * np.sin(theta1)])
    wrist = elbow + \
            np.array([l2 * np.cos(theta1 + theta2), l2 * np.sin(theta1 + theta2)])
    global angles
    angles.append([theta1, theta2])
    return wrist


final = [-10, 15.5]
T = sp.SE3(final[0], final[1], 0)
sol = robot.ikine_LM(T,mask = [1, 1, 0, 0, 0, 0])
two_joint_arm(GOAL_TH=0.01, theta1=sol.q[0], theta2=sol.q[1],xin = final[0], yin = final[1])

print(x, y)