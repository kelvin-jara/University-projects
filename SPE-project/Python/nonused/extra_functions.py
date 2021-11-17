

def inverseGeneratorBackUp(trj, initThetax, initThetay):
    thetas = []
    l1,l2 = 24, 21.5
    theta1, theta2 = initThetax, initThetay
    changed = False
    counter  = 0
    for i in trj:
        x, y = i[0], i[1]
        # print("x and y::",x,y)
        if y < 0:
            if np.sqrt(x ** 2 + y ** 2) > l1 + l2:
                theta2_goal = 0
            else:
                theta2_goal = np.arccos((x ** 2 + y ** 2 - l1 ** 2 - l2 ** 2) / (2 * l1 * l2))

            # print("theta goal 2: ", theta2_goal, " distance: ", np.sqrt(x ** 2 + y ** 2), 'li nd l2: ', l1 +l2 )
            tmp = np.math.atan2(l2 * np.sin(theta2_goal), (l1 + l2 * np.cos(theta2_goal)))
            theta1_goal = np.math.atan2(y, x) - tmp
        elif y > 0:
            if np.sqrt(x ** 2 + y ** 2) > l1 + l2:
                theta2_goal = 0
            else:
                theta2_goal = np.arccos((x ** 2 + y ** 2 - l1 ** 2 - l2 ** 2) / (2 * l1 * l2))

            # print("theta goal 2: ", theta2_goal, " distance: ", np.sqrt(x ** 2 + y ** 2), 'li nd l2: ', l1 +l2 )
            tmp = np.math.atan2(l2 * np.sin(theta2_goal), (l1 + l2 * np.cos(theta2_goal)))
            theta1_goal = np.math.atan2(y, x) - tmp
            see = True
            # if theta1_goal <= 0:
            if see:
                theta2_goal = -theta2_goal
                tmp = np.math.atan2(l2 * np.sin(theta2_goal),
                                    (l1 + l2 * np.cos(theta2_goal)))
                theta1_goal = np.math.atan2(y, x) - tmp
                #print(f"here:{np.rad2deg(theta1_goal)}:{np.rad2deg(theta2_goal)}")
            #print(f"outsied:{np.rad2deg(theta1_goal)}:{np.rad2deg(theta2_goal)}")
        else:
            continue
        if not math.isnan(theta1_goal) and  not math.isnan(theta1_goal):
            # print(theta1_goal, " : ", theta2_goal)
            pi = np.pi
            #angle  = [theta1 - ang_diff(theta1, theta1_goal), theta2 - ang_diff(theta2, theta2_goal)]
            angle = [theta1_goal, theta2_goal]
            thetas.append(angle)
            # print(theta1*(360/(2*pi)), ang_diff(theta1, theta1_goal)*(360/(2*pi)), (theta1 - ang_diff(theta1, theta1_goal))*(360/(2*pi)), theta1_goal*(360/(2*pi)))
            # theta1 = theta1_goal
            # theta2 = theta2_goal
            theta1 = angle[0]
            theta2 = angle[1]
            #thetas.append([theta1_goal, theta2_goal])


    return np.array(thetas)