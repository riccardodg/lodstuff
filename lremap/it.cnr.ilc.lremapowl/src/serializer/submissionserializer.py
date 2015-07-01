'''
Created on Jun 5, 2014


<owl:NamedIndividual rdf:about="&sub;#S1">
        <rdf:type rdf:resource="&dcmi;/Event"/>
        <dcterms:references rdf:resource="&paper;#P1"/>
        <dcterms:references rdf:resource="&swc;#C1"/>
         <dc:identifier>passcode</dc:identifier>
    </owl:NamedIndividual>
    
@author: riccardo
'''
from shutil import copy2
from utils import shasum
import codecs
import collections
import os
import utils

class SerializeSubmission(object):
    __t1="\t"
    __t2="\t\t"
    __t3="\t\t\t"
    __t4="\t\t\t\t"
    __t5="\t\t\t\t\t"
    __CLOSELINE__="</rdf:RDF>"
    __STARTSUB__="\n\n<!-- Start Submission List -->\n"
    __ENDSUB__="\n\n<!-- End Submission List -->\n"
    __PAPERS__="papers/"
    __SUBS__="submissions/"
    
    #description files used when many files are created
    __INDEXOFSUBS__="listofsubmissions"
    
    
    #dictionaries
    __pass2subs=collections.defaultdict(list)
    __pass2confs=collections.defaultdict(list) # from passcode to id conferences
    __pass2papers=collections.defaultdict(list) # from passcode to id papers
    __pass2paperObj=collections.defaultdict(list) # from passcode to  papers objects
   
    
    writefile=0
    headerfile=None
    
    def __init__(self, p2subs, p2confs,p2papers,writefile, outfile, headerfile,verbose):
        self.__p2subs=p2subs
        self.__p2confs=p2confs
        self.__p2papers=p2papers
        self.writefile = writefile
        self.outfile = outfile
        self.headerfile = headerfile
        self.verbose = verbose
        self.createPasscode2SubsIdsAndSubsId2PapersAndSubsId2Confs(verbose)
        self.serializeSubmissionsAndPapersAndConfs(verbose, writefile)
        
        
        
    def createPasscode2SubsIdsAndSubsId2PapersAndSubsId2Confs(self,verbose):
        name="SerializeSubmission.createPasscode2SubsIdsAndSubsId2PapersAndSubsId2Confs"
        p2subs=collections.defaultdict(list) #passcode2 subid
        p2ps=collections.defaultdict(list) #paper id to paper id   
        p2cs=collections.defaultdict(list) #paper id to conf id  
        p2pobj= collections.defaultdict(list) #paper id to paper obj  
        templistpid=[]
        templistconfid=[]
        templistsubid=[]
        if (verbose==1):
            print "\tExecuting "+name
        for p, subs in self.__p2subs.iteritems():
            papers=self.__p2papers.get(p)
            confs=self.__p2confs.get(p)
            
            for s in subs:
                subid=s.get_conf()+s.get_year()+"#"+s.get_passcode()
                if not (subid in templistsubid):
                    templistsubid.append(subid)
                    p2subs[p].append(subid)
                if papers is not None:
                    for paper in papers:
                        pid=str(paper.get_conf())+str(paper.get_year())+str(paper.get_pid())
                        pid=shasum(pid)
                        if not (pid in templistpid):
                            templistpid.append(pid)
                            p2ps[p].append(pid)
                            p2pobj[p].append(paper)
                    
                if confs is not None:
                    for conf in confs:
                        idc= conf.get_conf()
                        idy= conf.get_year()
                        idx=idc+idy
                        
                        idx =utils.pruneName(idx, " ")
                        
                        if not (idx in templistconfid):
                            templistconfid.append(idx)
                        p2cs[p].append(idc+idy)
                        
                             
                     
        self.set_pass_2subs(p2subs)
        self.set_pass_2papers(p2ps)
        self.set_pass_2confs(p2cs)
        self.set_pass_2paper_obj(p2pobj)        
        # for debug
