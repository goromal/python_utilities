#!/usr/bin/python3

import numpy as np
import utils_logging as logging

def getFormattedMatrixFromLog(logfilename, rowsize, frames_to_skip=1):
    data = logging.logToMatrix(logfilename, rowsize)
    return data[:, ::frames_to_skip]
