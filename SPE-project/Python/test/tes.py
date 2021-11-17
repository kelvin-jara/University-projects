import math
import numpy as np


def inverseGenerator0( x, y):
    l1,l2 = 2, 2
    theta2_goal = np.arccos((x ** 2 + y ** 2 - l1 ** 2 - l2 ** 2) / (2 * l1 * l2))
    tmp = np.math.atan2(l2 * np.sin(theta2_goal),
                        (l1 + l2 * np.cos(theta2_goal)))
    theta1_goal = np.math.atan2(y, x) - tmp
    return np.rad2deg(theta1_goal), np.rad2deg(theta2_goal)


def inverseGenerator1( x, y):
    l1,l2 = 2, 2
    theta2_goal = np.arccos((x ** 2 + y ** 2 - l1 ** 2 - l2 ** 2) / (2 * l1 * l2))
    tmp = np.math.atan2(l2 * np.sin(theta2_goal),
                        (l1 + l2 * np.cos(theta2_goal)))
    theta1_goal = np.math.atan2(y, x) - tmp
    if theta1_goal < 0:
        theta2_goal = -theta2_goal
        tmp = np.math.atan2(l2 * np.sin(theta2_goal),
                            (l1 + l2 * np.cos(theta2_goal)))
        theta1_goal = np.math.atan2(y, x) - tmp
    return np.rad2deg(theta1_goal), np.rad2deg(theta2_goal)


def inverseGenerator11( x, y):
    l1,l2 = 2, 2
    theta2_goal = np.arccos((x ** 2 + y ** 2 - l1 ** 2 - l2 ** 2) / (2 * l1 * l2))
    tmp = np.math.atan2(l2 * np.sin(theta2_goal),
                        (l1 + l2 * np.cos(theta2_goal)))
    theta1_goal = np.math.atan2(y, x) - tmp
    if theta1_goal < 0:
        theta2_goal = -theta2_goal
        tmp = np.math.atan2(l2 * np.sin(theta2_goal),
                            (l1 + l2 * np.cos(theta2_goal)))
        theta1_goal = np.math.atan2(y, x) - tmp
        theta1_goal += 2*np.pi
        theta2_goal += 2*np.pi
    return np.rad2deg(theta1_goal), np.rad2deg(theta2_goal)

def inverseGenerator2( x, y):
    l1,l2 = 2, 2
    if y >= 0:
        theta2_goal = np.arccos((x ** 2 + y ** 2 - l1 ** 2 - l2 ** 2) / (2 * l1 * l2))
        tmp = np.math.atan2(l2 * np.sin(theta2_goal),
                            (l1 + l2 * np.cos(theta2_goal)))
        theta1_goal = np.math.atan2(y, x) - tmp

    elif y < 0:
        theta2_goal = np.arccos((x ** 2 + y ** 2 - l1 ** 2 - l2 ** 2) / (2 * l1 * l2))
        tmp = np.math.atan2(l2 * np.sin(theta2_goal),
                            (l1 + l2 * np.cos(theta2_goal)))
        theta1_goal = np.math.atan2(y, x) - tmp + 2*np.pi

    """
    if theta1_goal < 0:
        theta2_goal = -theta2_goal
        tmp = np.math.atan2(l2 * np.sin(theta2_goal),
                            (l1 + l2 * np.cos(theta2_goal)))
        theta1_goal = np.math.atan2(y, x) - tmp
    """
    return np.rad2deg(theta1_goal), np.rad2deg(theta2_goal)
n = 2
print(f"first:{inverseGenerator0(n,n)}", f"first:{inverseGenerator1(n,n)}", f"first:{inverseGenerator11(n,n)}")
print(f"second:{inverseGenerator0(-n, n)}", f"second:{inverseGenerator1(-n, n)}", f"second:{inverseGenerator11(-n, n)}")
print(f"third:{inverseGenerator0(-n,-n)}", f"third:{inverseGenerator1(-n,-n)}", f"third:{inverseGenerator11(-n,-n)}")
print(f"third:{inverseGenerator0(n, -n)}", f"third:{inverseGenerator1(n,-n)}", f"fourth:{inverseGenerator11(n, -n)}")