#         print "\n##SUBS##"
#         for  p, subs in   p2subs.iteritems():
#             for s in subs:
#                 print p +" "+s
#                 
#         print "\n##PAPERS##"
#         for  p, papers in   p2ps.iteritems():
#             for s in papers:
#                 print p +" "+s        
#         
#         print "\n##CONFSS##"
#         for  p, confs in   p2cs.iteritems():
#             for s in confs:
#                 print p +" "+s

    
    def readHeaderFileAndCopy2OutFile(self,src,dst,verbose):
        name ="SerializeSubmission.readHeaderFileAndCopy2OutFile"
        if os.path.isfile(dst):
            os.remove(dst)
            
        if (verbose==1):
            print "\t\t\tExecuting "+name
        
        copy2(src, dst)
    
    def serializeSubmissionsAndPapersAndConfs(self,verbose,writefile):
        name ="SerializeSubmission.serializeSubmissionsAndPapersAndConfs" 
        if verbose==1:
            print "\tExecuting "+name
        
        if writefile==0:
            
            src=self.headerfile
            dst=self.outfile
            self.readHeaderFileAndCopy2OutFile(src,dst,verbose)
            self.serializeSubmissionsAndPapersAndConfsIntoSigleFile(verbose)
        else: 
            self.serializeSubmissionsAndPapersAndConfsInManyFiles(verbose)  

    
    def serializeSubmissionsAndPapersAndConfsIntoSigleFile(self,verbose):
        name ="SerializeSubmission.serializeSubmissionsAndPapersAndConfsIntoSigleFile"   
        sub_serialized =set()
        sub_paper_serialized =set()
        sub_conf_serialized =set()
        
        if (verbose==1):
            print "\t\tExecuting "+name

            
        oFile=codecs.open(self.outfile,'a','utf-8')
        oFile.write((self.__STARTSUB__).encode('utf-8'))    
        for p, subs in self.__p2subs.iteritems():
            for s in subs:
                '''
                create <owl:NamedIndividual rdf:about="&sub;#S1">
                    <rdf:type rdf:resource="&dcmi;/Event"/>
                '''
                subid=s.get_conf()+s.get_year()+"-"+s.get_passcode()
#                 pid=str(paper.get_conf())+str(paper.get_year())+str(paper.get_pid())
#                 pid=shasum(pid)
                if subid in sub_serialized:
                    pass
                    #print p + " "+pid+ " "+paper.get_conf()
                else:
                    sub_serialized.add(subid)    
                    #print p + " "+pid+ " "+paper.get_conf()
                    line=self.__t1+"<owl:NamedIndividual rdf:about=\"&sub;#"+str(subid)+"\">"
                    oFile.write((line+"\n").encode('utf-8'))
                    line=self.__t2+"<rdf:type rdf:resource=\"&dcmi;/Event\"/>"
                    oFile.write((line + "\n").encode('utf-8')) 
                    line=self.__t2+"<dc:identifier>"+s.get_passcode()+"</dc:identifier>"
                    oFile.write((line + "\n").encode('utf-8')) 
                    
                    
                    
                    '''
                    Create <dcterms:references rdf:resource="&paper;#P1"/>
                    '''
                   
                     
                    pids=self.get_pass_2papers().get(p)
                    if pids is not None:
                        for pid in pids:
                            if not (pid in sub_paper_serialized):
                                sub_paper_serialized.add(pid)
                                line=self.__t2+"<dcterms:references rdf:resource=\"&paper;#"+str(pid)+"\"/>"
                                oFile.write((line+"\n").encode('utf-8'))
                     
                    
                    
                    '''
                    Create <dcterms:references rdf:resource="&swc;#C1"/>
                    '''
                    
                     
                    confs=self.get_pass_2confs().get(p)
                    if confs is not None:
                        for conf in confs:
                            
                            sub_conf_serialized.add(conf)
                            line=self.__t2+"<dcterms:references rdf:resource=\"&conf;#"+str(conf)+"\"/>"
                            oFile.write((line+"\n").encode('utf-8'))
                     
                    line = self.__t1 + "</owl:NamedIndividual>"
                    oFile.write((line + "\n").encode('utf-8'))

         
        oFile.write((self.__ENDSUB__ + "\n").encode('utf-8'))
        oFile.write((self.__CLOSELINE__ + "\n").encode('utf-8'))
    
    
    '''
        Create a list of submissions which point to a single  file.
        Each author in authorList points to a single author file
        ''' 
    def serializeSubmissionsAndPapersAndConfsInManyFiles(self,verbose):
        name ="SerializeSubmission.serializeSubmissionsAndPapersAndConfsInManyFiles" 
        sub_serialized =set()
        sub_paper_serialized =set()
        sub_conf_serialized =set()
        
        
        append_paper="papers"
        append_subs="submissions"
        
        if (verbose==1):
            print "\t\tExecuting "+name

        
        #idx file
        idxfile=self.outfile+self.__INDEXOFSUBS__
          
        copy2(self.headerfile, idxfile)
        iFile=codecs.open(idxfile,'a','utf-8')
        iFile.write((self.__STARTSUB__+"\n").encode('utf-8'))
        
        for p, subs in self.__p2subs.iteritems():
            for s in subs:
                '''
                create <owl:NamedIndividual rdf:about="&sub;#S1">
                    <rdf:type rdf:resource="&dcmi;/Event"/>
                '''
                subid=s.get_conf()+s.get_year()+"-"+s.get_passcode()
