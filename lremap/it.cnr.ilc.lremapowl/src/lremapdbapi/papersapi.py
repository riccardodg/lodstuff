#! /usr/bin/env python
# -*- coding: utf-8 -*-


'''
Created on May 5, 2014
Access the db and extract the paper
@author: riccardo
'''


class LreMapPaperAPI (object):
    __AUTHNS__="auth"
    __GEONS__="gn"
    __PAPERTAB__="START_papers"
    
    def __init__(self, connection, verbose):
        self.connection = connection
        self.verbose = verbose

    
    def fetchData(self):
        name="LreMapPaperAPI.fetchData"

        #query="SELECT synsetid,definition, pos, lemma FROM "+ self.__SYNSETVIEW__ + " where lemma=\""+ws+ "\"  and pos='"+pos+"'"
        #query="SELECT * FROM "+ self.__PAPERTAB__ + "  where passcode='1000X-P3J6P5G7A6'; " #11X-J6E8G4A3E2
        #query="SELECT * FROM "+ self.__PAPERTAB__ + "  where passcode='11X-J6E8G4A3E2'; " #
        query="SELECT * FROM "+ self.__PAPERTAB__ + " B where B.status like '%Accept%';"
        #query="SELECT * FROM "+ self.__PAPERTAB__ + "  where username='riccardodg';"
        if (self.verbose==1):
            print "LREMAP PAPER APIs: Executing "+name  +" and query "+query
        
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