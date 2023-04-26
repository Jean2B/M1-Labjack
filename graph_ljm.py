# -*- coding: utf-8 -*-
"""
@author: Jean BERTRAND, Félicien BERTRAND, Tassadit YACINE
Date: 02 Mar 2023

Ce programme effectue les actions suivantes :
    + Connexion au LabJack et lecture des entrées
    + Affichage sur un graphique
    + Insertion des valeurs dans une base de données PostgreSQL
"""

# Import libraries
import numpy as np
from pyqtgraph.Qt import QtGui, QtCore, QtWidgets
import sys
import pyqtgraph as pg
from labjack import ljm

import dbms_class


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
    inputs = ["AIN0", "AIN1", "AIN2", "AIN3"]
    
    
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
    
    windowWidth = 20
    Xm = np.linspace(0,0,windowWidth)    
    ptr = -windowWidth
    
    def update():
        global curve, ptr, Xm
        nb_inputs = len(inputs)
        values = ljm.eReadNames(handle, nb_inputs, inputs)   # Lecture des analog inputs
        #Insertion in database
        zeros = np.zeros(4 - nb_inputs, dtype=int)
        values = np.concatenate([values, zeros])
        pg_instance.pg_table_insert(conn_dbms.cursor(), values, ptr, False)
        Xm[:-1] = Xm[1:]
        Xm[-1] = values[0] #TODO : pour l'instant le graphique n'affiche que la première valeur
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
