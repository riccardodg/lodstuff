#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Jun 19, 2014

Create the resource
check if the resourcetype is in the list of available types. If not create the subclass:

<!-- http://www.resourcebook.eu/lremap/owl/lremap_ri.owl#MyRT -->

    <owl:Class rdf:about="&ri;MyRT">
        <rdfs:subClassOf rdf:resource="&lremap;ResourceType"/>
    </owl:Class>

then create the resourcename
<!-- http://www.resourcebook.eu/lremap/owl/lremap_ri.owl#myname -->

    <owl:NamedIndividual rdf:about="&ri;myname">
        <rdf:type rdf:resource="&lremap;ResourceName"/>
    </owl:NamedIndividual>
    
Finally

<!-- http://www.resourcebook.eu/lremap/owl/lremap_ri.owl#newres -->

    <owl:NamedIndividual rdf:about="&ri;newres">
        <rdf:type rdf:resource="&ri;MyRT"/>
        <lremap:hasResourceName rdf:resource="&ri;myname"/>
    </owl:NamedIndividual>

If the type is in the list 
create the resourcename
<!-- http://www.resourcebook.eu/lremap/owl/lremap_ri.owl#myname -->

    <owl:NamedIndividual rdf:about="&ri;myname">
        <rdf:type rdf:resource="&lremap;ResourceName"/>
    </owl:NamedIndividual>
    
     <!-- http://www.resourcebook.eu/lremap/owl/lremap_ri.owl#MyCorpus -->
Finally
    <owl:NamedIndividual rdf:about="&ri;MyCorpus">
        <rdf:type rdf:resource="&lremap;Corpus"/>
        <lvont:language rdf:resource="&lexvo;id/iso639-3/ita"/>
        <lremap:hasResourceLanguageType rdf:resource="&lremap;Bi"/>
        <lremap:hasResourceAvailability rdf:resource="&lremap;Freely_Available"/>
        <lremap:hasResourceName rdf:resource="&ri;myname"/>
    </owl:NamedIndividual>       
