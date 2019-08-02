#!/usr/bin/python3
import sys
sys.path.insert(1, '../pylib')

import numpy as np
import utils_logging as logging

mydata = np.array([[ 1, 2, 1],
                   [ 2, 1, 0],
                   [-1, 1, 2]])

logging.matrixToLog('mydata.log', mydata)

newdata = logging.logToMatrix('mydata.log', 3)

print(newdata)

carTraj_Xforms = logging.logToMatrix('carTraj3.log', 3)
print(carTraj_Xforms.shape)
print(carTraj_Xforms[:,0:2])