#                 pid=str(paper.get_conf())+str(paper.get_year())+str(paper.get_pid())
#                 pid=shasum(pid)
                if subid in sub_serialized:
                    pass
                    #print p + " "+pid+ " "+paper.get_conf()
                else:
                    sub_serialized.add(subid)
                    sid=shasum(subid)
                    first_order_folder = str(sid[:1])
                    second_order_folder = str(sid[0:3])
                    if not os.path.exists(self.outfile+"/" + self.__SUBS__+first_order_folder):
                        os.makedirs(self.outfile+"/" + self.__SUBS__+"/"+first_order_folder)
                    if not os.path.exists(self.outfile+"/" + self.__SUBS__+first_order_folder + "/" + second_order_folder):
                        os.makedirs(self.outfile+"/" + self.__SUBS__+first_order_folder + "/" + second_order_folder)
                        
                    append_subs=self.__SUBS__+first_order_folder + "/" + second_order_folder
                    iLine=self.__t1+"<rdf:Description rdf:about=\"&sub;"+append_subs+"/"+str(subid)+"\">"
                    iFile.write((iLine+"\n").encode('utf-8')) 
                    iLine=self.__t2+"<dc:identifier>"+p+"</dc:identifier>"
                    iFile.write((iLine+"\n").encode('utf-8')) 
                    iLine=self.__t1+"</rdf:Description>"
                    iFile.write((iLine+"\n").encode('utf-8'))
                    
                    dst=self.outfile+"/"+append_subs+"/"+subid
                    copy2(self.headerfile, dst)
                    oFile=codecs.open(dst,'a','utf-8')  
                    #oFile.write((self.__STARTAUTH__+"\n").encode('utf-8'))
                    
                    line=self.__t1+"<owl:NamedIndividual rdf:about=\"&sub;"+append_subs+"/"+str(subid)+"\">"
                    oFile.write((line+"\n").encode('utf-8'))
                    #get the paper 
                    
                    pids=self.get_pass_2papers().get(p)
                    if pids is not None:
                        for pid in pids:
                            if not (pid in sub_paper_serialized):
                                sub_paper_serialized.add(pid)
                                first_order_folder = str(pid[:1])
                                second_order_folder = str(pid[0:3])
                                append_paper=self.__PAPERS__+first_order_folder + "/" + second_order_folder
                                line=self.__t2+"<dcterms:references rdf:resource=\"&paper;"+append_paper+"/"+str(pid)+"\"/>"
                                oFile.write((line+"\n").encode('utf-8'))
                                # add a label for the title
                                papers = self.get_pass_2paper_obj().get(p)
                                if papers is not None:
                                    #print papers
                                    for paper in papers:
                                        title=paper.get_title()
                                        title=title.replace("&", "&amp;")
                                        line=self.__t2+"<rdfs:label>"+title+"</rdfs:label>"
                                        oFile.write((line+"\n").encode('utf-8')) 
                     
                    
                    
                    '''
                    Create <dcterms:references rdf:resource="&swc;#C1"/>
                    '''
                    
                     
                    confs=self.get_pass_2confs().get(p)
                    if confs is not None:
                        for conf in confs:
                            
                            sub_conf_serialized.add(conf)
                            line=self.__t2+"<dcterms:references rdf:resource=\"&conf;#"+str(conf)+"\"/>"
                            oFile.write((line+"\n").encode('utf-8'))
                     
                    line = self.__t1 + "</owl:NamedIndividual>"
                    oFile.write((line + "\n").encode('utf-8'))

         
                    oFile.write((self.__ENDSUB__ + "\n").encode('utf-8'))
                    oFile.write((self.__CLOSELINE__ + "\n").encode('utf-8'))
                    
        iFile.write((self.__ENDSUB__+"\n").encode('utf-8'))
        iFile.write((self.__CLOSELINE__ + "\n").encode('utf-8'))   
        
    def get_pass_2subs(self):
        return self.__pass2subs


    def set_pass_2subs(self, value):
        self.__pass2subs = value


    def del_pass_2subs(self):
        del self.__pass2subs

    pass2subs = property(get_pass_2subs, set_pass_2subs, del_pass_2subs, "pass2subs's docstring")

    def get_pass_2confs(self):
        return self.__pass2confs


    def get_pass_2papers(self):
        return self.__pass2papers


    def set_pass_2confs(self, value):
        self.__pass2confs = value


    def set_pass_2papers(self, value):
        self.__pass2papers = value


    def del_pass_2confs(self):
        del self.__pass2confs


    def del_pass_2papers(self):
        del self.__pass2papers

    pass2confs = property(get_pass_2confs, set_pass_2confs, del_pass_2confs, "pass2confs's docstring")
    pass2papers = property(get_pass_2papers, set_pass_2papers, del_pass_2papers, "pass2papers's docstring")

    def get_pass_2paper_obj(self):
        return self.__pass2paperObj


    def set_pass_2paper_obj(self, value):
        self.__pass2paperObj = value


    def del_pass_2paper_obj(self):
        del self.__pass2paperObj

    pass2paperObj = property(get_pass_2paper_obj, set_pass_2paper_obj, del_pass_2paper_obj, "pass2paperObj's docstring")

    

    
        
