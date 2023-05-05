# -*- coding: utf-8 -*-
"""
@author: Jean BERTRAND, Félicien BERTRAND, Tassadit YACINE
Date: 02 Mar 2023
Last update : 04 May 2023

This program does the following:
    + Connection to LabJack and reading inputs
    + Display on a graph
    + Inserting values in a PostgreSQL database
"""

# Import libraries
import numpy as np
from pyqtgraph.Qt import QtGui, QtCore, QtWidgets
import sys
import pyqtgraph as pg
from labjack import ljm

import dbms_class

connection_type = "TCP"
# Setup and call eReadNames to read from AIN0/AIN1/AIN2/AIN3 on the LabJack.
inputs = ["AIN0", "AIN1", "AIN2", "AIN3"]
windowWidth = 20
intervalHandle = 1
interval = 1000 # Number of microseconds in the interval

# Open first found LabJack
try:
    handle = ljm.openS("ANY", connection_type, "ANY")  # Any device, TCP connection, Any identifier

except ljm.LJMError as e:
    print(f"Connection to Labjack failed:\n{e}")

else:
    info = ljm.getHandleInfo(handle)
    print("Opened a LabJack with Device type: %i, Connection type: %i,\n"
          "Serial number: %i, IP address: %s, Port: %i,\nMax bytes per MB: %i" %
          (info[0], info[1], info[2], ljm.numberToIP(info[3]), info[4], info[5]))
    
    #Database
    pg_instance = dbms_class.DbmsConn(host="127.0.0.1",
                                      dbname="postgres",
                                      port=5432,
                                      user="postgres",
                                      password="password")
    pg_instance.db_diag("MAGENTA")
    conn_dbms = pg_instance.pgsql_conn()  # Cursor for Postgres instructions in Python
    
    pg_instance.pg_table_dropcrea(conn_dbms.cursor(), "DROP")  # DROP / CREATE
    pg_instance.pg_table_dropcrea(conn_dbms.cursor(), "CREATE")  # DROP / CREATE
    
    
    #Plot PyQtGraph
    app = QtWidgets.QApplication(sys.argv)
    
    win = pg.GraphicsLayoutWidget(title="Labjack Signal GUI")
    p = win.addPlot(title=inputs)
    curve = p.plot(pen=None, symbol='o')
    
    Xm = np.linspace(0,0,windowWidth)    
    ptr = -windowWidth
    
    """
    This method reads the values from the Labjack and updates the database
    and the graph, by calling the 'insert_db' and 'graph' methods respectively.
    """
    def update():
        global ptr
        nb_inputs = len(inputs)
        values = ljm.eReadNames(handle, nb_inputs, inputs)   # Lecture des analog inputs
        ptr += 1
        insert_db(nb_inputs, values, ptr)
        graph(values, ptr)
    
    """
    This method inserts the signal values into a PostgreSQL database.
    
    Parameters
    ----------
    nb_inputs: int
        Number of signals to process.
    values: [float]
        List containing the value of each signal.
    ptr: int
        Number assigned to the processed frame.
    """
    def insert_db(nb_inputs, values, ptr):
        zeros = np.zeros(4 - nb_inputs, dtype=int)
        values = np.concatenate([values, zeros])
        pg_instance.pg_table_insert(conn_dbms.cursor(), values, ptr, False)
        
    """
    This method displays a graph of the points corresponding to
    the signal values, in order to reconstitute it.
    Abscissa: Number of points
    Ordinate: Voltage (V)
    
    Parameters
    ----------
    values: [float]
        List containing the value of each signal.
    ptr: int
        Number assigned to the processed frame.
    """
    def graph(values, ptr):
        global curve, Xm
        Xm[:-1] = Xm[1:]
        Xm[-1] = values[0] #Le graphique n'affiche que la première valeur
        curve.setData(Xm)
        curve.setPos(ptr,0)
        if ptr%20 == 0:
            QtWidgets.QApplication.processEvents()
    
    win.show()

    ljm.startInterval(intervalHandle, interval) 
    while True:
        ljm.waitForNextInterval(intervalHandle)
        update()
    
    ljm.cleanInterval(intervalHandle)
    ljm.close(handle)
