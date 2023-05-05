# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 15:56:35 2022

Classe des connections TCP: Cette classe permet d'instancier les objets de connections
à un serveur CAN TCP suivant les prescritions d'un bus donné.

Elle détaile :

    + connection à SGBD via PostGreSQL

@author: silvani

Modifié pour le LabJack
"""
# ##########################################################################
# # Python Modules
# import time
# import os
# import configparser
# import numpy as np
from datetime import datetime
from colorama import Fore
from colorama import Style
from colorama import init
import psycopg2


class DbmsConn:
    """Class for creating  a connection  to DataBase Magegement Service and transfering
     the register values from an ADC

     The object is the cursor parameters set-up
             Parameters
        ----------
        host : string
            Set the IP address of the db server on the network
        dbname : string
            Set the database name
        port : integer
            Set the port number for I/O DB transfer
        user : string
            Set the name of the allowed user
        password : string
            Set explicitly the password for allowed connection

        Returns
        -------
        An Object with DB connection parameters

        Notes
        -----
        Test note


     """

    def __init__(self, host, dbname, port, user, password):
        """ This object set the connection parameters

        """
        self.host = host
        self.dbname = dbname
        self.port = port
        self.user = user
        self.password = password

    # def __str__(self):
    #     return 'Connection on',self.host,' to ',self.dbname, \
    #                  ' through Port n°',port,' by user'.self.user

    def pgsql_conn(self):
        """
        That method launches a connection to the given DB.
        Commands of the corresponding language (default is PostGreSQL)
        are passed  from Python through the corresponding cursor class

        Returns
        -------
        conn : TYPE
            DESCRIPTION.

        """
        try:
            conn = psycopg2.connect(host=self.host,
                                    database=self.dbname,
                                    user=self.user,
                                    port=self.port,
                                    password=self.password)
            conn.autocommit = True
            return conn

        except psycopg2.Error as error:
            print("Error while connecting to PostgreSQL", error)

    @staticmethod
    def coloured_att(att: str, colour: str):
        """

        Parameters
        ----------
        att : String
            Attributes of the self object of which the __str__
            must be changed from white to colour

        colour : str
            The new ANSI colour of the printed attribut

        Returns
        -------
        TYPE string
            the str output of Fore.Colour+"Attribute Name"+"Style.RESET_ALL"
        """
        init()
        chgcolor = eval("Fore."+colour)
        rstcolor = Style.RESET_ALL
        return str(chgcolor)+att+rstcolor

    def db_diag(self, colour):
        """
        Set the parameter of the given DB connection

        Returns
        -------
        String
            Returns the host, dbname, user and port of the given DB server connection
        """
        init()

        return print('\n >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> \n'
                     'A connection is set with a PostGreSQL DB Server \n'
                     'on host ', self.coloured_att(self.host, colour), '\n'
                     'over DB ', self.coloured_att(self.dbname, colour), '\n'
                     'by user ', self.coloured_att(self.user, colour),
                     'through port n°', self.coloured_att(str(self.port), colour),
                     '\n >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> \n')

    @staticmethod
    def pg_table_dropcrea(curs_conn, action: str):
        """
        Parameters
        ----------
        curs_conn : TYPE connector
            curs_conn is a connector from Python to PostGreSQL allowing to pass SQL order from Python
            code lines.
        action : str
            The SQL command the user wishes to pass

        Returns
        -------
        None.

        """

        try:
            if action == "DROP":
                drop = 'DROP TABLE IF EXISTS pooTestTable;'
                print("+++++++++++++++++++++++++++++++++++\n", drop)
                curs_conn.execute(drop)
                print("pootesttable dropped!")
                print("+++++++++++++++++++++++++++++++++++\n")
                return       

            elif action == "CREATE":
                # Create Table tabletherm is not exist
                create = ' CREATE TABLE IF NOT EXISTS pootesttable \
                    (EventNumber INTEGER NOT NULL PRIMARY KEY, \
                     ModBus_ILoop INTEGER, \
                     DateTime TIMESTAMP NOT NULL, \
                     AI1 FLOAT, \
                     AI2 FLOAT, \
                     AI3 FLOAT, \
                     AI4 FLOAT );'
                print("+++++++++++++++++++++++++++++++++++\n", create)
                curs_conn.execute(create)
                print("pootesttable created!")
                print("+++++++++++++++++++++++++++++++++++\n")
                return   
                
            else:
                return print("There is no action on table method used there.")

        except NameError as err:
            return print("Switch expection: action is not defined!", err)

    @staticmethod
    def pg_table_insert(curs_conn, local_regs, incr, cout_local: bool):
        """
        

        Parameters
        ----------
        curs_conn : curseur de la classe psycopg:
            Permet de passer des instructions postGrSQL à partir du langage Python
        local_regs : list
            Liste des 4 valeurs de registres d'entrée analogique:
        incr : int
            Increment de la boucle temporelle infinie. Cadence 1s.
        cout_local: local value of the cout parameter for editing text

        Returns
        -------
        None.

        """
        # insert= 'INSERT into pootesttable VALUES('+str(incr+1)+","+str(incr)+", ""'" \
        # +str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+"'," \
        # +str(local_regs[0])+", "+str(local_regs[1])+", "+str(local_regs[2])+');'
        # print(insert) 
        # curs_conn.execute(insert)
        # return

        try:
            insert = 'INSERT into pootesttable VALUES('+str(incr+1) + "," \
             + str(incr)+", ""'"+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%fZ')) + "'," \
             + str(local_regs[0]) + ", " \
             + str(local_regs[1]) + ", " \
             + str(local_regs[2]) + ", " \
             + str(local_regs[3]) + ');'
        # print(insert) 
            curs_conn.execute(insert)

            if cout_local:
                return print("Register line inserted in pootesttable of postgres DB")
        except psycopg2.Error as err:
            print("Insertion failed!! Error", err)
            return print("Error Type : ", type(err)) 
  