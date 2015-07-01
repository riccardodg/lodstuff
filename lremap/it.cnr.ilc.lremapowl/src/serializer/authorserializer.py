#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on May 7, 2014

@author: riccardo
'''

from shutil import copy2
from utils import shasum, pruneName
import codecs
import collections
import os
import sys

'''
These APIs serve to create the following structure
Single file
<owl:NamedIndividual rdf:about="&auth;#2d0249738f36125405e9333b23035856b20db21c">
    <rdf:type rdf:resource="&foaf;/Person"/>
        <foaf:familyName>Rus</foaf:familyName>
        <foaf:mbox rdf:resource="mailto:xxx@xxx.net"/>
        <foaf:mbox_sha1sum>2d0249738f36125405e9333b23035856b20db21c
        </foaf:mbox_sha1sum><foaf:firstName>Vasile</foaf:firstName>
        <hasAffiliation rdf:resource="&auth;#IRISA"/>
        <hasAffiliation rdf:resource="&auth;#Italian_Institute_of_Technology"/>
        <hasAffiliation rdf:resource="&auth;#The_University_of_Memphis"/>
</owl:NamedIndividual>

<!-- AFFILIATION -->
<owl:NamedIndividual rdf:about="http://www.resourcebook.eu/lremap/owl/lremap_auth#IRISA">
    <rdf:type rdf:resource="&foaf;/Organization"/>
    <gn:countryCode>FR</gn:countryCode>
</owl:NamedIndividual>

