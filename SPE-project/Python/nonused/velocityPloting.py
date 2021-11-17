import numpy as np
import matplotlib.pyplot as plt
import math
import matplotlib.pyplot as plt
import pandas as pd

l1, l2 = 24, 21.5
l1, l2 = l1/100, l2/100
theta1, theta2 = np.pi, np.pi/2
w1, w2 = np.pi/6, np.pi/6
speed = []
jacobian = [[-l1*np.sin(theta1) - l2*np.sin(theta1 + theta2), -l2*np.sin(theta1 + theta2)],
            [l1*np.cos(theta1) + l2*np.cos(theta1+theta2), l2*np.cos(theta1 + theta2)]]
jacobian = np.array(jacobian)
angSpeed = np.array([[w1], [w2]])
# jaco = jacobian*angSpeed
jaco = np.matmul(jacobian,angSpeed)
linearSpeed = [np.sqrt(jaco[0][0]**2 + np.sqrt(jaco[0][0]**2)), np.sqrt(jaco[1][0]**2 + np.sqrt(jaco[1][0]**2))]
print(jaco)
