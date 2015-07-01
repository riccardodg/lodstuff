#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Jun 5, 2014

init for submissions
@author: riccardo
'''

class Submission(object):
    __passcode=""
    __conf=""
    __year=""
    __ty=""
    __subevent=""
    __pid=""
    
    
    
    def __init__ (self,passcode,conf,year,ty,subevent,pid):
        self.__passcode = passcode
        self.__year = year
        self.__conf = conf
        self.__ty = ty
        self.__subevent = subevent
        self.__pid = pid

    def get_passcode(self):
        return self.__passcode


    def get_conf(self):
        return self.__conf


    def get_year(self):
        return self.__year


    def get_ty(self):
        return self.__ty


    def get_subevent(self):
        return self.__subevent


    def get_pid(self):
        return self.__pid


    def set_passcode(self, value):
        self.__passcode = value


    def set_conf(self, value):
        self.__conf = value


    def set_year(self, value):
        self.__year = value


    def set_ty(self, value):
        self.__ty = value


    def set_subevent(self, value):
        self.__subevent = value


    def set_pid(self, value):
        self.__pid = value


    def del_passcode(self):
        del self.__passcode


    def del_conf(self):
        del self.__conf


    def del_year(self):
        del self.__year


    def del_ty(self):
        del self.__ty


    def del_subevent(self):
        del self.__subevent


    def del_pid(self):
        del self.__pid

    passcode = property(get_passcode, set_passcode, del_passcode, "passcode's docstring")
    conf = property(get_conf, set_conf, del_conf, "conf's docstring")
    year = property(get_year, set_year, del_year, "year's docstring")
    ty = property(get_ty, set_ty, del_ty, "ty's docstring")
    subevent = property(get_subevent, set_subevent, del_subevent, "subevent's docstring")
    pid = property(get_pid, set_pid, del_pid, "pid's docstring")
        
        
        