One file for each author. Used the sha to create subfolders
'''

class SerializeAuthor(object):
    __t1="\t"
    __t2="\t\t"
    __t3="\t\t\t"
    __t4="\t\t\t\t"
    __CLOSELINE__="</rdf:RDF>"
    __STARTAUTH__="\n\n<!-- Start Author List -->\n"
    __ENDAUTH__="\n\n<!-- End Author List -->\n"
    __STARTAFFI__="\n\n<!-- Start Affiliation List -->\n"
    __ENDAFFI__="\n\n<!-- End Affiliation List -->\n"
    __AFFILIATIONS__="affiliations/"
    __AUTHS__="authors/"
    
    #description files used when many files are created
    __INDEXOFAUTHS__="listofauthors"
    __INDEXOFAFFILIATIONS__="listofaffiliations"
    
    
    #dictionaries
    __pass2Sha=collections.defaultdict(list)
    __sha2Affiliation=collections.defaultdict(list)
    __affiliationId2Details=collections.defaultdict(list)
    
    
    
    __p2auths=collections.defaultdict(list)
    writefile=0
    outfile=sys.stdout
    headerfile=None

    def __init__(self, p2auths, writefile, outfile, headerfile,verbose):
        self.__p2auths = p2auths
        self.writefile = writefile
        self.outfile = outfile
        self.headerfile = headerfile
        self.verbose = verbose
        self.createPasscode2AuthIdsAndAffiliationSetAndAuthIds2Affiliations(verbose)
        
        self.serializeAuthorsAndAffiliations(verbose,writefile)

    '''
    Create a mapping between passcodes and ids of authors.
    Meanwhile map ids to affiliations in order to manage 1 auth with many institutions
    '''
    def createPasscode2AuthIdsAndAffiliationSetAndAuthIds2Affiliations(self,verbose):
        name="SerializeAuthor.createPasscode2AuthIdsAndAffiliationSetAndAuthIds2Affiliations"
        p2s=collections.defaultdict(list)
        s2a=collections.defaultdict(list)
        affiliations=collections.defaultdict(list)
        templistida=[]
        templistidaffi=[]
        if (verbose==1):
            print "\tExecuting "+name
        
        for p, auths in self.__p2auths.iteritems():
            for auth in auths:
                #print "\nPasscode "+p +" hasAuthEmail "+auth.get_email() +"\n" 
                idaffi="NOAFFI"
                #passcode to sha mappaing
                ida=shasum(auth.get_email())
                affiliation=auth.get_affiliation()
                name=affiliation.get_name()
                country=affiliation.get_country_code()
#                 if name is not None and country is not None:
                idaffi=pruneName(name,country)
#                 else:
#                     idaffi="NOAFFI"
#                     name="AFFINAME"
#                     country="None" 
                
                idaffi=shasum(idaffi)
                #print "XXX "+temp+ " "+idaffi
                if not (ida in templistida):
                    p2s[p].append(ida)
                    templistida.append(ida)
                else:
                    if (verbose==1):
                        print "\t\tWARNING Author Element "+ida+ " with email "+auth.get_email()+ " appears many times" 
                
                # affiliations
                #print "XXX "+temp+ " "+idaffi
                s2a[ida].append(idaffi)
                
                if not (idaffi in templistidaffi ):
                    templistidaffi.append(idaffi)
                    affiliations[idaffi].append(affiliation)
                else:
                    if (verbose==1):
                        print "\t\tWARNING Affiliation Element "+ida+ " with name "+name+ " and country "+country+ " appears many times"
                              
        self.set_pass_2_sha(p2s)
        self.set_affiliation_id_2_details(affiliations)
        self.set_sha_2_affiliation(s2a)    
        
          
    def readHeaderFileAndCopy2OutFile_1(self,verbose):
        name ="SerializeAuthor.readHeaderFileAndCopy2OutFile"
        src=self.headerfile
        dst=self.outfile
        if os.path.isfile(dst):
            os.remove(dst)
            
        if (verbose==1):
            print "\t\t\tExecuting "+name
        
        copy2(src, dst)
        
    def readHeaderFileAndCopy2OutFile(self,src,dst,verbose):
        name ="SerializeAuthor.readHeaderFileAndCopy2OutFile"
        if os.path.isfile(dst):
            os.remove(dst)
            
        if (verbose==1):
            print "\t\t\tExecuting "+name
        
        copy2(src, dst)    
#         for lines in s:
#             d.write(lines)
#         
    def serializeAuthorsAndAffiliations(self,verbose,writefile):
        name ="SerializeAuthor.serializeAuthorsAndAffiliations" 
        if verbose==1:
            print "\tExecuting "+name
        
        if writefile==0:
            
            src=self.headerfile
            dst=self.outfile
            self.readHeaderFileAndCopy2OutFile(src,dst,verbose)
            self.serializeAuthorsAndAffiliationsIntoSigleFile(verbose)
        else: 
            self.serializeAuthorsAndAffiliationsInManyFiles(verbose)   
        
    def serializeAuthorsAndAffiliationsIntoSigleFile(self,verbose):
        name ="SerializeAuthor.serializeAuthorsAndAffiliationsIntoSigleFile"   
        auth_serialized =set()
        auth_affi_serialized =set()
        
        if (verbose==1):
            print "\t\tExecuting "+name

            
        oFile=codecs.open(self.outfile,'a','utf-8')
        oFile.write((self.__STARTAUTH__).encode('utf-8'))    
        for p, auths in self.__p2auths.iteritems():
            for auth in auths:
               
                ida=shasum(auth.get_email())
                if ida in auth_serialized:
                    pass
                    #print ida
                else:
                    auth_serialized.add(ida)
                    '''
                    create <owl:NamedIndividual rdf:about="&auth;#2d0249738f36125405e9333b23035856b20db21c">
                    calculate the shasum1 of the email
                    ''' 
                    line=self.__t1+"<owl:NamedIndividual rdf:about=\"&auth;#"+str(ida)+"\">"
                    oFile.write((line+"\n").encode('utf-8'))    
                
                    '''
                    Create <rdf:type rdf:resource="&foaf;/Person"/>
                    '''
                    line=self.__t2+"<rdf:type rdf:resource=\"&foaf;/Person\"/>"
                    oFile.write((line+"\n").encode('utf-8'))  
                
                    '''
                    Create <foaf:familyName>lastname</foaf:familyName>
                    '''
                    line=self.__t2+"<foaf:familyName>"+auth.get_lastname()+"</foaf:familyName>"
                    oFile.write((line+"\n").encode('utf-8'))  
                
                    ''''
                    Create <foaf:mbox rdf:resource="mailto:xxx@xxx.net"/>
                    '''
                    line =self.__t2+"<foaf:mbox rdf:resource=\"mailto:"+auth.get_email()+"\"/>"
                    oFile.write((line+"\n").encode('utf-8'))  
                    
                    ''''
                    Create <foaf:mbox_sha1sum>2d0249738f36125405e9333b23035856b20db21c</foaf:mbox_sha1sum>
                    '''
                    line =self.__t2+"<foaf:mbox_sha1sum>"+ida+"</foaf:mbox_sha1sum>"
                    oFile.write((line+"\n").encode('utf-8'))  
                 
                    '''
                    Create <foaf:firstName>Vasile</foaf:firstName>
                    '''
                    line =self.__t2+"<foaf:firstName>"+auth.get_firstname()+"</foaf:firstName>"
                    oFile.write((line+"\n").encode('utf-8'))
                
                    '''
                    Loop over affiliations
                    '''
                    ida2idaffi=self.get_sha_2_affiliation()
                    idsaffi=ida2idaffi.get(ida)
                    #print "XXX "+ida + " "+str(idsaffi) 
                    
                    if idsaffi is not None:
                        #get affiliations
                        for idaffi in idsaffi:
                            if ida+idaffi in auth_affi_serialized:
                                pass 
                            #print "XXX "+ida + " "+idaffi
                            else:
                                auth_affi_serialized.add(ida+idaffi)
                                affiliations = self.get_affiliation_id_2_details()
                                details = affiliations.get(idaffi)
                                for det in details:
                                    # print det.get_name()
                                    '''
                                    Create as many has affiliation needed 
                                    <auth:hasAffiliation rdf:resource="&auth;#IRISA"/>
                                    '''
                                    line = self.__t2 + "<swc:affiliation rdf:resource=\"&auth;#" + idaffi + "\"/>"
                                    oFile.write((line + "\n").encode('utf-8'))
                
                        '''
                        Close author </owl:NamedIndividual>
                         '''
                        line = self.__t1 + "</owl:NamedIndividual>"
                        oFile.write((line + "\n").encode('utf-8'))        
            
            #end for author
        #end for passcode 
        oFile.write((self.__ENDAUTH__ + "\n").encode('utf-8')) 
        oFile.write((self.__STARTAFFI__ + "\n").encode('utf-8'))
        
        for idaffi, details in self.get_affiliation_id_2_details().iteritems():
            for det in details:
                '''
                <owl:NamedIndividual rdf:about="&auth;#id">
                    <rdf:type rdf:resource="&foaf;/Organization"/>
                    <foaf:organization>Txxxp</foaf:organization>
                    <gn:countryCode>FR</gn:countryCode>
                </owl:NamedIndividual>
                '''
                '''
                The individual
                '''
                line=self.__t1+"<owl:NamedIndividual rdf:about=\"&auth;#"+idaffi+"\">"
                oFile.write((line + "\n").encode('utf-8'))
                '''
                The type
                '''
                line=self.__t2+"<rdf:type rdf:resource=\"&foaf;/Organization\"/>"
                oFile.write((line + "\n").encode('utf-8'))
                
                '''
                The name
                '''
                name=det.get_name()
                name=name.replace("&", "&amp;")
                line=self.__t2+"<foaf:organization>"+name+"</foaf:organization>"
                oFile.write((line + "\n").encode('utf-8'))
                
                '''
                The country
                '''
                cc=det.get_country_code()
                line=self.__t2+"<gn:countryCode>"+cc+"</gn:countryCode>"
                oFile.write((line + "\n").encode('utf-8'))
                
                '''
                Close Affiliation </owl:NamedIndividual>
                '''
                line = self.__t1 + "</owl:NamedIndividual>"
                oFile.write((line + "\n").encode('utf-8'))
                
                
                
                          
        
        oFile.write((self.__ENDAFFI__ + "\n").encode('utf-8')) 
        
        
#         #use to debug
#         for a, bs in self.get_sha_2_affiliation().iteritems():
#             for b in bs:
#                 print "Author "+a +" hasAffiliation "+b
#                 
#         print ""
#         for p, auths in self.__p2auths.iteritems():
#             for auth in auths:
#                 print "Passcode "+p +" hasAuthEmail "+auth.get_email()
                  
        
        #end
        oFile.write((self.__CLOSELINE__ + "\n").encode('utf-8'))    
        
        
    def serializeAuthorsAndAffiliationsInManyFiles(self,verbose):
        name ="SerializeAuthor.serializeAuthorsAndAffiliationsInManyFiles"   
        auth_serialized =set()
        auth_affi_serialized =set()
        append_auth=""
        append_affi="affiliations"
        
        if (verbose==1):
            print "\t\tExecuting "+name

        
        #idx file
        idxfile=self.outfile+self.__INDEXOFAUTHS__
          
        copy2(self.headerfile, idxfile)
        iFile=codecs.open(idxfile,'a','utf-8')
        iFile.write((self.__STARTAUTH__+"\n").encode('utf-8')) 
        
        for p, auths in self.__p2auths.iteritems():
            for auth in auths:
                '''
                create <owl:NamedIndividual rdf:about="&auth;x/xyz/2d0249738f36125405e9333b23035856b20db21c">
                calculate the shasum1 of the email
                '''
                ida=shasum(auth.get_email())
                
                    
                if ida in auth_serialized:
                    pass
                    #print ida
                else:
                    auth_serialized.add(ida)
                    #output file according to shasum
                    first_order_folder = str(ida[:1])
                    second_order_folder = str(ida[0:3])
                    if not os.path.exists(self.outfile+"/" + self.__AUTHS__+first_order_folder):
                        os.makedirs(self.outfile+"/" + self.__AUTHS__+"/"+first_order_folder)
                    if not os.path.exists(self.outfile+"/" + self.__AUTHS__+first_order_folder + "/" + second_order_folder):
                        os.makedirs(self.outfile+"/" + self.__AUTHS__+first_order_folder + "/" + second_order_folder)
                        
                    append_auth=self.__AUTHS__+first_order_folder + "/" + second_order_folder
                    
                    #write description file 
                    iLine=self.__t1+"<rdf:Description rdf:about=\"&auth;"+append_auth+"/"+str(ida)+"\">"
                    iFile.write((iLine+"\n").encode('utf-8')) 
                    iLine=self.__t2+"<rdfs:label>"+auth.get_lastname()+ " "+auth.get_firstname()+"</rdfs:label>"
                    iFile.write((iLine+"\n").encode('utf-8')) 
                    iLine=self.__t1+"</rdf:Description>"
                    iFile.write((iLine+"\n").encode('utf-8')) 
                    
                    
                      
                    dst=self.outfile+"/"+append_auth+"/"+ida
                    copy2(self.headerfile, dst)
                    oFile=codecs.open(dst,'a','utf-8')  
                    #oFile.write((self.__STARTAUTH__+"\n").encode('utf-8'))        
                    line=self.__t1+"<owl:NamedIndividual rdf:about=\"&auth;"+append_auth+"/"+str(ida)+"\">"
                    oFile.write((line+"\n").encode('utf-8'))    
                
                    '''
                    Create <rdf:type rdf:resource="&foaf;/Person"/>
                    '''
                    line=self.__t2+"<rdf:type rdf:resource=\"&foaf;/Person\"/>"
                    oFile.write((line+"\n").encode('utf-8'))  
                
                    '''
                    Create <foaf:familyName>lastname</foaf:familyName>
                    '''
                    line=self.__t2+"<foaf:familyName>"+auth.get_lastname()+"</foaf:familyName>"
                    oFile.write((line+"\n").encode('utf-8'))  
                
                    ''''
                    Create <foaf:mbox rdf:resource="mailto:xxx@xxx.net"/>
                    '''
                    line =self.__t2+"<foaf:mbox rdf:resource=\"mailto:"+auth.get_email()+"\"/>"
                    oFile.write((line+"\n").encode('utf-8'))  
                    
                    ''''
                    Create <foaf:mbox_sha1sum>2d0249738f36125405e9333b23035856b20db21c</foaf:mbox_sha1sum>
                    '''
                    line =self.__t2+"<foaf:mbox_sha1sum>"+ida+"</foaf:mbox_sha1sum>"
                    oFile.write((line+"\n").encode('utf-8'))  
                 
                    '''
                    Create <foaf:firstName>Vasile</foaf:firstName>
                    '''
                    line =self.__t2+"<foaf:firstName>"+auth.get_firstname()+"</foaf:firstName>"
                    oFile.write((line+"\n").encode('utf-8'))
                
                    '''
                    Loop over affiliations
                    '''
                    ida2idaffi=self.get_sha_2_affiliation()
                    idsaffi=ida2idaffi.get(ida)
                    #print "XXX "+ida + " "+str(idsaffi) 
                    
                    if idsaffi is not None:
                        #get affiliations
                        for idaffi in idsaffi:
                            if ida+idaffi in auth_affi_serialized:
                                pass 
                            #print "XXX "+ida + " "+idaffi
                            else:
                                auth_affi_serialized.add(ida+idaffi)
                                affiliations = self.get_affiliation_id_2_details()
                                details = affiliations.get(idaffi)
                                first_order_folder = str(idaffi[:1])
                                second_order_folder = str(idaffi[0:3])
                                append_affi=self.__AFFILIATIONS__+first_order_folder + "/" + second_order_folder
                                
                                
                                for det in details:
                                    # print det.get_name()
                                    '''
                                    Create as many has affiliation needed 
                                    <auth:hasAffiliation rdf:resource="&auth;#IRISA"/>
                                    '''
                                    line = self.__t2 + "<swc:affiliation rdf:resource=\"&auth;" +append_affi+"/" +idaffi + "\"/>"
                                    oFile.write((line + "\n").encode('utf-8'))
                
                        '''
                        Close author </owl:NamedIndividual>
                         '''
                        line = self.__t1 + "</owl:NamedIndividual>"
                        oFile.write((line + "\n").encode('utf-8')) 
                        
                        oFile.write((self.__CLOSELINE__ + "\n").encode('utf-8'))       
            
            #end for author
        #end for passcode
        iFile.write((self.__ENDAUTH__+"\n").encode('utf-8'))
        iFile.write((self.__CLOSELINE__ + "\n").encode('utf-8'))    
        
        
        '''
        Each affiliation in a distinct file
        '''
        #idx file
        idxfile=self.outfile+"/"+self.__INDEXOFAFFILIATIONS__
        copy2(self.headerfile, idxfile)
        iFile=codecs.open(idxfile,'a','utf-8')
        iFile.write((self.__STARTAFFI__+"\n").encode('utf-8'))
        for idaffi, details in self.get_affiliation_id_2_details().iteritems():
            for det in details:
                '''
                <owl:NamedIndividual rdf:about="&auth;#id">
                    <rdf:type rdf:resource="&foaf;/Organization"/>
                    <foaf:organization>Txxxp</foaf:organization>
                    <gn:countryCode>FR</gn:countryCode>
                </owl:NamedIndividual>
                '''
                '''
                The individual
                '''
                first_order_folder = str(idaffi[:1])
                second_order_folder = str(idaffi[0:3])
                if not os.path.exists(self.outfile+"/" + self.__AFFILIATIONS__+ first_order_folder):
                    os.makedirs(self.outfile+"/" + self.__AFFILIATIONS__+ first_order_folder)
                if not os.path.exists(self.outfile+"/" + self.__AFFILIATIONS__+ first_order_folder + "/" + second_order_folder):
                    os.makedirs(self.outfile+"/" + self.__AFFILIATIONS__+ first_order_folder + "/" + second_order_folder)
                        
                append_affi=self.__AFFILIATIONS__+first_order_folder + "/" + second_order_folder+"/"
                
                #write description file 
                iLine=self.__t1+"<rdf:Description rdf:about=\"&auth;"+append_affi+"/"+str(idaffi)+"\"></rdf:Description>"
                iFile.write((iLine+"\n").encode('utf-8')) 
                    
                dst=self.outfile+"/"+append_affi+"/"+idaffi
                copy2(self.headerfile, dst)
                oFile=codecs.open(dst,'a','utf-8')  
                
                line=self.__t1+"<owl:NamedIndividual rdf:about=\"&auth;"+append_affi+idaffi+"\">"
                oFile.write((line + "\n").encode('utf-8'))
                '''
                The type
                '''
                line=self.__t2+"<rdf:type rdf:resource=\"&foaf;/Organization\"/>"
                oFile.write((line + "\n").encode('utf-8'))
                
                '''
                The name
                '''
                name=det.get_name()
                name=name.replace("&", "&amp;")
                line=self.__t2+"<foaf:organization>"+name+"</foaf:organization>"
                oFile.write((line + "\n").encode('utf-8'))
                
                '''
                The country
                '''
                cc=det.get_country_code()
                line=self.__t2+"<gn:countryCode>"+cc+"</gn:countryCode>"
                oFile.write((line + "\n").encode('utf-8'))
                
                '''
                Close Affiliation </owl:NamedIndividual>
                '''
                line = self.__t1 + "</owl:NamedIndividual>"
                oFile.write((line + "\n").encode('utf-8'))
                
                oFile.write((self.__CLOSELINE__ + "\n").encode('utf-8'))
           
            #end loop idaffi 
                
        
        #end loop details
        iFile.write((self.__ENDAFFI__+"\n").encode('utf-8')) 
        iFile.write((self.__CLOSELINE__ + "\n").encode('utf-8'))
#         #use to debug
#         for a, bs in self.get_sha_2_affiliation().iteritems():
#             for b in bs:
#                 print "Author "+a +" hasAffiliation "+b
#                 
#         print ""
#         for p, auths in self.__p2auths.iteritems():
#             for auth in auths:
#                 print "Passcode "+p +" hasAuthEmail "+auth.get_email()
                  
        
        #end
            
        
    def get_pass_2_sha(self):
        return self.__pass2Sha


    def get_sha_2_affiliation(self):
        return self.__sha2Affiliation


    def set_pass_2_sha(self, value):
        self.__pass2Sha = value


    def set_sha_2_affiliation(self, value):
        self.__sha2Affiliation = value


    def del_pass_2_sha(self):
        del self.__pass2Sha


    def del_sha_2_affiliation(self):
        del self.__sha2Affiliation

    pass2Sha = property(get_pass_2_sha, set_pass_2_sha, del_pass_2_sha, "pass2Sha's docstring")
    sha2Affiliation = property(get_sha_2_affiliation, set_sha_2_affiliation, del_sha_2_affiliation, "sha2Affiliation's docstring")

    


    def get_affiliation_id_2_details(self):
        return self.__affiliationId2Details


   


    def set_affiliation_id_2_details(self, value):
        self.__affiliationId2Details = value


    


    def del_affiliation_id_2_details(self):
        del self.__affiliationId2Details

    sha2Affiliation = property(get_sha_2_affiliation, set_sha_2_affiliation, del_sha_2_affiliation, "sha2Affiliation's docstring")
    affiliationId2Details = property(get_affiliation_id_2_details, set_affiliation_id_2_details, del_affiliation_id_2_details, "affiliationId2Details's docstring")

    

    

    
