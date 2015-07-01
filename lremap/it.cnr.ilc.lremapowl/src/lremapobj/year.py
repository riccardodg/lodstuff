#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on May 16, 2014
fields:
  passcode
  year
@author: riccardo
'''

class Year(object):
    __passcode=""
    __year=""
    
    def __init__ (self,year):
        self.__year = year
        
        
        
        
        
    def get_passcode(self):
        return self.__passcode


    def get_year(self):
        return self.__year


    def set_passcode(self, value):
        self.__passcode = value


    def set_year(self, value):
        self.__year = value


    def del_passcode(self):
        del self.__passcode


    def del_year(self):
        del self.__year

    passcode = property(get_passcode, set_passcode, del_passcode, "passcode's docstring")
    year = property(get_year, set_year, del_year, "year's docstring")
