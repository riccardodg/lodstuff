#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on May 16, 2014
fields:
  passcode
  year
@author: riccardo
'''

class Conference(object):
    __passcode=""
    __conf=""
    __year=""
    __ty=""
    __subevent=""
    __location=""
    
    
    
    def __init__ (self,conf,year,ty,subevent,location):
        self.__year = year
        self.__conf = conf
        self.__ty = ty
        self.__subevent = subevent
        self.__location = location

    def get_passcode(self):
        return self.__passcode


    def get_conf(self):
        return self.__conf


    def set_passcode(self, value):
        self.__passcode = value


    def set_conf(self, value):
        self.__conf = value


    def del_passcode(self):
        del self.__passcode


    def del_conf(self):
        del self.__conf

    passcode = property(get_passcode, set_passcode, del_passcode, "passcode's docstring")
    conf = property(get_conf, set_conf, del_conf, "conf's docstring")

    def get_year(self):
        return self.__year


    def set_year(self, value):
        self.__year = value


    def del_year(self):
        del self.__year

    year = property(get_year, set_year, del_year, "year's docstring")

    def get_ty(self):
        return self.__ty


    def get_subevent(self):
        return self.__subevent


    def get_location(self):
        return self.__location


    def set_ty(self, value):
        self.__ty = value


    def set_subevent(self, value):
        self.__subevent = value


    def set_location(self, value):
        self.__location = value


    def del_ty(self):
        del self.__ty


    def del_subevent(self):
        del self.__subevent


    def del_location(self):
        del self.__location

    ty = property(get_ty, set_ty, del_ty, "ty's docstring")
    subevent = property(get_subevent, set_subevent, del_subevent, "subevent's docstring")
    location = property(get_location, set_location, del_location, "location's docstring")
        
        
        
        
        
   
    