@author: riccardo
'''
from shutil import copy2
from utils import pruneName, modifyString, shasum
import codecs
import collections
import os
import sys


class SerializeResource(object):
    __t1="\t"
    __t2="\t\t"
    __t3="\t\t\t"
    __t4="\t\t\t\t"
    __CLOSELINE__="</rdf:RDF>"
    __STARTRES__="\n\n<!-- Start Resource List -->\n"
    __ENDRES__="\n\n<!-- End Resource List -->\n"
    __RIDSEP__="-"
    
    __STARTRESCLS__="\n\n<!-- Start Resource Class List -->\n"
    __ENDRESCLS__="\n\n<!-- End Resource Class List -->\n"
    
    __STARTRESNAMES__="\n\n<!-- Start Resource Names List -->\n"
    __ENDRESNAMES__="\n\n<!-- End Resource Names List -->\n"
    
    __STARTRESAVAILS__="\n\n<!-- Start Resource Avails List -->\n"
    __ENDRESAVAILS__="\n\n<!-- End Resource Avails List -->\n"
    
    __STARTRESSTATUS__="\n\n<!-- Start Resource Status List -->\n"
    __ENDRESSTATUS__="\n\n<!-- End Resource Status List -->\n"
    
    __STARTRESMODS__="\n\n<!-- Start Resource Modality List -->\n"
    __ENDRESMODS__="\n\n<!-- End Resource Modality List -->\n"
    
    __STARTRESUSES__="\n\n<!-- Start Resource Uses List -->\n"
    __ENDRESUSES__="\n\n<!-- End Resource Uses List -->\n"
    
    __SUBS__="submissions/"
    __RES__="resources/"
    __INDEXOFRES__="listofresources"
    
    #dictionaries
    __p2ris=collections.defaultdict(list)
    __p2subs=collections.defaultdict(list)
    __rid2ris=collections.defaultdict(list)
    writefile=0
    outfile=sys.stdout
    headerfile=None
    
    __RTYPES__=[]
    __RAVAILS__=[]
    __RSTATUS__=[]
    __RSTATUS__=[]
    __RMODS__ =[]
    __RUSES__ =[]
    
    #stats dictionaries
    __newrtypeNumOfInstances=collections.defaultdict(set)

    def __init__(self, p2ris, p2subs,writefile, outfile, headerfile,verbose,dbtypes,avails, statuses,mods, uses):
        self.__p2ris = p2ris
        self.__p2subs = p2subs
        self.writefile = writefile
        self.outfile = outfile
        self.headerfile = headerfile
        self.verbose = verbose
        self.__RTYPES__ = dbtypes
        self.__RAVAILS__ = avails
        self.__RSTATUS__ = statuses
        self.__RMODS__ = mods
        self.__RUSES__ = uses
#         
        self.createPasscode2ResourceIdsAndResourceIds2SubmisionIds(verbose)
        self.serializeResources(verbose,writefile)
        
    
    '''
    Create a mapping between passcodes and ids of resources.
    Meanwhile map ids to affiliations in order to manage 1 auth with many institutions
    '''    
    def createPasscode2ResourceIdsAndResourceIds2SubmisionIds(self, verbose):
        name="SerializeResource.createPasscode2ResourceIdsAndResourceIds2SubmisionIds" 
        p2ri=collections.defaultdict(list) #passcode 2 rid
        p2s=collections.defaultdict(list) #passcode 2 subid
        rid2ris=collections.defaultdict(list)
        templistrid=[]
        templistsubid=[]
        if (verbose==1):
            print "\tExecuting "+name
        for p, ris in self.__p2ris.iteritems():
            for ri in ris:
                status=pruneName(ri.get_prodstatus(),"")
                status=modifyString(status,"/","_")
                pname=pruneName(ri.get_name(),"")
                pname=modifyString(pname,"/","-")
                pname=pname.replace("&", "&amp;")
                subid=ri.get_conf()+ri.get_year()+self.__RIDSEP__+ri.get_passcode()
                rid=subid+self.__RIDSEP__+ri.get_type()+self.__RIDSEP__+pname+self.__RIDSEP__+status
                #print rid#.get_type() #
                if not (rid in templistrid):
                    templistrid.append(rid)
                    p2ri[p].append(rid)
                    #print rid#.get_type() #
                    rid2ris[rid].append(ri)
                if not (subid in templistsubid):
                    templistsubid.append(subid)
                    p2s[p].append(subid)    
                    
        self.set_p_2ris(p2ri) 
        self.set_p_2subs(p2s)     
        self.set_rid_2ris(rid2ris) 
        #print self.__RTYPES__
        
        
    def readHeaderFileAndCopy2OutFile(self,src,dst,verbose):
        name ="SerializeResource.readHeaderFileAndCopy2OutFile"
        if os.path.isfile(dst):
            os.remove(dst)
            
        if (verbose==1):
            print "\t\t\tExecuting "+name
        
        copy2(src, dst)
        
    def serializeResources(self,verbose,writefile):
        name ="SerializeResource.serializeResources" 
        if verbose==1:
            print "\tExecuting "+name
        
        if writefile==0:
            
            src=self.headerfile
            dst=self.outfile
            self.readHeaderFileAndCopy2OutFile(src,dst,verbose)
            self.serializeResourcesIntoSigleFile(verbose)
        else: 
            self.serializeResourcesIntoManyFile(verbose) 
             
    def serializeResourcesIntoSigleFile(self,verbose):
        name ="SerializeResource.serializeResourcesIntoSigleFile"   
        rtype_subclassed =set()
        newrtype =collections.defaultdict(set)
        names_serialized =set()
        avails_serialized =set()
        status_serialized =set()
        mods_serialized =set()
        l1_serialized =set()
        uses_serialized =set()
        
        ns="&lremap;"
        #print self.get_rid_2ris()
        if (verbose==1):
            print "\t\tExecuting "+name

            
        oFile=codecs.open(self.outfile,'a','utf-8')
        oFile.write((self.__STARTRES__).encode('utf-8'))  
        for p, rids in self.get_p_2ris().iteritems():
            for rid in rids:
                '''
                prepare the structure for new classes
                '''
                ris=self.get_rid_2ris().get(rid)
                if ris is not None:
                    for ri in ris:
                        #print rid + " "+ str(ri)
                        rtype=ri.get_type()
                        #print rid + " "+ str(rtype)
                        rtype=pruneName(rtype, "")
                        #rtype="Language_Resources/Technologies_Infrastructure"
                        rtype=modifyString(rtype,"/","-")
                        rtype=rtype.replace("&", "&amp;")
                        if not (rtype in self.__RTYPES__):
                            ns="&ri;#"
                            if not rtype in rtype_subclassed:
                                #print "SUB CLASS "+ rtype 
                                rtype_subclassed.add(rtype)
                                newrtype[rtype].add(1)
                                
                            else:
                                
                                nrc=newrtype.get(rtype)
                                if nrc is not None:
                                    for num in nrc:
                                        #print num
                                        del newrtype[rtype]
                                        newrtype[rtype].add(num+1)
                                else:
                                    if (self.verbose==1):
                                        print "\t\t Warning resource type "+rtype+ " NOT YET ENCOUNTERED"        
                        else:
                            ns="&lremap;"  
                        
                        '''
                        create the resourcename
                            <owl:NamedIndividual rdf:about="&ri;myname">
                                <rdf:type rdf:resource="&lremap;ResourceName"/>
                            </owl:NamedIndividual>
                        '''  
                            
                        rid=shasum(rid)
                        line=self.__t1+"<owl:NamedIndividual rdf:about=\"&ri;#"+rid+ "\">" 
                        oFile.write((line + "\n").encode('utf-8'))
                        line=self.__t2+"<rdf:type rdf:resource=\""+ns+rtype+"\"/>" 
                        oFile.write((line + "\n").encode('utf-8'))     
                        rname=ri.get_name()
                        #print rid + " "+ str(rtype)
                        rname=pruneName(rname, "")
                        rname=modifyString(rname,"^","-")
                        #rname="-"
                        rname=rname.replace("&", "&amp;")
                        if not (rname in names_serialized):
                            names_serialized.add(rname)
                        
                        #avail="Freely_Available_aaa"    
                        avail= ri.get_avail()
                        
                        if avail is not None:
                            
                            avail=pruneName(avail, "")
                            avail=modifyString(avail,"^","-")
                            avail=avail.replace("&", "&amp;")
                            if not (avail in self.__RAVAILS__):
                                avails_serialized.add(avail)
                                line=self.__t2+"<lremap:hasResourceAvailability rdf:resource=\"&ri;#"+avail+ "\"/>" 
                            else:
                                line=self.__t2+"<lremap:hasResourceAvailability rdf:resource=\"&lremap;"+avail+ "\"/>"
                                    
                            oFile.write((line + "\n").encode('utf-8'))
                        
                        status= ri.get_prodstatus()
                        if (status is not None) and (status != "NoStatus"):
                            
                            status=pruneName(status, "")
                            status=modifyString(status,"^","-")
                            status=status.replace("&", "&amp;")
                            if not (status in self.__RSTATUS__):
                                status_serialized.add(status)
                                line=self.__t2+"<lremap:hasResourceStatus rdf:resource=\"&ri;#"+status+ "\"/>"
                            else:
                                line=self.__t2+"<lremap:hasResourceStatus rdf:resource=\"&lremap;"+status+ "\"/>"
                                    
                            oFile.write((line + "\n").encode('utf-8'))
                            
                        
                        mod= ri.get_modality()
                        
                        if mod is not None:
                            
                            mod=pruneName(mod, "")
                            mod=modifyString(mod,"^","-")
                            mod=mod.replace("&", "&amp;")
                            if not (mod in self.__RMODS__):
                                mods_serialized.add(mod)
                                line=self.__t2+"<lremap:hasResourceModality rdf:resource=\"&ri;#"+mod+ "\"/>" 
                            else:
                                line=self.__t2+"<lremap:hasResourceModality rdf:resource=\"&lremap;"+mod+ "\"/>"
                                    
                            oFile.write((line + "\n").encode('utf-8'))
                            
                        
                        use= ri.get_resourceusage()
                        
                        if use is not None:
                            
                            use=pruneName(use, "")
                            use=modifyString(use,"^","-")
                            use=use.replace("&", "&amp;")
                            if not (use in self.__RUSES__):
                                uses_serialized.add(use)
                                line=self.__t2+"<lremap:hasResourceUse rdf:resource=\"&ri;#"+use+ "\"/>" 
                            else:
                                line=self.__t2+"<lremap:hasResourceUse rdf:resource=\"&lremap;"+use+ "\"/>"
                                    
                            oFile.write((line + "\n").encode('utf-8'))            
                        
                        '''
                        create the individual with all properties
                            <owl:NamedIndividual rdf:about="&ri;MyCorpus">
                                <rdf:type rdf:resource="&lremap;Corpus"/>
                                <lvont:language rdf:resource="&lexvo;id/iso639-3/ita"/>
                                <lremap:hasResourceLanguageType rdf:resource="&lremap;Bi"/>
                                <lremap:hasResourceAvailability rdf:resource="&lremap;Freely_Available"/>
                                <lremap:hasResourceName rdf:resource="&ri;myname"/>
                            </owl:NamedIndividual> 
                        '''  
                        
                        
                        line=self.__t2+"<lremap:hasResourceName rdf:resource=\"&ri;#"+rname.decode(encoding='UTF-8',errors='strict')+ "\"/>" 
                        #oFile.write((line + "\n").encode('utf-8'))
                        oFile.write(line+"\n")
                        
                    
                        
                        
                            
                            
                        # referencing submissions
                        pids =self.get_p_2subs().get(p)
                        
                        if pids is not None:
                            for pid in pids:
                                line=self.__t2+"<dcterms:references rdf:resource=\"&sub;#"+str(pid)+"\"/>"
                                oFile.write((line + "\n").encode('utf-8')) 
                        #closing individual
                        line=self.__t1+"</owl:NamedIndividual>" 
                        oFile.write((line + "\n").encode('utf-8'))                    
                                        
        oFile.write((self.__ENDRES__ + "\n").encode('utf-8'))
        
        # create subclass
        oFile=codecs.open(self.outfile,'a','utf-8')
        oFile.write((self.__STARTRESCLS__).encode('utf-8'))    
        '''
                create  <owl:Class rdf:about="&ri;MyRT">
                <rdfs:subClassOf rdf:resource="&lremap;ResourceType"/>
                </owl:Class>
                '''
        for rc in rtype_subclassed:
            line=self.__t1+"<owl:Class rdf:about=\"&ri;#"+rc+ "\">" 
            oFile.write((line + "\n").encode('utf-8'))
            line=self.__t2+"<rdfs:subClassOf rdf:resource=\"&lremap;ResourceType\"/>" 
            oFile.write((line + "\n").encode('utf-8')) 
            line=self.__t1+"</owl:Class>" 
            oFile.write((line + "\n").encode('utf-8'))      
        
        oFile=codecs.open(self.outfile,'a','utf-8')
        oFile.write((self.__ENDRESCLS__).encode('utf-8'))
        
        
        #resourcenames inds
        
        oFile.write((self.__STARTRESNAMES__).encode('utf-8'))
        
        for rname in names_serialized:
            line=self.__t1+"<owl:NamedIndividual rdf:about=\"&ri;#"+rname.decode(encoding='UTF-8',errors='strict')+ "\">" 
            #line=self.__t1+"<owl:NamedIndividual rdf:about=\"&lremap;#"+rname+ "\">" 
            #oFile.write((line + "\n").encode('utf-8'))
            oFile.write(line+"\n")
                       
            if rname!="-":
                line=self.__t2+"<rdf:type rdf:resource=\"&lremap;ResourceName\"/>" 
            else:
                line=self.__t2+"<rdf:type rdf:resource=\"&lremap;NoName\"/>"     
            oFile.write((line + "\n").encode('utf-8')) 
            line=self.__t1+"</owl:NamedIndividual>" 
            oFile.write((line + "\n\n").encode('utf-8')) 
        
        
        oFile.write((self.__ENDRESNAMES__).encode('utf-8'))
        
        
        
        oFile.write((self.__STARTRESAVAILS__).encode('utf-8'))
        
        for avail in avails_serialized:
            line=self.__t1+"<owl:NamedIndividual rdf:about=\"&ri;#"+avail+ "\">" 
            oFile.write((line + "\n").encode('utf-8'))
            line=self.__t2+"<rdf:type rdf:resource=\"&lremap;ResourceAvailability\"/>" 
              
            oFile.write((line + "\n").encode('utf-8')) 
            line=self.__t1+"</owl:NamedIndividual>" 
            oFile.write((line + "\n\n").encode('utf-8')) 
        
        
        oFile.write((self.__ENDRESAVAILS__).encode('utf-8'))
        
        oFile.write((self.__STARTRESSTATUS__).encode('utf-8'))
        
        for status in status_serialized:
            line=self.__t1+"<owl:NamedIndividual rdf:about=\"&ri;#"+status+ "\">" 
            oFile.write((line + "\n").encode('utf-8'))
            line=self.__t2+"<rdf:type rdf:resource=\"&lremap;ResourceStatus\"/>" 
              
            oFile.write((line + "\n").encode('utf-8')) 
            line=self.__t1+"</owl:NamedIndividual>" 
            oFile.write((line + "\n\n").encode('utf-8')) 
        
        oFile=codecs.open(self.outfile,'a','utf-8')
        oFile.write((self.__ENDRESSTATUS__).encode('utf-8'))
        
        
        oFile.write((self.__STARTRESMODS__).encode('utf-8'))
        
        for mod in mods_serialized:
            line=self.__t1+"<owl:NamedIndividual rdf:about=\"&ri;#"+mod+ "\">" 
            oFile.write((line + "\n").encode('utf-8'))
            line=self.__t2+"<rdf:type rdf:resource=\"&lremap;ResourceModality\"/>" 
              
            oFile.write((line + "\n").encode('utf-8')) 
            line=self.__t1+"</owl:NamedIndividual>" 
            oFile.write((line + "\n\n").encode('utf-8')) 
        
        
        oFile.write((self.__ENDRESMODS__).encode('utf-8'))
        
        oFile.write((self.__STARTRESUSES__).encode('utf-8'))
        
        for use in uses_serialized:
            line=self.__t1+"<owl:NamedIndividual rdf:about=\"&ri;#"+use+ "\">" 
            oFile.write((line + "\n").encode('utf-8'))
            line=self.__t2+"<rdf:type rdf:resource=\"&lremap;ResourceUse\"/>" 
              
            oFile.write((line + "\n").encode('utf-8')) 
            line=self.__t1+"</owl:NamedIndividual>" 
            oFile.write((line + "\n\n").encode('utf-8')) 
        
        oFile=codecs.open(self.outfile,'a','utf-8')
        oFile.write((self.__ENDRESUSES__).encode('utf-8'))
        
        #other stuff
        self.set_newrtype_num_of_instances(newrtype)
 
        
        oFile.write((self.__CLOSELINE__ + "\n").encode('utf-8'))
    #end
    
    def serializeResourcesIntoManyFile(self,verbose):
        name ="SerializeResource.serializeResourcesIntoManyFile"   
        rtype_subclassed =set()
        newrtype =collections.defaultdict(set)
        names_serialized =set()
        avails_serialized =set()
        status_serialized =set()
        mods_serialized =set()
        l1_serialized =set()
        uses_serialized =set()
        res_serialized =set()
        append_res=""
        
        ns="&lremap;"
        #print self.get_rid_2ris()
        if (verbose==1):
            print "\t\tExecuting "+name
        #idx file
        idxfile=self.outfile+self.__INDEXOFRES__
        copy2(self.headerfile, idxfile)
        iFile=codecs.open(idxfile,'a','utf-8')
        iFile.write((self.__STARTRES__+"\n").encode('utf-8'))    
        
        for p, rids in self.get_p_2ris().iteritems():
            for rid in rids:
                rtype_subclassed =set()
                newrtype =collections.defaultdict(set)
                names_serialized =set()
                avails_serialized =set()
                status_serialized =set()
                mods_serialized =set()
                l1_serialized =set()
                uses_serialized =set()
                res_serialized =set()
                    
                '''
                prepare the structure for new classes
                '''
                ris=self.get_rid_2ris().get(rid)
                if ris is not None:
                    for ri in ris:
                        #print rid + " "+ str(ri)
                        '''
                        create the description file
                
                        '''
                        rid1=shasum(rid)
                        first_order_folder = str(rid1[:1])
                        second_order_folder = str(rid1[0:3])
                        if not os.path.exists(self.outfile+"/" + self.__RES__+first_order_folder):
                            os.makedirs(self.outfile+"/" + self.__RES__+"/"+first_order_folder)
                        if not os.path.exists(self.outfile+"/" + self.__RES__+first_order_folder + "/" + second_order_folder):
                            os.makedirs(self.outfile+"/" + self.__RES__+first_order_folder + "/" + second_order_folder)
                
                        append_res=self.__RES__+first_order_folder + "/" + second_order_folder
                        #write description file 
                        iLine=self.__t1+"<rdf:Description rdf:about=\"&ri;"+"/"+append_res+"/"+str(rid1)+"\">"
                        iFile.write((iLine+"\n").encode('utf-8'))
                        label="Conference: "+ri.get_conf()+ " and "
                        label=label+"Year: "+ri.get_year()+" and "
                        label=label+"Passcode: "+ri.get_passcode()+" and "
                        label=label+"Type: "+ri.get_type()+" and "
                        label=label+"Name: "+ri.get_name().decode(encoding='UTF-8',errors='strict')+" "
                        iLine=self.__t2+"<rdfs:label>"+label+"</rdfs:label>"
                        #iFile.write((iLine+"\n").encode('utf-8')) 
                        iFile.write((iLine+"\n"))
                        iLine=self.__t1+"</rdf:Description>"
                        #iFile.write((iLine+"\n").encode('utf-8'))
                        iFile.write((iLine+"\n"))
                        
                        
                        # as usual
                        rtype=ri.get_type()
                        #print rid + " "+ str(rtype)
                        rtype=pruneName(rtype, "")
                        #rtype="Language_Resources/Technologies_Infrastructure"
                        rtype=modifyString(rtype,"/","-")
                        rtype=rtype.replace("&", "&amp;")
                        if not (rtype in self.__RTYPES__):
                            ns="&ri;#"
                            if not rtype in rtype_subclassed:
                                #print "SUB CLASS "+ rtype 
                                rtype_subclassed.add(rtype)
                                newrtype[rtype].add(1)
                                
                                
                            else:
                                
                                nrc=newrtype.get(rtype)
                                if nrc is not None:
                                    for num in nrc:
                                        #print num
                                        del newrtype[rtype]
                                        newrtype[rtype].add(num+1)
                                else:
                                    if (self.verbose==1):
                                        print "\t\t Warning resource type "+rtype+ " NOT YET ENCOUNTERED"        
                        else:
                            ns="&lremap;"  
                        
                        '''
                        create the resourcename
                            <owl:NamedIndividual rdf:about="&ri;myname">
                                <rdf:type rdf:resource="&lremap;ResourceName"/>
                            </owl:NamedIndividual>
                        '''  
                            
                        
                        dst=self.outfile+"/"+append_res+"/"+rid1
                        copy2(self.headerfile, dst)
                        oFile=codecs.open(dst,'a','utf-8')
                        line=self.__t1+"<owl:NamedIndividual rdf:about=\"&ri;"+append_res+"/"+str(rid1)+ "\">" 
                        oFile.write((line + "\n").encode('utf-8'))
                        line=self.__t2+"<rdf:type rdf:resource=\""+ns+rtype+"\"/>" 
                        oFile.write((line + "\n").encode('utf-8'))     
                        rname=ri.get_name()
                        #print rid + " "+ str(rtype)
                        rname=pruneName(rname, "")
                        rname=modifyString(rname,"^","-")
                        #rname="-"
                        rname=rname.replace("&", "&amp;")
                        if not (rname in names_serialized):
                            names_serialized.add(rname)
                        
                        #avail="Freely_Available_aaa"    
                        avail= ri.get_avail()
                        
                        if avail is not None:
                            
                            avail=pruneName(avail, "")
                            avail=modifyString(avail,"^","-")
                            avail=avail.replace("&", "&amp;")
                            if not (avail in self.__RAVAILS__):
                                avails_serialized.add(avail)
                                line=self.__t2+"<lremap:hasResourceAvailability rdf:resource=\"&ri;"+append_res+"/"+avail+ "\"/>" 
                            else:
                                line=self.__t2+"<lremap:hasResourceAvailability rdf:resource=\"&lremap;"+avail+ "\"/>"
                                    
                            oFile.write((line + "\n").encode('utf-8'))
                        
                        status= ri.get_prodstatus()
                        if (status is not None) and (status != "NoStatus"):
                            
                            status=pruneName(status, "")
                            status=modifyString(status,"^","-")
                            status=status.replace("&", "&amp;")
                            if not (status in self.__RSTATUS__):
                                status_serialized.add(status)
                                line=self.__t2+"<lremap:hasResourceStatus rdf:resource=\"&ri;"+append_res+"/"+status+ "\"/>"
                            else:
                                line=self.__t2+"<lremap:hasResourceStatus rdf:resource=\"&lremap;"+status+ "\"/>"
                                    
                            oFile.write((line + "\n").encode('utf-8'))
                            
                        
                        mod= ri.get_modality()
                        
                        if mod is not None:
                            
                            mod=pruneName(mod, "")
                            mod=modifyString(mod,"^","-")
                            mod=mod.replace("&", "&amp;")
                            if not (mod in self.__RMODS__):
                                mods_serialized.add(mod)
                                line=self.__t2+"<lremap:hasResourceModality rdf:resource=\"&ri;"+append_res+"/"+mod+ "\"/>" 
                            else:
                                line=self.__t2+"<lremap:hasResourceModality rdf:resource=\"&lremap;"+mod+ "\"/>"
                                    
                            oFile.write((line + "\n").encode('utf-8'))
                            
                        
                        use= ri.get_resourceusage()
                        
                        if use is not None:
                            
                            use=pruneName(use, "")
                            use=modifyString(use,"^","-")
                            use=use.replace("&", "&amp;")
                            if not (use in self.__RUSES__):
                                uses_serialized.add(use)
                                line=self.__t2+"<lremap:hasResourceUse rdf:resource=\"&ri;"+append_res+"/"+use+ "\"/>" 
                            else:
                                line=self.__t2+"<lremap:hasResourceUse rdf:resource=\"&lremap;"+use+ "\"/>"
                                    
                            oFile.write((line + "\n").encode('utf-8'))            
                        
                        '''
                        create the individual with all properties
                            <owl:NamedIndividual rdf:about="&ri;MyCorpus">
                                <rdf:type rdf:resource="&lremap;Corpus"/>
                                <lvont:language rdf:resource="&lexvo;id/iso639-3/ita"/>
                                <lremap:hasResourceLanguageType rdf:resource="&lremap;Bi"/>
                                <lremap:hasResourceAvailability rdf:resource="&lremap;Freely_Available"/>
                                <lremap:hasResourceName rdf:resource="&ri;myname"/>
                            </owl:NamedIndividual> 
                        '''  
                        
                        
                        #line=self.__t2+"<lremap:hasResourceName rdf:resource=\"&ri;"+append_res+"/"+rname+ "\"/>" 
                        line=self.__t2+"<lremap:hasResourceName rdf:resource=\"&lremap;"+rname.decode(encoding='UTF-8',errors='strict')+ "\"/>" 
                        #oFile.write((line + "\n").encode('utf-8'))
                        oFile.write(line+"\n")
                    
                        
                        
                            
                            
                        # referencing submissions
                        pids =self.get_p_2subs().get(p)
                        
                        if pids is not None:
                            for pid in pids:
                                line=self.__t2+"<dcterms:references rdf:resource=\"&sub;#"+str(pid)+"\"/>"
                                oFile.write((line + "\n").encode('utf-8')) 
                        #closing individual
                        line=self.__t1+"</owl:NamedIndividual>" 
                        oFile.write((line + "\n").encode('utf-8'))                    
                                        
                        oFile.write((self.__ENDRES__ + "\n").encode('utf-8'))
        
                        # create subclass
                       
                        oFile.write((self.__STARTRESCLS__).encode('utf-8'))    
                        '''
                        create  <owl:Class rdf:about="&ri;MyRT">
                        <rdfs:subClassOf rdf:resource="&lremap;ResourceType"/>
                        </owl:Class>
                        '''
                        for rc in rtype_subclassed:
                            line=self.__t1+"<owl:Class rdf:about=\"&ri;"+append_res+"/"+rc+ "\">" 
                            oFile.write((line + "\n").encode('utf-8'))
                            line=self.__t2+"<rdfs:subClassOf rdf:resource=\"&lremap;ResourceType\"/>" 
                            oFile.write((line + "\n").encode('utf-8')) 
                            line=self.__t1+"</owl:Class>" 
                            oFile.write((line + "\n").encode('utf-8'))      
        
                        
                        oFile.write((self.__ENDRESCLS__).encode('utf-8'))
        
        
                            #resourcenames inds
                        for rname in names_serialized:
                        
                            oFile.write((self.__STARTRESNAMES__).encode('utf-8'))
                        
                            #line=self.__t1+"<owl:NamedIndividual rdf:about=\"&ri;"+append_res+"/"+rname+ "\">" 
                            line=self.__t1+"<owl:NamedIndividual rdf:about=\"&lremap;"+append_res+"/"+rname.decode(encoding='UTF-8',errors='strict')+ "\">" 
                            #oFile.write((line + "\n").encode('utf-8'))
                            oFile.write(line+"\n")
                       
                            if rname!="-":
                                line=self.__t2+"<rdf:type rdf:resource=\"&lremap;ResourceName\"/>" 
                            else:
                                line=self.__t2+"<rdf:type rdf:resource=\"&lremap;NoName\"/>"     
                            oFile.write((line + "\n").encode('utf-8')) 
                            line=self.__t1+"</owl:NamedIndividual>" 
                            oFile.write((line + "\n").encode('utf-8')) 
        
        
                            oFile.write((self.__ENDRESNAMES__).encode('utf-8'))
        
        
        
        
        
                       
        
                        for avail in avails_serialized:
                            oFile.write((self.__STARTRESAVAILS__).encode('utf-8'))
                            line=self.__t1+"<owl:NamedIndividual rdf:about=\"&ri;"+append_res+"/"+avail+ "\">" 
                            oFile.write((line + "\n").encode('utf-8'))
                            line=self.__t2+"<rdf:type rdf:resource=\"&lremap;ResourceAvailability\"/>" 
              
                            oFile.write((line + "\n").encode('utf-8')) 
                            line=self.__t1+"</owl:NamedIndividual>" 
                            oFile.write((line + "\n").encode('utf-8')) 
                            oFile.write((self.__ENDRESAVAILS__).encode('utf-8'))
        
                        
                        for status in status_serialized:
                            oFile.write((self.__STARTRESSTATUS__).encode('utf-8'))
        
                        
                            line=self.__t1+"<owl:NamedIndividual rdf:about=\"&ri;"+append_res+"/"+status+ "\">" 
                            oFile.write((line + "\n").encode('utf-8'))
                            line=self.__t2+"<rdf:type rdf:resource=\"&lremap;ResourceStatus\"/>" 
              
                            oFile.write((line + "\n").encode('utf-8')) 
                            line=self.__t1+"</owl:NamedIndividual>" 
                            oFile.write((line + "\n\n").encode('utf-8')) 
        
                    
                            oFile.write((self.__ENDRESSTATUS__).encode('utf-8'))
        
                        for mod in mods_serialized:
                            oFile.write((self.__STARTRESMODS__).encode('utf-8'))
        
                            line=self.__t1+"<owl:NamedIndividual rdf:about=\"&ri;"+append_res+"/"+mod+ "\">" 
                            oFile.write((line + "\n").encode('utf-8'))
                            line=self.__t2+"<rdf:type rdf:resource=\"&lremap;ResourceModality\"/>" 
              
                            oFile.write((line + "\n").encode('utf-8')) 
                            line=self.__t1+"</owl:NamedIndividual>" 
                            oFile.write((line + "\n\n").encode('utf-8')) 
        
        
                            oFile.write((self.__ENDRESMODS__).encode('utf-8'))
        
                        for use in uses_serialized:
                            oFile.write((self.__STARTRESUSES__).encode('utf-8'))
        
                        
                            line=self.__t1+"<owl:NamedIndividual rdf:about=\"&ri;"+append_res+"/"+use+ "\">" 
                            oFile.write((line + "\n").encode('utf-8'))
                            line=self.__t2+"<rdf:type rdf:resource=\"&lremap;ResourceUse\"/>" 
              
                            oFile.write((line + "\n").encode('utf-8')) 
                            line=self.__t1+"</owl:NamedIndividual>" 
                            oFile.write((line + "\n\n").encode('utf-8')) 
        
        
                            oFile.write((self.__ENDRESUSES__).encode('utf-8'))
                        
                        oFile.write((self.__CLOSELINE__ + "\n").encode('utf-8'))    
#             iFile.write((self.__ENDRESCLS__).encode('utf-8'))     
        iFile.write((self.__CLOSELINE__).encode('utf-8'))              
        
        #other stuff
        self.set_newrtype_num_of_instances(newrtype)
 
            
        
    #end   
               
    def get_p_2ris(self):
        return self.__p2ris


    def get_p_2subs(self):
        return self.__p2subs


    def get_rid_2ris(self):
        return self.__rid2ris


    def set_p_2ris(self, value):
        self.__p2ris = value


    def set_p_2subs(self, value):
        self.__p2subs = value


    def set_rid_2ris(self, value):
        self.__rid2ris = value


    def del_p_2ris(self):
        del self.__p2ris


    def del_p_2subs(self):
        del self.__p2subs


    def del_rid_2ris(self):
        del self.__rid2ris

    p2ris = property(get_p_2ris, set_p_2ris, del_p_2ris, "p2ris's docstring")
    p2subs = property(get_p_2subs, set_p_2subs, del_p_2subs, "p2subs's docstring")
    rid2ris = property(get_rid_2ris, set_rid_2ris, del_rid_2ris, "rid2ris's docstring")

    def get_newrtype_num_of_instances(self):
        return self.__newrtypeNumOfInstances


    def set_newrtype_num_of_instances(self, value):
        self.__newrtypeNumOfInstances = value


    def del_newrtype_num_of_instances(self):
        del self.__newrtypeNumOfInstances

    newrtypeNumOfInstances = property(get_newrtype_num_of_instances, set_newrtype_num_of_instances, del_newrtype_num_of_instances, "newrtypeNumOfInstances's docstring")
