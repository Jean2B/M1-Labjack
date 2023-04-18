# -*- coding: utf-8 -*-
"""
@author: Jean BERTRAND, Félicien BERTRAND, Tassadit YACINE
Date: 02 Mar 2023
"""

# Import libraries
import numpy as np
from pyqtgraph.Qt import QtGui, QtCore, QtWidgets
import sys
import pyqtgraph as pg
from labjack import ljm


# Open first found LabJack
try:
    handle = ljm.openS("ANY", "TCP", "ANY")  # Any device, TCP connection, Any identifier

except ljm.LJMError as e:
    print(f"Connection to Labjack failed:\n{e}")

else:
    info = ljm.getHandleInfo(handle)
    print("Opened a LabJack with Device type: %i, Connection type: %i,\n"
          "Serial number: %i, IP address: %s, Port: %i,\nMax bytes per MB: %i" %
          (info[0], info[1], info[2], ljm.numberToIP(info[3]), info[4], info[5]))
    
    # Setup and call eReadName to read from AIN0 on the LabJack.
    name = "AIN0"
    
    #Plot PyQtGraph
    app = QtWidgets.QApplication(sys.argv)
    
    win = pg.GraphicsLayoutWidget(title="Labjack Signal GUI")
    p = win.addPlot(title=name)
    curve = p.plot(pen=None, symbol='o')
    
    windowWidth = 20
    Xm = np.linspace(0,0,windowWidth)    
    ptr = -windowWidth
    
    def update():
        global curve, ptr, Xm
        value = ljm.eReadName(handle, name)   # Lecture de l'analog input
        #print("\n%s reading : %f V" % (name, value))
        Xm[:-1] = Xm[1:]
        Xm[-1] = value      
        ptr += 1
        curve.setData(Xm)
        curve.setPos(ptr,0)
        if ptr%20 == 0:
            QtWidgets.QApplication.processEvents()
    
    win.show()
    
    intervalHandle = 1
    interval = 1000 # Number of microseconds in the interval
    ljm.startInterval(intervalHandle, interval) 
    while True:
        ljm.waitForNextInterval(intervalHandle)
        update()
    
    pg.QtGui.QApplication.exec_()
    ljm.close(handle)
