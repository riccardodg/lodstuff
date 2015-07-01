#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on May 12, 2014
Model Paper
fields:
  conf
  year
  passcode
  paper id
  status
  title
  category1
  category1
  keywords
@author: riccardo
'''


class Paper(object):

    __conf=""
    __year=""
    __passcode=""
    __pid=""
    __status=""
    __title=""
    __category1=""
    __category2=""
    __keywords=""
    
    
    def __init__(self, conf,year,pid, status, title, category1, category2, keywords):
        self.__conf = conf
        self.__year = year
        self.__pid = pid
        self.__status = status
        self.__title = title
        self.__category1 = category1
        self.__category2 = category2
        self.__keywords = keywords

    def get_passcode(self):
        return self.__passcode


    def get_pid(self):
        return self.__pid


    def get_status(self):
        return self.__status


    def get_title(self):
        return self.__title


    def get_category_1(self):
        return self.__category1


    def get_category_2(self):
        return self.__category2


    def get_keywords(self):
        return self.__keywords


    def set_passcode(self, value):
        self.__passcode = value


    def set_pid(self, value):
        self.__pid = value


    def set_status(self, value):
        self.__status = value


    def set_title(self, value):
        self.__title = value


    def set_category_1(self, value):
        self.__category1 = value


    def set_category_2(self, value):
        self.__category2 = value


    def set_keywords(self, value):
        self.__keywords = value


    def del_passcode(self):
        del self.__passcode


    def del_pid(self):
        del self.__pid


    def del_status(self):
        del self.__status


    def del_title(self):
        del self.__title


    def del_category_1(self):
        del self.__category1


    def del_category_2(self):
        del self.__category2


    def del_keywords(self):
        del self.__keywords

    passcode = property(get_passcode, set_passcode, del_passcode, "passcode's docstring")
    pid = property(get_pid, set_pid, del_pid, "pid's docstring")
    status = property(get_status, set_status, del_status, "status's docstring")
    title = property(get_title, set_title, del_title, "title's docstring")
    category1 = property(get_category_1, set_category_1, del_category_1, "category1's docstring")
    category2 = property(get_category_2, set_category_2, del_category_2, "category2's docstring")
    keywords = property(get_keywords, set_keywords, del_keywords, "keywords's docstring")

    def get_conf(self):
        return self.__conf


    def get_year(self):
        return self.__year


    def set_conf(self, value):
        self.__conf = value


    def set_year(self, value):
        self.__year = value


    def del_conf(self):
        del self.__conf


    def del_year(self):
        del self.__year

    conf = property(get_conf, set_conf, del_conf, "conf's docstring")
    year = property(get_year, set_year, del_year, "year's docstring")


