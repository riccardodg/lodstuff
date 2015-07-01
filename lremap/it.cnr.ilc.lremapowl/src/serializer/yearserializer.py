#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on May 16, 2014

<owl:Class rdf:about="&year;2010">
        <rdfs:label xml:lang="en">2010</rdfs:label>
        <rdfs:subClassOf rdf:resource="&year;Year"/>
    </owl:Class>
    
    and add the individual
    
    <owl:NamedIndividual rdf:about="&year;2010">
        <rdf:type rdf:resource="&year;2010"/>
    </owl:NamedIndividual>

@author: riccardo
'''
from shutil import copy2
import codecs
import os

class SerializeYear(object):
    
    __t1="\t"
    __t2="\t\t"
    __t3="\t\t\t"
    __t4="\t\t\t\t"
    __CLOSELINE__="</rdf:RDF>"
    
    __STARTCLASSYEAR__="\n\n<!-- Start Class Year List -->\n"
    __ENDCLASSYEAR__="\n\n<!-- End Class Year List -->\n"
    __STARTYEAR__="\n\n<!-- Start Year List -->\n"
    __ENDYEAR__="\n\n<!-- End Year List -->\n"


    def __init__(self, p2years, writefile, outfile, headerfile,verbose):
        self.__p2years = p2years
        self.writefile = writefile
        self.outfile = outfile
        self.headerfile = headerfile
        self.verbose = verbose
        self.serializeYears(verbose,writefile)
        
    
    def readHeaderFileAndCopy2OutFile(self,src,dst,verbose):
        name ="SerializeYear.readHeaderFileAndCopy2OutFile"
        if os.path.isfile(dst):
            os.remove(dst)
            
        if (verbose==1):
            print "\t\t\tExecuting "+name
        
        copy2(src, dst)    
#         for lines in s:
#             d.write(lines)
#         
    def serializeYears(self,verbose,writefile):
        name ="SerializeYear.serializeYear" 
        if verbose==1:
            print "\tExecuting "+name
        
        src=self.headerfile
        dst=self.outfile
        self.readHeaderFileAndCopy2OutFile(src,dst,verbose)
        self.serializeYearsIntoSigleFile(verbose)
        
#         if writefile==0:
#             
#             src=self.headerfile
#             dst=self.outfile
#             self.readHeaderFileAndCopy2OutFile(src,dst,verbose)
#             self.serializeYearsIntoSigleFile(verbose)
#         else: 
#             self.serializeYearsIntoSigleFile(verbose)
    
    
    def  serializeYearsIntoSigleFile(self,verbose):
        name ="SerializeYear.serializeYearsIntoSigleFile"   
        year_serialized =set()
        
        if (verbose==1):
            print "\t\tExecuting "+name           
        
        oFile=codecs.open(self.outfile,'a','utf-8')
        oFile.write((self.__STARTCLASSYEAR__).encode('utf-8'))
        
        '''
        write
        <owl:Class rdf:about="&year;2010">
            <rdfs:label xml:lang="en">2010</rdfs:label>
            <rdfs:subClassOf rdf:resource="&year;Year"/>
        </owl:Class>
        '''
        for p, years in self.__p2years.iteritems():
            for year in years: 
                idy= year.get_year()
                if not idy  in year_serialized:
                    year_serialized.add(idy)
                    line=self.__t1+"<owl:Class rdf:about=\"&year;#"+idy+"\">"
                    oFile.write((line+"\n").encode('utf-8'))
                    line=self.__t2+"<rdfs:label>"+idy+"</rdfs:label>"
                    oFile.write((line+"\n").encode('utf-8'))
                    line=self.__t2+"<rdfs:subClassOf rdf:resource=\"&year;#Year\"/>"
                    oFile.write((line+"\n").encode('utf-8'))
                    line=self.__t1+"</owl:Class>"
                    oFile.write((line+"\n").encode('utf-8')) 
        
        oFile.write((self.__ENDCLASSYEAR__+"\n").encode('utf-8'))
        
        '''
        <owl:NamedIndividual rdf:about="&year;2010">
            <rdf:type rdf:resource="&year;2010"/>
        </owl:NamedIndividual>
        '''
        oFile.write((self.__STARTYEAR__).encode('utf-8'))
        for y in year_serialized:
            line=self.__t1+"<owl:NamedIndividual rdf:about=\"&year;#"+y+"\">"
            oFile.write((line+"\n").encode('utf-8'))
            line=self.__t2+"<rdf:type rdf:resource=\"&year;#"+y+"\"/>"
            oFile.write((line+"\n").encode('utf-8'))
            line=self.__t1+"</owl:NamedIndividual>"
            oFile.write((line+"\n").encode('utf-8'))
            
            
        oFile.write((self.__ENDYEAR__).encode('utf-8'))
        oFile.write((self.__CLOSELINE__+"\n").encode('utf-8'))        