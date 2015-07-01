#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on May 5, 2014

@author: riccardo

Model an affiliation
fields: 
name
country code 

'''

class Affiliation(object):
    __name=""
    __countryCode=""

    def __init__(self, name, countryCode):
        self.__name = name
        self.__countryCode = countryCode

    def get_name(self):
        return self.__name


    def get_country_code(self):
        return self.__countryCode


    def set_name(self, value):
        self.__name = value


    def set_country_code(self, value):
        self.__countryCode = value


    def del_name(self):
        del self.__name


    def del_country_code(self):
        del self.__countryCode

    name = property(get_name, set_name, del_name, "name's docstring")
    countryCode = property(get_country_code, set_country_code, del_country_code, "countryCode's docstring")
        
        

    
    
    
    
