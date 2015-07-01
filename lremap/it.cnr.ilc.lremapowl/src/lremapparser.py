#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Apr 30, 2014

@author: riccardo
'''


from lremapdbapi import yearsapi, authorsapi, papersapi, confapi, subapi, \
    resourceapi
from lremapobj.author import Author
from lremapobj.conference import Conference
from lremapobj.paper import Paper
from lremapobj.resource import Resource
from lremapobj.submission import Submission
from lremapobj.year import Year
from mapdao import lremapdao
import collections








class LreMapParser:
    '''
    classdocs
    '''
    
    # db parameters
    user="mystart"
    passwd="mystart"
    db="START_DB"
    host="localhost"
    
    __SEP__="\t"
    __WSEP__=";"
    __OUTDIR__="./lremap/owl"
    
    __YEAR__="y" # list of years
    __CONF__="c" # list of conferences
    __SUB__="s" # list of submissions
    __SUBANDPAPERANDCONF__="s+" # list of submissions
    __AUTH__="a" # list of authors
    __PAPER__="p" # list of papers
    __PAPERANDAUTH__="ap" # list of papers and connected authors
    __RES__="r" # list of resources
    __RESNORM__="rn" # list of normalized resources
    __RESTEMP__="rt" # list of template resources
    
    __ALL__="all" # root to sense
    __NOTFOUND__="Not Found"
    __MAINNCONTACT__="Main Contact"
    
    #header files
    __AUTHSINGLEHEADERFILE__ ="./in/auth.single.header.xml" #0
    __AUTHMULTIPLEHEADERFILE__ ="./in/auth.multiple.header.xml" #1
    __PAPERSINGLEHEADERFILE__ ="./in/paper.single.header.xml" #2
    __PAPERMULTIPLEHEADERFILE__ ="./in/paper.multiple.header.xml" #3
    __YEARSINGLEHEADERFILE__ ="./in/year.single.header.xml" #4
    __YEARMULTIPLEHEADERFILE__ ="./in/year.single.header.xml" #5
    __CONFSINGLEHEADERFILE__ ="./in/conf.single.header.xml" #6
    __CONFMULTIPLEHEADERFILE__ ="./in/conf.single.header.xml" #7
    __SUBSINGLEHEADERFILE__ ="./in/sub.single.header.xml" #8
    __SUBMULTIPLEHEADERFILE__ ="./in/sub.multiple.header.xml" #9
    __RESISINGLEHEADERFILE__ ="./in/res.single.header.xml" #10
    __RESIMULTIPLEHEADERFILE__ ="./in/res.multiple.header.xml" #11
    
    __listOfHeaderFiles=[
                         __AUTHSINGLEHEADERFILE__,__AUTHMULTIPLEHEADERFILE__,
                         __PAPERSINGLEHEADERFILE__,__PAPERMULTIPLEHEADERFILE__,
                         __YEARSINGLEHEADERFILE__,__YEARMULTIPLEHEADERFILE__,
                         __CONFSINGLEHEADERFILE__,__CONFMULTIPLEHEADERFILE__,
                         __SUBSINGLEHEADERFILE__,__SUBMULTIPLEHEADERFILE__,
                         __RESISINGLEHEADERFILE__,__RESIMULTIPLEHEADERFILE__
                         
                         ]
    
    __AUTHSINGLEOUTPUTFILE__ =__OUTDIR__+"/lremap_auth" #0
    __AUTHMULTIPLEOUTPUTFILE__ =__OUTDIR__+"/instances/" #1
    
    __PAPERSINGLEOUTPUTFILE__ =__OUTDIR__+"/lremap_paper" #2
    __PAPERMULTIPLEOUTPUTFILE__ =__OUTDIR__+"/instances/" #3
    
    __YEARSINGLEOUTPUTFILE__ =__OUTDIR__+"/lremap_year" #4
    __YEARMULTIPLEOUTPUTFILE__ =__OUTDIR__+"/lremap_year" #5
    
    __CONFSINGLEOUTPUTFILE__ =__OUTDIR__+"/lremap_conf" #6
    __CONFMULTIPLEOUTPUTFILE__ =__OUTDIR__+"/lremap_conf" #7
    
    __SUBSINGLEOUTPUTFILE__ =__OUTDIR__+"/lremap_sub" #8
    __SUBMULTIPLEOUTPUTFILE__ =__OUTDIR__+"/instances/" #9
    
    __RESISINGLEOUTPUTFILE__ =__OUTDIR__+"/lremap_ri" #10
    __RESIMULTIPLEOUTPUTFILE__ =__OUTDIR__+"/instances/" #11
    
    __listOfOutputFiles=[
                         __AUTHSINGLEOUTPUTFILE__,__AUTHMULTIPLEOUTPUTFILE__,
                         __PAPERSINGLEOUTPUTFILE__,__PAPERMULTIPLEOUTPUTFILE__,
                         __YEARSINGLEOUTPUTFILE__,__YEARMULTIPLEOUTPUTFILE__,
                         __CONFSINGLEOUTPUTFILE__,__CONFMULTIPLEOUTPUTFILE__,
                         __SUBSINGLEOUTPUTFILE__,__SUBMULTIPLEOUTPUTFILE__,
                         __RESISINGLEOUTPUTFILE__,__RESIMULTIPLEOUTPUTFILE__
                         
                         ]
    
    __authFile=""
    __paperFile=""
    
    #metadata in db 
    
    #ResourceType in DB and in resource schema
   
    __RT_ANT="Annotation_Tool"
    __RT_CORPUS="Corpus"
    __RT_CT="Corpus_Tool"
    __RT_EVLD="Evaluation_Data"
    __RT_EVLMFG="Evaluation_Methodology-Formalism-Guidelines"
    __RT_EVLPKG="Evaluation_Package"
    __RT_EVLSBP="Evaluation_Standard-Best_Practice"
    __RT_EVLT="Evaluation_Tool"
    __RT_GLM="Grammar-Language_Model"
    __RT_IMGA="Image_Analyser"
    __RT_LANI="Language_Identifier"
    __RT_LANMT="Language_Modeling_Tool"
    __RT_LRTINF="Language_Resources-Technologies_Infrastructure"
    __RT_LEX="Lexicon"
    __RT_MTT="Machine_Translation_Tool"
    __RT_MD="Metadata"
    __RT_NOTYPE="NoType"
    __RT_ONTO="Ontology"
    __RT_PA="Prosodic_Analyser"
    __RT_REPANFG="Representation-Annotation_Formalism-Guidelines"
    __RT_REPANSBP="Representation-Annotation_Standard-Best_Practice"
    __RT_NER="Named_Entity_Recognizer"
    __RT_SIGPFEXT="Signal_Processing-Feature_Extraction"
    __RT_SPKR="Speaker_recogniser"
    __RT_SPRT="Speech_Recognizer-Transcriber"
    __RT_SPKNDT="Spoken_Dialogue_Tool"
    __RT_T2SPSYN="Text-to-Speech_Synthesizer"
    __RT_TP="Tagger-Parser"
    __RT_TER="Terminology"
    __RT_TOK="Tokenizer"
    __RT_TRANS="Transcriber"
    __RT_WSD="Word_Sense_Disambiguator"
    __resourcetypesInMapDb=[
                            __RT_ANT,__RT_CORPUS,__RT_CT,__RT_EVLD,
                            __RT_EVLMFG,__RT_EVLPKG,__RT_EVLSBP,__RT_EVLT,
                            __RT_GLM, __RT_IMGA, __RT_LANI, __RT_LANMT, __RT_LRTINF,
                            __RT_LEX, __RT_MTT, __RT_MD,__RT_NOTYPE,__RT_ONTO, __RT_PA, 
                            __RT_REPANFG,__RT_REPANSBP,__RT_NER, __RT_SIGPFEXT,__RT_SPKR,__RT_SPRT,
                            __RT_SPKNDT, __RT_T2SPSYN, __RT_TP,__RT_TER,__RT_TOK,
                            __RT_TRANS, __RT_WSD          
                            ]
    
    __COMMON__NA__="Not_Applicable"
    __COMMON__NR__="Not_Relevant"
    __commonvaluesInMapDb=[__COMMON__NA__,__COMMON__NR__]
    
    __AVAIL_FA__="Freely_Available"
    __AVAIL_FDC__="From_Data_Center(s)"
    __AVAIL_FO__="From_Owner"
    __AVAIL_NA__="Not_Available"
    __availabilitiesInMapDb=[__AVAIL_FA__,__AVAIL_FDC__,__AVAIL_FO__,__AVAIL_NA__]
    
    
    __STATUS__EUPD__="Existing-updated"
    __STATUS_USED__="Existing-used" 
    __STATUS__NCF__="Newly_created-finished"
    __STATUS_NCIP__="Newly_created-in_progress"   
    __statusInMapDb=[__STATUS__EUPD__,__STATUS_USED__,__STATUS__NCF__,__STATUS_NCIP__]
    
    
    __MOD_MI__="Modality_Independent"
    __MOD_MM__="Multimodal/Multimedia"
    __MOD__SL__="Sign_Language"
    __MOD_SP__="Speech"
    __MOD_SW__="Speech-Written"
    __MOD_W__="Written"
    __modalitiesInMapDb=[__MOD_MI__,__MOD_MM__,__MOD__SL__,__MOD_SP__,__MOD_SW__,__MOD_W__]
    
    __LANTGYPE__BI__="Bi"
    __LANGTYPE_LI__="LI"
    __LANGTYPE_MO__="Mono"
    __LANGTYPE_MU__="Multi"
    __LANGTYPE_TRI__="Tri"
    __langtypesInMapDb=[__LANGTYPE_MO__,__LANTGYPE__BI__,__LANGTYPE_TRI__,__LANGTYPE_MU__,__LANGTYPE_LI__]
    
    __USE_ACQ__="Acquisition"
    __USE_DIA__="Dialogue"
    __USE_DIS__="Discourse"
    __USE_DCTC__="Document_Classification-Text_categorisation"
    __USE_ERG__="Emotion_Recognition-Generation"
    __USE_IEIR__="Information_Extraction-Information_Retrieval"
    __USE_KDR__="Knowledge_Discovery-Representation"
    __USE_LI__="Language_Identification"
    __USE_LM__="Language_Modelling"
    __USE_MTST__="Machine_Translation-SpeechToSpeech_Translation"
    __USE_MDP__="Multimedia_Document_Processing"
    __USE_NER__="Named_Entity_Recognition"
    __USE_NLG__="Natural_Language_Generation"
    __USE_PI__="Person_Identification"
    __USE_QA__="Question_Answering"
    __USE_SW__="Semantic_Web"
    __USE_SLRG__="Sign_Language_Recognition-Generation"
    __USE_SPU__="Speech_Recognition-Understanding"
    __USE_SS__="Speech_Synthesis"
    __USE_SUM__="Summarisation"
    __USE_TM__="Text_Mining"
    __USE_TE__="Textual_Entailment"
    __USE_TDT__="Topic_Detection_and_Tracking"
    __USE_VC__="Voice_Control"
    __USE_WS__="Web_Services"
    __USE_WSD__="Word_Sense_Disambiguation"
    __usesInMapDb=[
                   __USE_ACQ__,__USE_DIA__,__USE_DIS__,__USE_DCTC__,__USE_ERG__,
                   __USE_IEIR__,__USE_KDR__,__USE_LI__,__USE_LM__,__USE_MTST__,
                   __USE_MDP__,__USE_NER__,__USE_NLG__,__USE_PI__,__USE_QA__,
                   __USE_SW__,__USE_SLRG__,__USE_SPU__,__USE_SS__,__USE_SUM__,
                   __USE_TM__,__USE_TE__,__USE_TDT__,__USE_VC__,__USE_WS__,__USE_WSD__
                   ]
    
    
    __STATUS_ACCP__="accepted"
    __STATUS_DRAFT__="draft"
    __STATUS_FC__="forthcoming"
    __STATUS_LEGAL__="legal"
    __STATUS_NPR__="non_peer_reviewed"
    __STATUS_PR__="peer_reviewed"
    __STATUS_PUB__="published"
    __STATUS_REJ__="rejected"
    __STATUS_UPUB__="unpublished"
    __STATUS_TEST="accept_poster+demosuggested"
    __statusInBibo=[ __STATUS_ACCP__,__STATUS_DRAFT__,__STATUS_FC__,
                    __STATUS_LEGAL__,__STATUS_NPR__,__STATUS_PR__,
                    __STATUS_PUB__,__STATUS_REJ__,__STATUS_UPUB__, __STATUS_TEST
                    ]
    
    
    #dictionaries
    __passcode2Authors = collections.defaultdict(list)
    __passcode2Papers = collections.defaultdict(list)
    __passcode2Years = collections.defaultdict(list)
    __passcode2Confs = collections.defaultdict(list)
    __passcode2Subs = collections.defaultdict(list)
    __passcode2Resources = collections.defaultdict(list)
    


    def __init__(self,dowhat,writefile,verbose):
        self.verbose=verbose
        self.dowhat=dowhat
        self.writefile=writefile
        '''
        Constructor
        '''
        global connection
        
        dao=lremapdao.LreMapDAO(self.user, self.passwd, self.db, self.host,verbose)
        connection=dao.connect()
       
    
    
    
    
    def switchHeaderFile(self,idx):
        return self.__listOfHeaderFiles[idx]
    
    def switchOutputFile(self,idx):
        return self.__listOfOutputFiles[idx] 
    
    
    '''
    Fetch all resource instances
    '''
    def fetchResource(self,isobjres,connection):
        name="fetchResource"
        resdao=resourceapi.LreMapResourceAPI(connection,isobjres,self.verbose)    
        if (self.verbose==1):
            print ("\t\tExecuting "+name+"\n").encode('utf-8')
        objs=resdao.fetchData() 
        return objs  
    
    '''
    init authors
    valid data start from i=0
    i=0 conf,
    i=1 year,
    i=2 passcode,
    i=3 resourceid,
    i=4 type,
    i=5 name,
    i=6 size,
    i=7 unit,
    i=8 prodstatus,
    i=9 langsel,
    i=10 langdimension,
    i=11 lang1,
    i=12 lang2,
    i=13 lang3,
    i=14 lang4,
    i=15 lang5,
    i=16 langother,
    i=17 modality,
    i=18 resourceusage,
    i=19 avail ,
    i=20 license,
    i=21 url,
    i=22 doc,
    i=23 description,
    i=24 shared,
    i=25 pf ,
    i=26 uurl
    
    -- NOT USED i=3 resourceid, i=9 langsel, i=24 shared, i=25 pf , i=26 uurl  
    '''
    def initResources(self,isobjres,results):
        name="initResources"  
        if (self.verbose==1):
            print ("\t\tExecuting "+name+"\n").encode('utf-8')
        temp = collections.defaultdict(set)
        if results is not None:
            i=0
            for row in results:
                conf = results[i][0]
                year = results[i][1]
                passcode = results[i][2]
                rtype = results[i][4]
                name = results[i][5]
                size = results[i][6]
                unit = results[i][7]
                prodstatus = results[i][8]

                langtype = results[i][10]
                lang1 = results[i][11]
                lang2 = results[i][12]
                lang3 = results[i][13]
                lang4 = results[i][14]
                lang5 = results[i][15]
                langother = results[i][16]
                modality = results[i][17]
                resourceusage = results[i][18]
                avail  = results[i][19]
                rlicense = results[i][20]
                url = results[i][21]
                doc = results[i][22]
                description = results[i][23]
                
                
                # init author authornumber, username, firstname, lastname, email, institute, country
                #manage nonetype
                if rtype is None:
                    rtype="NoType"
                if name is None:
                    name="NoName"
                if prodstatus is None:
                    prodstatus="NoStatus"
                                
                obj=Resource(conf, year, passcode, isobjres, rtype, name, size, unit, prodstatus, langtype,lang1, lang2, lang3, lang4, lang5, langother, modality, resourceusage, avail , rlicense, url, doc, description)
                temp[passcode].add(obj)
#                 if authn != self.__MAINNCONTACT__:
#                     temp[passcode].add(auth)
                i=i+1
            self.set_passcode_2_resources(temp)       
    
    '''
    Fetch all authors
    '''
    def fetchAuthors(self,connection):
        name="fetchAuthors"
        authdao=authorsapi.LreMapAuthAPI(connection,self.verbose)    
        if (self.verbose==1):
            print ("\t\tExecuting "+name+"\n").encode('utf-8')
        auths=authdao.fetchData() 
        return auths 
        #print (len(auths))  
    
    '''
    init authors
    valid data start from i=2
    i=0 conf
    i=1 year
    i=2 passcode
    i=3 auth number
    i=4 username
    i=5 firstname
    i=6 lastname
    i=7 email
    i=8 affiliation
    i=9 country
    
    8 and 9 define affiliation 
    '''
    def initAuthors(self,results):
        name="initAuthors"  
        if (self.verbose==1):
            print ("\t\tExecuting "+name+"\n").encode('utf-8')
        temp = collections.defaultdict(set)
        if results is not None:
            i=0
            for row in results:
                passcode=results[i][2]
                authn=results[i][3]
                username=results[i][4]
                firstname=results[i][5]
                lastname=results[i][6]
                email=results[i][7]
                institute=results[i][8]
                country=results[i][9]
                # init author authornumber, username, firstname, lastname, email, institute, country
                #manage nonetype
                if username is None:
                    username=""
                if firstname is None:
                    firstname=""
                if lastname is None:
                    lastname=""
                if institute is None:
                    institute=""
                if country is None:
                    country=""                
                auth=Author(authn,username,firstname,lastname,email,institute,country)
                temp[passcode].add(auth)
#                 if authn != self.__MAINNCONTACT__:
#                     temp[passcode].add(auth)
                i=i+1
            self.set_passcode_2_authors(temp) 
             
       
        
    
    
    '''
    Fetch all years
    '''
    def fetchYears(self,connection):
        name="fetchYears"
        paperdao=yearsapi.LreMapYearAPI(connection,self.verbose)    
        if (self.verbose==1):
            print ("\t\tExecuting "+name+"\n").encode('utf-8')
        papers=paperdao.fetchData() 
        return papers 
        #print (len(auths))  
    
    '''
    init years
    valid data start from i=2
    i=0 conf
    i=1 year
    i=2 passcode
    .....
    
    8 and 9 define affiliation 
    '''
    def initYears(self,results):
        name="initYears"  
        if (self.verbose==1):
            print ("\t\tExecuting "+name+"\n").encode('utf-8')
        temp = collections.defaultdict(set)
        if results is not None:
            i=0
            for row in results:
                year=results[i][1]
                passcode=results[i][2]
                
                       
                year=Year(year)
                temp[passcode].add(year)
#                 if authn != self.__MAINNCONTACT__:
#                     temp[passcode].add(auth)
                i=i+1
            self.set_passcode_2_years(temp)        
    
    
    '''
    Fetch all confs
    '''
    def fetchConferences(self,connection):
        name="fetchConferences"
        confdao=confapi.LreMapConfAPI(connection,self.verbose)    
        if (self.verbose==1):
            print ("\t\tExecuting "+name+"\n").encode('utf-8')
        confs=confdao.fetchData() 
        return confs 
        #print (len(auths)) 
        
         
    
    '''
    init conf
    valid data start from i=2
    i=0 conf
    i=1 year
    i=2 paperid
    i=3 passcode
    i=4 type
    i=5 subevent
    i=6 location
    .....
    
    8 and 9 define affiliation 
    '''
    def initConferences(self,results):
        name="initConferences"  
        if (self.verbose==1):
            print ("\t\tExecuting "+name+"\n").encode('utf-8')
        temp = collections.defaultdict(set)
        if results is not None:
            i=0
            for row in results:
                conf=results[i][0]
                year=results[i][1]
                pid=results[i][2]
                passcode=results[i][3]
                ty=results[i][4]
                se=results[i][5]
                location=results[i][6]
                
                       
                obj=Conference(conf,year,ty,se,location)
                temp[passcode].add(obj)
#                 if authn != self.__MAINNCONTACT__:
#                     temp[passcode].add(auth)
                i=i+1
            self.set_passcode_2_confs(temp)        
    
    
    '''
    Fetch all subs
    '''
    def fetchSubmissions(self,connection):
        name="fetchSubmissions"
        subdao=subapi.LreMapSubAPI(connection,self.verbose)    
        if (self.verbose==1):
            print ("\t\tExecuting "+name+"\n").encode('utf-8')
        subs=subdao.fetchData() 
        return subs 
        #print (len(auths)) 
        
    
    '''
    init sub
    valid data start from i=2
    i=0 conf
    i=1 year
    i=2 paperid
    i=3 passcode
    i=4 type
    i=5 subevent
    i=6 location
    .....
    
    8 and 9 define affiliation 
    '''
    def initSubmissions(self,results):
        name="initSubmissions"  
        if (self.verbose==1):
            print ("\t\tExecuting "+name+"\n").encode('utf-8')
        temp = collections.defaultdict(set)
        if results is not None:
            i=0
            for row in results:
                conf=results[i][0]
                year=results[i][1]
                pid=results[i][2]
                passcode=results[i][3]
                ty=results[i][4]
                se=results[i][5]
                
                       
                obj=Submission(passcode,conf,year,ty,se,pid)
                temp[passcode].add(obj)
#                 if authn != self.__MAINNCONTACT__:
#                     temp[passcode].add(auth)
                i=i+1
            self.set_passcode_2_subs(temp)       
    
    '''
    Fetch all papers
    '''
    def fetchPapers(self,connection):
        name="fetchPapers"
        paperdao=papersapi.LreMapPaperAPI(connection,self.verbose)    
        if (self.verbose==1):
            print ("\t\tExecuting "+name+"\n").encode('utf-8')
        papers=paperdao.fetchData() 
        return papers 
        #print (len(auths))
    
    
    
    '''
    init paper
    valid data start from i=2
    i=0 conf
    i=1 year
    i=2 passcode
    i=3 paper id
    i=4 status
    i=5 title
    i=6 category1
    i=7 category2
    i=8 keywords
    '''
    def initPapers(self,results):
        name="initPapers"  
        if (self.verbose==1):
            print ("\t\tExecuting "+name+"\n").encode('utf-8')
        temp = collections.defaultdict(set)
        if results is not None:
            i=0
            for row in results:
                conf=results[i][0]
                year=results[i][1]
                passcode=results[i][2]
                pid=results[i][3]
                status=results[i][4]
                title=results[i][5]
                category1=results[i][6]
                category2=results[i][7]
                keywords=results[i][8]
                
                if status is None:
                    status=""
                if title is None:
                    title=""
                if category1 is None:
                    category1=""
                if category2 is None:
                    category2=""
                if keywords is None:
                    keywords=""                
                paper=Paper(conf,year,pid,status,title,category1,category2,keywords)
                
                temp[passcode].add(paper)
                i=i+1
            self.set_passcode_2_papers(temp) 
#             print "XXXX "+str(len(self.get_passcode_2_papers()))       
    
    '''
    This method switches among different types of output to
    create the structures to be serialized
    '''
    def readFromDbAndCreateSetsAccordingToDoWhat(self, outfile):
        name="readFromDbAndCreateSetsAccordingToDoWhat"
        act=self.dowhat
        
        if (self.verbose==1):
            print ("\t\tExecuting "+name+"\n").encode('utf-8')
        
        if (act==self.__YEAR__):
            if (self.verbose==1):
                print ("\t\tExecuting Extraction of YEARS From "+self.db+ "\n").encode('utf-8')
        
        
        if (act==self.__AUTH__):
            if (self.verbose==1):
                print ("\t\tExecuting Extraction of AUTHORS From "+self.db+ "\n").encode('utf-8') 
            auths=self.fetchAuthors(connection)  
            self.initAuthors(auths)
        
        if (act==self.__PAPER__):
            if (self.verbose==1):
                print ("\t\tExecuting Extraction of PAPERS From "+self.db+ "\n").encode('utf-8') 
            papers=self.fetchPapers(connection)  
            self.initPapers(papers)
        
        if (act==self.__PAPERANDAUTH__):
            if (self.verbose==1):
                print ("\t\tExecuting Extraction of AUTHORS and PAPERS From "+self.db+ "\n").encode('utf-8')
            
            auths=self.fetchAuthors(connection)  
            self.initAuthors(auths)    
            papers=self.fetchPapers(connection)  
            self.initPapers(papers)
        if (act==self.__YEAR__):
            if (self.verbose==1):
                print ("\t\tExecuting Extraction of YEARS From "+self.db+ "\n").encode('utf-8')
            years=self.fetchYears(connection)
            self.initYears(years)
        
        if (act==self.__CONF__):
            if (self.verbose==1):
                print ("\t\tExecuting Extraction of CoNF From "+self.db+ "\n").encode('utf-8')
            objs=self.fetchConferences(connection)
            self.initConferences(objs)
            
        if (act==self.__SUB__):
            if (self.verbose==1):
                print ("\t\tExecuting Extraction of Submission From "+self.db+ "\n").encode('utf-8')
            objs=self.fetchSubmissions(connection)
            self.initSubmissions(objs)
        
        if (act==self.__SUBANDPAPERANDCONF__):
            if (self.verbose==1):
                print ("\t\tExecuting Extraction of SUBS PAPERS AND CONF From "+self.db+ "\n").encode('utf-8')
             
            papers=self.fetchPapers(connection)  
            self.initPapers(papers)
            objs=self.fetchConferences(connection)
            self.initConferences(objs)
            objs=self.fetchSubmissions(connection)
            self.initSubmissions(objs)  
        if (act==self.__RES__):
            if (self.verbose==1):
                print ("\t\tExecuting Extraction of Resource Instances From "+self.db+ "\n").encode('utf-8')
                objs=self.fetchSubmissions(connection)
            self.initSubmissions(objs) 
            objs=self.fetchResource("ri", connection)
            self.initResources("ri", objs)        
            
            
    
    
    
    
    
    def get_passcode_2_authors(self):
        return self.__passcode2Authors


    def set_passcode_2_authors(self, value):
        self.__passcode2Authors = value


    def del_passcode_2_authors(self):
        del self.__passcode2Authors

    passcode2Authors = property(get_passcode_2_authors, set_passcode_2_authors, del_passcode_2_authors, "passcode2Authors's docstring")

    def get_passcode_2_papers(self):
        return self.__passcode2Papers


    def set_passcode_2_papers(self, value):
        self.__passcode2Papers = value


    def del_passcode_2_papers(self):
        del self.__passcode2Papers

    passcode2Papers = property(get_passcode_2_papers, set_passcode_2_papers, del_passcode_2_papers, "passcode2Papers's docstring")

    def get_passcode_2_years(self):
        return self.__passcode2Years


    def set_passcode_2_years(self, value):
        self.__passcode2Years = value


    def del_passcode_2_years(self):
        del self.__passcode2Years

    passcode2Years = property(get_passcode_2_years, set_passcode_2_years, del_passcode_2_years, "passcode2Years's docstring")

    def get_passcode_2_confs(self):
        return self.__passcode2Confs


    def set_passcode_2_confs(self, value):
        self.__passcode2Confs = value


    def del_passcode_2_confs(self):
        del self.__passcode2Confs

    passcode2Confs = property(get_passcode_2_confs, set_passcode_2_confs, del_passcode_2_confs, "passcode2Confs's docstring")

    def get_status_in_bibo(self):
        return self.__statusInBibo


    def set_status_in_bibo(self, value):
        self.__statusInBibo = value


    def del_status_in_bibo(self):
        del self.__statusInBibo

    statusInBibo = property(get_status_in_bibo, set_status_in_bibo, del_status_in_bibo, "statusInBibo's docstring")

    def get_passcode_2_subs(self):
        return self.__passcode2Subs


    def set_passcode_2_subs(self, value):
        self.__passcode2Subs = value


    def del_passcode_2_subs(self):
        del self.__passcode2Subs

    passcode2Subs = property(get_passcode_2_subs, set_passcode_2_subs, del_passcode_2_subs, "passcode2Subs's docstring")

    def get_passcode_2_resources(self):
        return self.__passcode2Resources


    def set_passcode_2_resources(self, value):
        self.__passcode2Resources = value


    def del_passcode_2_resources(self):
        del self.__passcode2Resources

    passcode2Resources = property(get_passcode_2_resources, set_passcode_2_resources, del_passcode_2_resources, "passcode2Resources's docstring")

    def get_resourcetypes_in_map_db(self):
        return self.__resourcetypesInMapDb


    def set_resourcetypes_in_map_db(self, value):
        self.__resourcetypesInMapDb = value


    def del_resourcetypes_in_map_db(self):
        del self.__resourcetypesInMapDb

    resourcetypesInMapDb = property(get_resourcetypes_in_map_db, set_resourcetypes_in_map_db, del_resourcetypes_in_map_db, "resourcetypesInMapDb's docstring")

    def get_availabilities_in_map_db(self):
        return self.__availabilitiesInMapDb


    def get_status_in_map_db(self):
        return self.__statusInMapDb


    def get_modalities_in_map_db(self):
        return self.__modalitiesInMapDb


    def get_langtypes_in_map_db(self):
        return self.__langtypesInMapDb


    def get_uses_in_map_db(self):
        return self.__usesInMapDb


    def set_availabilities_in_map_db(self, value):
        self.__availabilitiesInMapDb = value


    def set_status_in_map_db(self, value):
        self.__statusInMapDb = value


    def set_modalities_in_map_db(self, value):
        self.__modalitiesInMapDb = value


    def set_langtypes_in_map_db(self, value):
        self.__langtypesInMapDb = value


    def set_uses_in_map_db(self, value):
        self.__usesInMapDb = value


    def del_availabilities_in_map_db(self):
        del self.__availabilitiesInMapDb


    def del_status_in_map_db(self):
        del self.__statusInMapDb


    def del_modalities_in_map_db(self):
        del self.__modalitiesInMapDb


    def del_langtypes_in_map_db(self):
        del self.__langtypesInMapDb


    def del_uses_in_map_db(self):
        del self.__usesInMapDb

    availabilitiesInMapDb = property(get_availabilities_in_map_db, set_availabilities_in_map_db, del_availabilities_in_map_db, "availabilitiesInMapDb's docstring")
    statusInMapDb = property(get_status_in_map_db, set_status_in_map_db, del_status_in_map_db, "statusInMapDb's docstring")
    modalitiesInMapDb = property(get_modalities_in_map_db, set_modalities_in_map_db, del_modalities_in_map_db, "modalitiesInMapDb's docstring")
    langtypesInMapDb = property(get_langtypes_in_map_db, set_langtypes_in_map_db, del_langtypes_in_map_db, "langtypesInMapDb's docstring")
    usesInMapDb = property(get_uses_in_map_db, set_uses_in_map_db, del_uses_in_map_db, "usesInMapDb's docstring")
