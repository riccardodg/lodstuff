#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Jun 12, 2014
Model the resource
Fields 
  conf,
  year,
  passcode,
  resourceid,
  type,
  name,
  size,
  unit,
  prodstatus,
  langsel,
  langdimension,
  lang1,
  lang2,
  lang3,
  lang4,
  lang5,
  langother,
  modality,
  resourceusage,
  avail ,
  license,
  url,
  doc,
  description,
  shared,
  pf ,
  uurl
  
@author: riccardo

'''

class Resource(object):
    '''type of the object
    is an instance
    is a normalized
    is a template
    '''
    __isobjres="";
    
    #not all fields are needed 
    '''fields that will define the id
    __conf=""
    __year=""
    __passcode=""
    __rtype=""
    __name=""
    __prodstatus=""
    '''
    
    '''
    for the class
    __type=""
    '''
    
    '''
    objectproperties
    __prodstatus=""
    __langtype="" mono/bi..
    __lang1="" should point to http://lexvo.org/id/iso639-3/<code>
    __lang2=""
    __lang3=""
    __lang4=""
    __lang5=""
    __modality=""
    __resourceusage=""
    __avail =""
    __license="" should point to metashare
    
    '''
    
    '''
    dataproperties
    __size=""
    __unit=""
    __url=""
    __doc=""
    __description=""
    __langother
    '''
    __conf=""
    __year=""
    __passcode=""
    __type=""
    __name=""
    __size=""
    __unit=""
    __prodstatus=""
    __langtype=""
    __lang1=""
    __lang2=""
    __lang3=""
    __lang4=""
    __lang5=""
    __langother=""
    __modality=""
    __resourceusage=""
    __avail =""
    __license=""
    __url=""
    __doc=""
    __description=""
    
    def __init__(self,conf, year, passcode, isobjres, rtype, name, size, unit, prodstatus, langtype, 
                 lang1, lang2, lang3, lang4, lang5, langother, modality, resourceusage, avail , rlicense, 
                 url, doc, description):
            self.__conf=conf
            self.__year=year
            self.__passcode=passcode
            self.__isobjres=isobjres
            self.__type=rtype
            self.__name=name
            self.__size=size
            self.__unit=unit
            self.__prodstatus=prodstatus
            self.__langtype=langtype
            self.__lang1=lang1
            self.__lang2=lang2
            self.__lang3=lang3
            self.__lang4=lang4
            self.__lang5=lang5
            self.__langother=langother
            self.__modality=modality
            self.__resourceusage=resourceusage
            self.__avail =avail
            self.__license=rlicense
            self.__url=url
            self.__doc=doc
            self.__description=description

    def get_isobjres(self):
        return self.__isobjres


    def get_conf(self):
        return self.__conf


    def get_year(self):
        return self.__year


    def get_passcode(self):
        return self.__passcode


    def get_type(self):
        return self.__type


    def get_name(self):
        return self.__name


    def get_size(self):
        return self.__size


    def get_unit(self):
        return self.__unit


    def get_prodstatus(self):
        return self.__prodstatus


    def get_langtype(self):
        return self.__langtype


    def get_lang_1(self):
        return self.__lang1


    def get_lang_2(self):
        return self.__lang2


    def get_lang_3(self):
        return self.__lang3


    def get_lang_4(self):
        return self.__lang4


    def get_lang_5(self):
        return self.__lang5


    def get_langother(self):
        return self.__langother


    def get_modality(self):
        return self.__modality


    def get_resourceusage(self):
        return self.__resourceusage


    def get_avail(self):
        return self.__avail


    def get_license(self):
        return self.__license


    def get_url(self):
        return self.__url


    def get_doc(self):
        return self.__doc


    def get_description(self):
        return self.__description


    def set_isobjres(self, value):
        self.__isobjres = value


    def set_conf(self, value):
        self.__conf = value


    def set_year(self, value):
        self.__year = value


    def set_passcode(self, value):
        self.__passcode = value


    def set_type(self, value):
        self.__type = value


    def set_name(self, value):
        self.__name = value


    def set_size(self, value):
        self.__size = value


    def set_unit(self, value):
        self.__unit = value


    def set_prodstatus(self, value):
        self.__prodstatus = value


    def set_langtype(self, value):
        self.__langtype = value


    def set_lang_1(self, value):
        self.__lang1 = value


    def set_lang_2(self, value):
        self.__lang2 = value


    def set_lang_3(self, value):
        self.__lang3 = value


    def set_lang_4(self, value):
        self.__lang4 = value


    def set_lang_5(self, value):
        self.__lang5 = value


    def set_langother(self, value):
        self.__langother = value


    def set_modality(self, value):
        self.__modality = value


    def set_resourceusage(self, value):
        self.__resourceusage = value


    def set_avail(self, value):
        self.__avail = value


    def set_license(self, value):
        self.__license = value


    def set_url(self, value):
        self.__url = value


    def set_doc(self, value):
        self.__doc = value


    def set_description(self, value):
        self.__description = value


    def del_isobjres(self):
        del self.__isobjres


    def del_conf(self):
        del self.__conf


    def del_year(self):
        del self.__year


    def del_passcode(self):
        del self.__passcode


    def del_type(self):
        del self.__type


    def del_name(self):
        del self.__name


    def del_size(self):
        del self.__size


    def del_unit(self):
        del self.__unit


    def del_prodstatus(self):
        del self.__prodstatus


    def del_langtype(self):
        del self.__langtype


    def del_lang_1(self):
        del self.__lang1


    def del_lang_2(self):
        del self.__lang2


    def del_lang_3(self):
        del self.__lang3


    def del_lang_4(self):
        del self.__lang4


    def del_lang_5(self):
        del self.__lang5


    def del_langother(self):
        del self.__langother


    def del_modality(self):
        del self.__modality


    def del_resourceusage(self):
        del self.__resourceusage


    def del_avail(self):
        del self.__avail


    def del_license(self):
        del self.__license


    def del_url(self):
        del self.__url


    def del_doc(self):
        del self.__doc


    def del_description(self):
        del self.__description

    isobjres = property(get_isobjres, set_isobjres, del_isobjres, "isobjres's docstring")
    conf = property(get_conf, set_conf, del_conf, "conf's docstring")
    year = property(get_year, set_year, del_year, "year's docstring")
    passcode = property(get_passcode, set_passcode, del_passcode, "passcode's docstring")
    type = property(get_type, set_type, del_type, "type's docstring")
    name = property(get_name, set_name, del_name, "name's docstring")
    size = property(get_size, set_size, del_size, "size's docstring")
    unit = property(get_unit, set_unit, del_unit, "unit's docstring")
    prodstatus = property(get_prodstatus, set_prodstatus, del_prodstatus, "prodstatus's docstring")
    langtype = property(get_langtype, set_langtype, del_langtype, "langtype's docstring")
    lang1 = property(get_lang_1, set_lang_1, del_lang_1, "lang1's docstring")
    lang2 = property(get_lang_2, set_lang_2, del_lang_2, "lang2's docstring")
    lang3 = property(get_lang_3, set_lang_3, del_lang_3, "lang3's docstring")
    lang4 = property(get_lang_4, set_lang_4, del_lang_4, "lang4's docstring")
    lang5 = property(get_lang_5, set_lang_5, del_lang_5, "lang5's docstring")
    langother = property(get_langother, set_langother, del_langother, "langother's docstring")
    modality = property(get_modality, set_modality, del_modality, "modality's docstring")
    resourceusage = property(get_resourceusage, set_resourceusage, del_resourceusage, "resourceusage's docstring")
    avail = property(get_avail, set_avail, del_avail, "avail's docstring")
    license = property(get_license, set_license, del_license, "license's docstring")
    url = property(get_url, set_url, del_url, "url's docstring")
    doc = property(get_doc, set_doc, del_doc, "doc's docstring")
    description = property(get_description, set_description, del_description, "description's docstring")
    
