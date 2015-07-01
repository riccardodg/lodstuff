#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on May 16, 2014

    <owl:Class rdf:about="&conf;Lrec2014">
        <rdfs:label xml:lang="en">Lrec2014</rdfs:label>
        <rdfs:subClassOf rdf:resource="&conf;Conference"/>
    </owl:Class>
    
    and add the individual
    
    owl:NamedIndividual rdf:about="&conf;Lrec2014">
        <rdf:type rdf:resource="&conf;Lrec2014"/>
        <conf:heldIn rdf:resource="&year;2010"/>
    </owl:NamedIndividual>

@author: riccardo
'''
from shutil import copy2
import codecs
import os
import utils

class SerializeConference(object):
    
    __t1="\t"
    __t2="\t\t"
    __t3="\t\t\t"
    __t4="\t\t\t\t"
    __CLOSELINE__="</rdf:RDF>"
    
    __STARTLOCLIST__="\n\n<!-- Start Location List -->\n"
    __ENDLOCLIST__="\n\n<!-- End Location List -->\n"
    __STARTCONF__="\n\n<!-- Start Conference List -->\n"
    __ENDCONF__="\n\n<!-- End Conference List List -->\n"


    def __init__(self, p2confs, writefile, outfile, headerfile,verbose):
        self.__p2confs = p2confs
        self.writefile = writefile
        self.outfile = outfile
        self.headerfile = headerfile
        self.verbose = verbose
        self.serializeConference(verbose,writefile)
        
    
    def readHeaderFileAndCopy2OutFile(self,src,dst,verbose):
        name ="SerializeConference.readHeaderFileAndCopy2OutFile"
        if os.path.isfile(dst):
            os.remove(dst)
            
        if (verbose==1):
            print "\t\t\tExecuting "+name
        
        copy2(src, dst)    
#         for lines in s:
#             d.write(lines)
#         
    def serializeConference(self,verbose,writefile):
        name ="SerializeConference.serializeConference" 
        if verbose==1:
            print "\tExecuting "+name
        
        src=self.headerfile
        dst=self.outfile
        self.readHeaderFileAndCopy2OutFile(src,dst,verbose)
        self.serializeConferenceIntoSigleFile(verbose)
        
#         if writefile==0:
#             
#             src=self.headerfile
#             dst=self.outfile
#             self.readHeaderFileAndCopy2OutFile(src,dst,verbose)
#             self.serializeYearsIntoSigleFile(verbose)
#         else: 
#             self.serializeYearsIntoSigleFile(verbose)
    
    
    def  serializeConferenceIntoSigleFile(self,verbose):
        name ="SerializeConference.serializeConferenceIntoSigleFile"   
        conf_serialized =set()
        location_serialized =set()
        
        if (verbose==1):
            print "\t\tExecuting "+name           
        
        oFile=codecs.open(self.outfile,'a','utf-8')
        oFile.write((self.__STARTCONF__).encode('utf-8'))
        
        '''
        write
         <owl:Class rdf:about="&conf;Lrec2014">
        <rdfs:label xml:lang="en">Lrec2014</rdfs:label>
        <rdfs:subClassOf rdf:resource="&conf;Conference"/>
    </owl:Class>
        '''
        for p, confs in self.__p2confs.iteritems():
            for conf in confs: 
                idc= conf.get_conf()
                idy= conf.get_year()
                ty=conf.get_ty()
                se=conf.get_subevent()
                location=conf.get_location()
                event="ConferenceEvent"
                subevent=""
                idx=idc+"#"+idy
                #idx=idc
                idx =utils.pruneName(idx, " ")
                if not idx  in conf_serialized:
                    
                    conf_serialized.add(idx)
                    location_serialized.add(location)
                    '''
                    <owl:NamedIndividual rdf:about="&swc;C1">
                        <rdf:type rdf:resource="&swc;ConferenceEvent"/>
                        <hasLocation rdf:resource="&swc;Reykjavik"/>
                    </owl:NamedIndividual>
                    
                    '''
                    if ty=="WS":
                        event="WorkshopEvent"
                        subevent="<swc:isSubEventOf rdf:resource=\"&swc;#"+se+"\"/>"
                    else:
                        event="ConferenceEvent"
                        subevent=""
                            
                        
                    line=self.__t1+"<owl:NamedIndividual rdf:about=\"&swc;#"+idc+idy+"\">"
                    oFile.write((line+"\n").encode('utf-8'))
                    line=self.__t2+"<rdfs:label>"+idc+" "+idy+"</rdfs:label>"
                    oFile.write((line+"\n").encode('utf-8'))
                    line=self.__t2+"<rdf:type rdf:resource=\"&swc;#"+event+"\"/>"
                    oFile.write((line+"\n").encode('utf-8'))
                    line=self.__t2+"<tl:atYear rdf:datatype=\"&xsd;#gYear\">"+idy+"</tl:atYear>"
                    oFile.write((line+"\n").encode('utf-8'))
                    line=self.__t2+"<swc:hasLocation rdf:resource=\"&swc;#"+location+"\"/>"
                    oFile.write((line+"\n").encode('utf-8'))
                    if subevent != "":
                        line=self.__t2+subevent
                        oFile.write((line+"\n").encode('utf-8'))
                    line=self.__t1+"</owl:NamedIndividual>"
                    oFile.write((line+"\n").encode('utf-8')) 
        
        oFile.write((self.__ENDCONF__+"\n").encode('utf-8'))
        
        '''
        <owl:NamedIndividual rdf:about="&year;2010">
            <rdf:type rdf:resource="&year;2010"/>
        </owl:NamedIndividual>
        '''
        oFile.write((self.__STARTLOCLIST__).encode('utf-8'))
        for y in location_serialized:
            
            line=self.__t1+"<owl:NamedIndividual rdf:about=\"&swc;#"+y+"\">"
            oFile.write((line+"\n").encode('utf-8'))
            line=self.__t2+"<rdf:type rdf:resource=\"&geo;#SpatialThing\"/>"
            oFile.write((line+"\n").encode('utf-8'))
            line=self.__t1+"</owl:NamedIndividual>"
            oFile.write((line+"\n").encode('utf-8'))
            
            
        oFile.write((self.__ENDLOCLIST__).encode('utf-8'))
        oFile.write((self.__CLOSELINE__+"\n").encode('utf-8'))        