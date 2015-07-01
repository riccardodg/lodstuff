#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Apr 30, 2014
Connect to LreMap DB
@author: riccardo
'''


import MySQLdb



class LreMapDbAPI (object):

    __connection=None 
    
    
    def __init__(self,host,user,passwd,db,verbose):
        self.host=host
        self.user=user
        self.passwd=passwd
        self.db=db
        self.verbose=verbose
        
    def connectToDb(self,host,user,passwd,db):
        connection = self.get_connection()
        name="LreMapDbAPI.connectToDb"
        if (self.verbose==1):
            print "LREMAPDB APIs: Executing "+name  +"\n"
        try:
            if connection is None:
                connection = MySQLdb.connect(host,user,passwd,db)
                connection.set_character_set('utf8')
            else:
                if (self.verbose==1):
                    print "Already Connected "+name+ "\n"
                    
        except:
            connection =None
            
        self.set_connection(connection)
        return connection
    

        
    def closeConnection(self, connection):
        name="closeConnection"
        if (self.verbose==1):
            print "LREMAPDB APIs: Executing "+name  +"\n"
        if connection is not None:
            connection.close()
            
            
            
     
    def get_connection(self):
        return self.__connection


    def set_connection(self, value):
        self.__connection = value


    def del_connection(self):
        del self.__connection

    connection = property(get_connection, set_connection, del_connection, "connection's docstring")
           
