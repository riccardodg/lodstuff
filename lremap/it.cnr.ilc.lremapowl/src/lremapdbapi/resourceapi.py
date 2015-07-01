#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Jun 12, 2014
Access the db and extract the resource instance
@author: riccardo
'''

class LreMapResourceAPI (object):
    __AUTHNS__="auth"
    __GEONS__="gn"
    __RESITAB__="START_resource"
    __RESNTAB__="START_resource"
    __RESTTAB__="START_resource"
    __RESTAB__=""
    __RESPAPER__="START_papers"
    
    def __init__(self, connection, isobjres,verbose):
        self.connection = connection
        self.verbose = verbose
        self.isobjres=isobjres

    
    def fetchData(self):
        name="LreMapResourceAPI.fetchData"
        if self.isobjres=="ri":
            self.__RESTAB__=self.__RESITAB__
        if self.isobjres=="rn":
            self.__RESTAB__=self.__RESNTAB__     
        if self.isobjres=="rt":
            self.__RESTAB__=self.__RESTTAB__    

        #query="SELECT synsetid,definition, pos, lemma FROM "+ self.__SYNSETVIEW__ + " where lemma=\""+ws+ "\"  and pos='"+pos+"'"
        #query="SELECT * FROM "+ self.__RESTAB__ + "  where passcode='1000X-P3J6P5G7A6'; " #11X-J6E8G4A3E2
        #query="SELECT * FROM "+ self.__RESTAB__ + "  where passcode='712X-E7E6F9C2C5'; "
        #query="SELECT * FROM "+ self.__RESTAB__ + "  where passcode='11X-J6E8G4A3E2'; " #
        query="SELECT * FROM "+ self.__RESTAB__ + " A,  "+self.__RESPAPER__+ " B where A.passcode=B.passcode and A.CONF=B.CONF and A.YEAR=B.YEAR AND B.status like '%Accept%';"
        #query="SELECT * FROM "+ self.__RESTAB__ + "  where name like '%WordNet%';"
        #print query
        if (self.verbose==1):
            print "LREMAP RESOURCE APIs: Executing "+name  +" and query "+query
        
        cursor = self.connection.cursor()
        #query="SELECT synsetid,definition, pos, lemma FROM "+ self.__SYNSETVIEW__ + " where lemma='"+ws+ "'  and pos='"+pos+"'"
        
        try:
            cursor.execute(query)
            results=cursor.fetchall()
#             for row in results:
#                 print row[0]
        except:
            print "Error: unable to fecth data "+ query
            results=None
            
        return results 