#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on May 5, 2014
Model Author
fields:
  passcode
  authornumber
  username
  firstname
  lastname
  email
  affiliation (as object)
@author: riccardo
'''
from lremapobj import affiliation



class Author(object):

    
    __passcode=""
    __authornumber=""
    __username=""
    __firstname=""
    __lastname=""
    __email=""
    __affiliation=[]
    
    
    def __init__(self, authornumber, username, firstname, lastname, email, institute, country):
        self.__authornumber = authornumber
        self.__username = username
        self.__firstname = firstname
        self.__lastname = lastname
        self.__email = email
        self.institute = institute
        self.country = country
        self.__affiliation = affiliation.Affiliation(institute,country)

    def get_passcode(self):
        return self.__passcode


    def get_authornumber(self):
        return self.__authornumber


    def get_username(self):
        return self.__username


    def get_firstname(self):
        return self.__firstname


    def get_lastname(self):
        return self.__lastname


    def get_email(self):
        return self.__email


    def get_affiliation(self):
        return self.__affiliation


    def set_passcode(self, value):
        self.__passcode = value


    def set_authornumber(self, value):
        self.__authornumber = value


    def set_username(self, value):
        self.__username = value


    def set_firstname(self, value):
        self.__firstname = value


    def set_lastname(self, value):
        self.__lastname = value


    def set_email(self, value):
        self.__email = value


    def set_affiliation(self, value):
        self.__affiliation = value


    def del_passcode(self):
        del self.__passcode


    def del_authornumber(self):
        del self.__authornumber


    def del_username(self):
        del self.__username


    def del_firstname(self):
        del self.__firstname


    def del_lastname(self):
        del self.__lastname


    def del_email(self):
        del self.__email


    def del_affiliation(self):
        del self.__affiliation

    passcode = property(get_passcode, set_passcode, del_passcode, "passcode's docstring")
    authornumber = property(get_authornumber, set_authornumber, del_authornumber, "authornumber's docstring")
    username = property(get_username, set_username, del_username, "username's docstring")
    firstname = property(get_firstname, set_firstname, del_firstname, "firstname's docstring")
    lastname = property(get_lastname, set_lastname, del_lastname, "lastname's docstring")
    email = property(get_email, set_email, del_email, "email's docstring")
    affiliation = property(get_affiliation, set_affiliation, del_affiliation, "affiliation's docstring")
