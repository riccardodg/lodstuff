#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on May 12, 2014

<owl:NamedIndividual rdf:about="&paper;1000X-P3J6P5G7A6">
        <rdf:type rdf:resource="&bibo;Article"/>
        <hasTopic>Topic2</hasTopic>
        <hasTopic>Topic1</hasTopic>
        <hasKeyword>K1</hasKeyword>
        <bibo:status rdf:resource="&paper;undecided"/>
        <bibo:authorList>
         <rdf:Seq>
            <rdf:li rdf:resource="http://example.org/author/Author1"/>;
            <rdf:li rdf:resource="http://example.org/author/Author2"/>;
            <rdf:li rdf:resource="http://example.org/author/Author3"/>;
         </rdf:Seq>
 </ bibo:authorList >
    </owl:NamedIndividual>
    
    add status such
    <owl:NamedIndividual rdf:about="&paper;undecided">
        <rdf:type rdf:resource="&bibo2;DocumentStatus"/>
    </owl:NamedIndividual>
@author: riccardo
'''
from shutil import copy2
from utils import shasum, pruneName
import codecs
import collections
import os


class SerializePaper(object):
    __t1="\t"
    __t2="\t\t"
    __t3="\t\t\t"
    __t4="\t\t\t\t"
    __t5="\t\t\t\t\t"
    __CLOSELINE__="</rdf:RDF>"
    __STARTPAPER__="\n\n<!-- Start Paper List -->\n"
    __ENDPAPER__="\n\n<!-- End Paper List -->\n"
    __STARTSTATUS__="\n\n<!-- Start Status List -->\n"
    __ENDSTATUS__="\n\n<!-- End Status List -->\n"
    __PAPERS__="papers/"
    __AUTHS__="authors/"
    __STATUS__="status/"
    
    #description files used when many files are created
    __INDEXOFPAPERS__="listofpapers"
    __INDEXOFSTATUS__="listofstatus"
    
    #dictionaries
    __pass2Shap=collections.defaultdict(list)
    __p2papers=collections.defaultdict(list)
    __paper2auths=collections.defaultdict(list)
    
    writefile=0
    headerfile=None
    '''
    
      conf+year+pid=pid
      status
      title
      category1
      category1
      keywords
    '''
    def __init__(self, p2ps, p2auths,writefile, outfile, headerfile,verbose,statusInBibo):
        #print "ZZZZ "+str(len(p2ps))
        self.__p2papers = p2ps
        self.__p2auths = p2auths
        self.writefile = writefile
        self.outfile = outfile
        self.headerfile = headerfile
        self.verbose = verbose
        self.statusInBibo=statusInBibo
        self.createPasscode2PaperIdsAndPaperIds2Authors(verbose)
        self.serializePapersAndAuthorList(verbose,writefile)
    
    
    '''
    Create a mapping between passcodes and ids of papers.
    Meanwhile map ids of papers to ids of authors
    '''
    def createPasscode2PaperIdsAndPaperIds2Authors(self,verbose):
        name="SerializePaper.createPasscode2PaperIdsAndPaperIds2Authors"
        p2pid=collections.defaultdict(list) #passcode2 papers
        p2as=collections.defaultdict(list) #paper id to auth id
        templistpid=[]
        templistida=[]
        if (verbose==1):
            print "\tExecuting "+name
        
        for p, papers in self.__p2papers.iteritems():
            for paper in papers:
                pid=str(paper.get_conf())+str(paper.get_year())+str(paper.get_pid())
                pid=shasum(pid)
                if not (pid in templistpid):
                    p2pid[p].append(pid)
                else:
                    if (verbose==1):
                        print "\t\tWARNING Paper Element "+pid+ "  appears many times" 
                        
                #managing authors
                
                auths=self.__p2auths.get(p)
                
                if auths is not None:
                    if (len(auths)==0):
                        if (verbose==1):
                            print "\t\tWARNING Paper Element "+pid+ " has No author"
                    else:
                        for a in auths:
                            chk=a.get_firstname()+"#"+a.get_lastname()
                            ida=shasum(a.get_email())
                            chk=chk+"#"+ida
                            if not (ida in templistida):
                                p2as[pid].append(chk)  
                                 
        #end for 
        self.set_paper_2auths(p2as)         
        self.set_pass_2_shap(p2pid)           
                          
    
    def readHeaderFileAndCopy2OutFile(self,src,dst,verbose):
        name ="SerializePaper.readHeaderFileAndCopy2OutFile"
        if os.path.isfile(dst):
            os.remove(dst)
            
        if (verbose==1):
            print "\t\t\tExecuting "+name
        
        copy2(src, dst)
    
    
    def serializePapersAndAuthorList(self,verbose,writefile):
        name ="SerializePaper.serializePapersAndAuthorList" 
        if verbose==1:
            print "\tExecuting "+name
        
        if writefile==0:
            
            src=self.headerfile
            dst=self.outfile
            self.readHeaderFileAndCopy2OutFile(src,dst,verbose)
            self.serializePapersAndAuthorListIntoSigleFile(verbose)
        else: 
            self.serializePapersAndAuthorListInManyFiles(verbose)                               
    
    
    '''
    topics and keywords not managed yet
    '''
    
    def serializePapersAndAuthorListIntoSigleFile(self,verbose):
        name ="SerializePaper.serializePapersAndAuthorListIntoSigleFile"   
        paper_serialized =set()
        paper_auth_serialized =set()
        paper_status_serialized =set()
        
        if (verbose==1):
            print "\t\tExecuting "+name

            
        oFile=codecs.open(self.outfile,'a','utf-8')
        oFile.write((self.__STARTPAPER__).encode('utf-8'))    
        for p, papers in self.__p2papers.iteritems():
            for paper in papers:
                '''
                create <owl:NamedIndividual rdf:about="&paper;#2d0249738f36125405e9333b23035856b20db21c">
                calculate the shasum1 of the email
                '''
                pid=str(paper.get_conf())+str(paper.get_year())+str(paper.get_pid())
                pid=shasum(pid)
                if pid in paper_serialized:
                    pass
                    #print p + " "+pid+ " "+paper.get_conf()
                else:
                    paper_serialized.add(pid)    
                    #print p + " "+pid+ " "+paper.get_conf()
                    line=self.__t1+"<owl:NamedIndividual rdf:about=\"&paper;#"+str(pid)+"\">"
                    oFile.write((line+"\n").encode('utf-8'))
                    
                    
                    '''
                    Create <rdf:type rdf:resource="&bibo;Article" />
                    '''
                    line=self.__t2+"<rdf:type rdf:resource=\"&bibo;Article\"/>"
                    oFile.write((line+"\n").encode('utf-8'))
                    
                    '''
                    create title
                    '''
                    title=paper.get_title()
                    title=title.replace("&", "&amp;")
                    line=self.__t2+"<dc:title>"+title+"</dc:title>"
                    oFile.write((line+"\n").encode('utf-8'))
                    
                    '''
                    create the status
                    '''
                    status=pruneName(paper.get_status(),"")
                    if not status in paper_status_serialized:
                        #print "XXXX "+status
                        paper_status_serialized.add(status)
                        
                        status=shasum(status)
                        
                        line= self.__t2+"<bibo:status rdf:resource=\"&paper;#"+status+"\"/>"
                        oFile.write((line+"\n").encode('utf-8'))
                    else:
                        pass
                        #print "ZZZ "+status
                    ''' create the authors'''
                    auths=self.get_paper_2auths()
                    #print auths
                    
                    if len(auths)>0:
                        line=self.__t2+"<bibo:authorList rdf:parseType=\"Collection\">"
                        oFile.write((line+"\n").encode('utf-8'))
                        line=self.__t3+"<rdf:Seq>"
                        #oFile.write((line+"\n").encode('utf-8'))
                        for a in auths.get(pid):
                            
                            #print a
                            if not (a in paper_auth_serialized):
                                #<rdf:Description rdf:about
                                line=self.__t3+"<rdf:Description rdf:about=\"&auth;#"+a.split("#")[2]+"\">"
                                oFile.write((line+"\n").encode('utf-8'))
                                line=self.__t4+"<rdfs:label>"+a.split("#")[1]+ " "+a.split("#")[0]+"</rdfs:label>"
                                oFile.write((line+"\n").encode('utf-8'))
                                line=self.__t3+"</rdf:Description>"
                                oFile.write((line+"\n").encode('utf-8'))
                            else:
                                if (verbose==1):
                                    print "\t\tWARNING Author Element "+a+ "  appears many times"
                                    
                        #line=self.__t3+"</rdf:Seq>"
                        #oFile.write((line+"\n").encode('utf-8'))
                        line=self.__t2+"</bibo:authorList>"
                        oFile.write((line+"\n").encode('utf-8'))
                    '''
                    Close paper </owl:NamedIndividual>
                    '''
                    line = self.__t1 + "</owl:NamedIndividual>"
                    oFile.write((line + "\n").encode('utf-8'))       
            
            #end for papers
        #end for passcode
        oFile.write((self.__ENDPAPER__ + "\n").encode('utf-8'))   
        oFile.write((self.__STARTSTATUS__ + "\n").encode('utf-8'))
        
        #write status
        for s in paper_status_serialized:
            '''
            <owl:NamedIndividual rdf:about="&paper;undecided">
                <rdf:type rdf:resource="&bibo2;DocumentStatus"/>
            </owl:NamedIndividual>
            '''
            
            ser=shasum(s)
            line=self.__t1+"<owl:NamedIndividual rdf:about=\"&paper;#"+ser+"\">"
            oFile.write((line + "\n").encode('utf-8'))  
            line=self.__t2+"<rdf:type rdf:resource=\"&paper;#status\"/>"
            oFile.write((line + "\n").encode('utf-8'))
            
            
            
            line=self.__t2+"<rdfs:label>"+s+"</rdfs:label>"
            oFile.write((line + "\n").encode('utf-8'))
            line=self.__t1+"</owl:NamedIndividual>"
            oFile.write((line + "\n").encode('utf-8'))
        
        oFile.write((self.__ENDSTATUS__ + "\n").encode('utf-8'))
        oFile.write((self.__CLOSELINE__ + "\n").encode('utf-8'))
        
        
        
        '''
        Create a list of papers which points to a single paper file.
        Each author in authorList points to a single author file
        ''' 
    def serializePapersAndAuthorListInManyFiles(self,verbose):
        name ="SerializePaper.serializePapersAndAuthorListInManyFiles" 
        paper_serialized =set() # auth_serialized =set()
        paper_auth_serialized =set() # auth_affi_serialized =set()
        paper_status_serialized =set()  #auth_affi_serialized =set()
        
        
        append_auth="authors"
        append_paper="papers"
        append_status="status"
        
        if (verbose==1):
            print "\t\tExecuting "+name

        
        #idx file
        idxfile=self.outfile+self.__INDEXOFPAPERS__
          
        copy2(self.headerfile, idxfile)
        iFile=codecs.open(idxfile,'a','utf-8')
        iFile.write((self.__STARTPAPER__+"\n").encode('utf-8')) 
        
        for p, papers in self.__p2papers.iteritems():
            for paper in papers:
                '''
                create <owl:NamedIndividual rdf:about="&paper;x/xyz/2d0249738f36125405e9333b23035856b20db21c">
                calculate the shasum1 of the email
                '''
                pid=str(paper.get_conf())+str(paper.get_year())+str(paper.get_pid())
                pid=shasum(pid)
                
                    
                if pid in paper_serialized:
                    pass
                    print pid
                else:
                    paper_serialized.add(pid)
                    #output file according to shasum
                    first_order_folder = str(pid[:1])
                    second_order_folder = str(pid[0:3])
                    if not os.path.exists(self.outfile+"/" + self.__PAPERS__+first_order_folder):
                        os.makedirs(self.outfile+"/" + self.__PAPERS__+"/"+first_order_folder)
                    if not os.path.exists(self.outfile+"/" + self.__PAPERS__+first_order_folder + "/" + second_order_folder):
                        os.makedirs(self.outfile+"/" + self.__PAPERS__+first_order_folder + "/" + second_order_folder)
                        
                    append_paper=self.__PAPERS__+first_order_folder + "/" + second_order_folder
                    
                    #write description file
                    title=paper.get_title()
                    title=title.replace("&", "&amp;")
                    iLine=self.__t1+"<rdf:Description rdf:about=\"&paper;"+append_paper+"/"+str(pid)+"\">"
                    iFile.write((iLine+"\n").encode('utf-8')) 
                    iLine=self.__t2+"<dc:title>"+title+"</dc:title>"
                    iFile.write((iLine+"\n").encode('utf-8')) 
                    iLine=self.__t1+"</rdf:Description>"
                    iFile.write((iLine+"\n").encode('utf-8')) 
                    
                    
                      
                    dst=self.outfile+"/"+append_paper+"/"+pid
                    copy2(self.headerfile, dst)
                    oFile=codecs.open(dst,'a','utf-8')  
                    #oFile.write((self.__STARTAUTH__+"\n").encode('utf-8'))
                    
                    line=self.__t1+"<owl:NamedIndividual rdf:about=\"&paper;"+append_paper+"/"+str(pid)+"\">"
                    oFile.write((line+"\n").encode('utf-8'))    
                
                    '''
                    Create <rdf:type rdf:resource="&bibo;/Article"/>
                    '''
                    line=self.__t2+"<rdf:type rdf:resource=\"&bibo;Article\"/>"
                    oFile.write((line+"\n").encode('utf-8'))
                
                    '''
                    create title
                    '''
                    title=paper.get_title()
                    title=title.replace("&", "&amp;")
                    line=self.__t2+"<dc:title>"+title+"</dc:title>"
                    oFile.write((line+"\n").encode('utf-8'))  
                
                    '''
                    create the status
                    '''
                    status=pruneName(paper.get_status(),"")
                    if not status in paper_status_serialized:
                        #print "XXXX "+status
                        paper_status_serialized.add(status)
                        ser=shasum(status)
                        first_order_folder = str(ser[:1])
                        second_order_folder = str(ser[0:3])
                        append_status=self.__STATUS__+first_order_folder + "/" + second_order_folder
                        line= self.__t2+"<bibo:status rdf:resource=\"&paper;"+append_status+"/"+ser+"\"/>"
                        oFile.write((line+"\n").encode('utf-8'))
                    else:
                        pass
                        #print "ZZZ "+status  
                    
                    ''' create the authors'''
                    auths=self.get_paper_2auths()
                    #print len(auths)
                    if len(auths)>0:
                        line=self.__t2+"<bibo:authorList rdf:parseType=\"Collection\">"
                        oFile.write((line+"\n").encode('utf-8'))
#                         line=self.__t3+"<rdf:Seq>"
#                         oFile.write((line+"\n").encode('utf-8'))
                        for a in auths.get(pid):
                            if not (a in paper_auth_serialized):
                                ida=a.split("#")[2]
                                first_order_folder = str(ida[:1])
                                second_order_folder = str(ida[0:3])
                                append_auth=self.__AUTHS__+first_order_folder + "/" + second_order_folder+"/"
                                line=self.__t3+"<rdf:Description rdf:about=\"&auth;"+append_auth+ida+"\">"
                                oFile.write((line+"\n").encode('utf-8'))
                                line=self.__t4+"<rdfs:label>"+a.split("#")[1]+ " "+a.split("#")[0]+"</rdfs:label>"
                                oFile.write((line+"\n").encode('utf-8'))
                                line=self.__t3+"</rdf:Description>"
                                oFile.write((line+"\n").encode('utf-8'))
                               
                            else:
                                if (verbose==1):
                                    print "\t\tWARNING Author Element "+a+ "  appears many times"
                                    
#                         line=self.__t3+"</rdf:Seq>"
#                         oFile.write((line+"\n").encode('utf-8'))
                        line=self.__t2+"</bibo:authorList>"
                        oFile.write((line+"\n").encode('utf-8'))
                    
                    '''
                    Close paper </owl:NamedIndividual>
                    '''
                    line = self.__t1 + "</owl:NamedIndividual>"
                    oFile.write((line + "\n").encode('utf-8'))    
                
                    
                        
                    oFile.write((self.__CLOSELINE__ + "\n").encode('utf-8'))       
            
            #end for author
        #end for passcode
        iFile.write((self.__ENDPAPER__+"\n").encode('utf-8'))
        iFile.write((self.__CLOSELINE__ + "\n").encode('utf-8'))    
        
        
        '''
        Each status in a distinct file
        '''
        #idx file
        idxfile=self.outfile+"/"+self.__INDEXOFSTATUS__
        copy2(self.headerfile, idxfile)
        iFile=codecs.open(idxfile,'a','utf-8')
        iFile.write((self.__STARTSTATUS__+"\n").encode('utf-8'))
        #write status
        for s in paper_status_serialized:
            '''
            <owl:NamedIndividual rdf:about="&paper;undecided">
                <rdf:type rdf:resource="&bibo2;DocumentStatus"/>
            </owl:NamedIndividual>
            '''
            
            ser=shasum(s)
            first_order_folder = str(ser[:1])
            second_order_folder = str(ser[0:3])
            if not os.path.exists(self.outfile+"/" + self.__STATUS__+first_order_folder):
                os.makedirs(self.outfile+"/" + self.__STATUS__+"/"+first_order_folder)
            if not os.path.exists(self.outfile+"/" + self.__STATUS__+first_order_folder + "/" + second_order_folder):
                os.makedirs(self.outfile+"/" + self.__STATUS__+first_order_folder + "/" + second_order_folder)
            append_status=self.__STATUS__+first_order_folder + "/" + second_order_folder
            dst=self.outfile+"/"+append_status+"/"+ser
            copy2(self.headerfile, dst)
            oFile=codecs.open(dst,'a','utf-8')
            #write description file 
            iLine=self.__t1+"<rdf:Description rdf:about=\"&paper;"+append_status+"/"+str(ser)+"\"></rdf:Description>"
            iFile.write((iLine+"\n").encode('utf-8'))    
            line=self.__t1+"<owl:NamedIndividual rdf:about=\"&paper;#"+ser+"\">"
            oFile.write((line + "\n").encode('utf-8'))  
            line=self.__t2+"<rdf:type rdf:resource=\"&paper;#status\"/>"
            oFile.write((line + "\n").encode('utf-8'))
            
            line=self.__t2+"<rdfs:label>"+s+"</rdfs:label>"
            oFile.write((line + "\n").encode('utf-8'))
            line=self.__t1+"</owl:NamedIndividual>"
            oFile.write((line + "\n").encode('utf-8'))
        
            
            oFile.write((self.__CLOSELINE__ + "\n").encode('utf-8'))
         
        
        iFile.write((self.__ENDSTATUS__ + "\n").encode('utf-8'))
        iFile.write((self.__CLOSELINE__ + "\n").encode('utf-8'))
#         #use to debug
#         for a, bs in self.get_sha_2_affiliation().iteritems():
#             for b in bs:
#                 print "Author "+a +" hasAffiliation "+b
#                 
#         print ""
#         for p, papers in self.__p2auths.iteritems():
#             for auth in papers:
#                 print "Passcode "+p +" hasAuthEmail "+auth.get_email()
                   
         
        #end               
    
    def get_paper_2auths(self):
        return self.__paper2auths


    def set_paper_2auths(self, value):
        self.__paper2auths = value


    def del_paper_2auths(self):
        del self.__paper2auths

    paper2auths = property(get_paper_2auths, set_paper_2auths, del_paper_2auths, "paper2auths's docstring")

    def get_pass_2_shap(self):
        return self.__pass2Shap


    def set_pass_2_shap(self, value):
        self.__pass2Shap = value


    def del_pass_2_shap(self):
        del self.__pass2Shap

    pass2Shap = property(get_pass_2_shap, set_pass_2_shap, del_pass_2_shap, "pass2Shap's docstring")

    def get_p_2papers(self):
        return self.__p2papers


    def set_p_2papers(self, value):
        self.__p2papers = value


    def del_p_2papers(self):
        del self.__p2papers

    p2papers = property(get_p_2papers, set_p_2papers, del_p_2papers, "p2papers's docstring")
