#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on May 7, 2014

many utilities to manage results set
@author: riccardo
'''

import re
import sha

def fetchDataAtIndex(self,results, idx, verbose):
    name="utils.fetchDataAtIndex "
    listOfSynsets=[]
    if(self.verbose==1):
        print "Executing "+name + " Idx: "+str(idx)
        idset=set()
    if results is not None:
        i=0
        for row in results:
            row=str(results[i][idx])
            idset.add(row)
            i=i+1
        listOfSynsets.append(idset)
    return listOfSynsets


def shasum(string):
    obj=sha.new(string)
    return obj.hexdigest()

def pruneName(string1,string2):
    change="_"
    s=""
    if string2 != "":
        string=string1+change+string2
    else:
        string=string1    
    s = re.sub(r"\s+", change, string)
    return s

def modifyString(string, ch1,ch2):
    mymatch ="/"+ch1 +"?"
    
#     s = re.sub(mymatch,ch2,string)
#     s = re.sub(mymatch,ch2,string)
    s = re.sub(r'[//\^,:;%" "]+', ch2,string)
    #print s
    return s