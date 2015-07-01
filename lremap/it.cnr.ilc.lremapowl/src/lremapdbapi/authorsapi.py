#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on May 5, 2014
Access the db and extract the author
@author: riccardo
'''


class LreMapAuthAPI (object):
    __AUTHTAB__="START_authors"
    __RESPAPER__="START_papers"
    
    def __init__(self, connection, verbose):
        self.connection = connection
        self.verbose = verbose

    
    def fetchData(self):
        name="LreMapPaperAPI.fetchData"

        #query="SELECT synsetid,definition, pos, lemma FROM "+ self.__SYNSETVIEW__ + " where lemma=\""+ws+ "\"  and pos='"+pos+"'"
        #query="SELECT * FROM "+ self.__AUTHTAB__ + "  where passcode='1000X-P3J6P5G7A6'; "
        #query="SELECT * FROM "+ self.__AUTHTAB__ + "  where passcode='11X-J6E8G4A3E2'; "
        query="SELECT * FROM "+ self.__AUTHTAB__ + " A,  "+self.__RESPAPER__+ " B where A.passcode=B.passcode and A.CONF=B.CONF and A.YEAR=B.YEAR AND B.status like '%Accept%';"
        #query="SELECT * FROM "+ self.__AUTHTAB__ + "  where username='riccardodg';"
        if (self.verbose==1):
            print "LREMAP AUTH APIs: Executing "+name  +" and query "+query
        
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