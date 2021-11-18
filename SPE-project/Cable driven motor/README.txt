CABLE Driven Robot for the SPE project


NOTICE: Do not power the motors unless the the arduino has been reseted by:
	- running pytohn script
	- press the botton in the board
	- upload a new code


----------------
INTIALIZATION STEPS
- Place the end effector in the center of the table by pulling the dc motors
- Open the Unity 3D project and  python main script
- Press play to the python script
- Turn on the power
- Run the Unity 3D interface
- Wait until the python console shows a confirmation message
- The user interface can now be used to pick and place the objects


---------------
NOTES:
- A more powerfull power supply can be used to increase speed
- DC motors can handle up to 24 V
- The port for the Serial Commincation is COM5 if other is used change in the robot3.py file
- To chnage the speed of the robot, it is possble to:
	- decrease the number of points in the definePathAcce.py
	- decrese the time step of sneding the points to the arduino mega
