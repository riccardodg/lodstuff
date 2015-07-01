#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Apr 30, 2014
Exec this module to play with the map
@author: riccardo
'''



from serializer.authorserializer import SerializeAuthor
from serializer.conferenceserializer import SerializeConference
from serializer.paperserializer import SerializePaper
from serializer.resourceserializer import SerializeResource
from serializer.submissionserializer import SerializeSubmission
from serializer.yearserializer import SerializeYear
import datetime
import lremapparser
import sys


''' 
outfile is the output file which contains statistics
dowhat is the operation
writefile identifies the output files for the map
lDebug if true is verbose
sDebug if true print statistics
pDebug if true add execution comments
'''
def lremap(outfile, dowhat, lDebug,sDebug,pDebug, writefile):
    
    if lDebug==1:
        outfile.write(("Params \n").encode('utf-8'))
        outfile.write(("\t To do list: "+str(dowhat)+ "\n").encode('utf-8'))
        outfile.write(("\t Verbose: "+str(lDebug)+"\n").encode('utf-8'))
        outfile.write(("\t Debug Statistics?: "+str(sDebug)+"\n").encode('utf-8'))
        outfile.write(("\t Debug Parser?: "+str(pDebug)+"\n").encode('utf-8'))
        outfile.write(("\t Write Files?: "+str(writefile)+"\n").encode('utf-8'))
        outfile.write(("\t\n").encode('utf-8'))
        outfile.write(("\t\n").encode('utf-8'))
    
    # create an instance of the lremap parser 
    handler=lremapparser.LreMapParser(dowhat,writefile,lDebug)
    handler.readFromDbAndCreateSetsAccordingToDoWhat(outfile) 
    
    auths=handler.get_passcode_2_authors()
    papers=handler.get_passcode_2_papers()
    years=handler.get_passcode_2_years()
    confs=handler.get_passcode_2_confs()
    subs=handler.get_passcode_2_subs()
    ris=handler.get_passcode_2_resources()
    #print "AUTH "+str(len(papers))
    if dowhat=="a":
        idx=0+writefile
        headerFile =handler.switchHeaderFile(idx)  
        outputFile=handler.switchOutputFile(idx)     
        SerializeAuthor(auths, writefile, outputFile, headerFile,lDebug)
    if dowhat=="p":
        idx=2+writefile
        headerFile =handler.switchHeaderFile(idx)  
        outputFile=handler.switchOutputFile(idx) 
        
        SerializePaper(papers,auths,writefile, outputFile, headerFile,lDebug,handler.get_status_in_bibo()) 
    
    if dowhat=="ap":
        idx=0+writefile
        headerFile =handler.switchHeaderFile(idx)  
        outputFile=handler.switchOutputFile(idx)
        SerializeAuthor(auths, writefile, outputFile, headerFile,lDebug)  
        idxp=2+writefile
        headerFile =handler.switchHeaderFile(idxp)  
        outputFile=handler.switchOutputFile(idxp) 
        SerializePaper(papers,auths,writefile, outputFile, headerFile,lDebug,handler.get_status_in_bibo())  
        
    if dowhat=="y":
        idx=4+writefile
        headerFile =handler.switchHeaderFile(idx)  
        outputFile=handler.switchOutputFile(idx)
        print outputFile
        SerializeYear(years, writefile, outputFile, headerFile,lDebug)
        
    if dowhat=="c":
        idx=6+writefile
        headerFile =handler.switchHeaderFile(idx)  
        outputFile=handler.switchOutputFile(idx)
        SerializeConference(confs, writefile, outputFile, headerFile,lDebug)
        
    if dowhat=="s":
        idx=8+writefile
        headerFile =handler.switchHeaderFile(idx)  
        outputFile=handler.switchOutputFile(idx)
        SerializeSubmission(subs,confs, papers,writefile, outputFile, headerFile,lDebug)                  
      
    if dowhat =="s+":
        idxp=2+writefile
        headerFile =handler.switchHeaderFile(idxp)  
        outputFile=handler.switchOutputFile(idxp) 
        SerializePaper(papers,auths,writefile, outputFile, headerFile,lDebug,handler.get_status_in_bibo()) 
        
        idx=6+writefile
        headerFile =handler.switchHeaderFile(idx)  
        outputFile=handler.switchOutputFile(idx)
        SerializeConference(confs, writefile, outputFile, headerFile,lDebug)
        
        idx=8+writefile
        headerFile =handler.switchHeaderFile(idx)  
        outputFile=handler.switchOutputFile(idx)
        SerializeSubmission(subs,confs, papers,writefile, outputFile, headerFile,lDebug)
    
    
    if dowhat=="r":
        idx=8+writefile
        headerFile =handler.switchHeaderFile(idx)  
        outputFile=handler.switchOutputFile(idx)
        SerializeSubmission(subs,confs, papers,writefile, outputFile, headerFile,lDebug)
        idx=10+writefile
        headerFile =handler.switchHeaderFile(idx)  
        outputFile=handler.switchOutputFile(idx)
        SerializeResource(ris, subs,writefile, outputFile, headerFile,lDebug,handler.get_resourcetypes_in_map_db(), 
                          handler.get_availabilities_in_map_db(), handler.get_status_in_map_db(),
                          handler.get_modalities_in_map_db(), handler.get_uses_in_map_db() )
        
    
            #print p +"\t"+str(auth.get_affiliation().get_country_code())
    
            

def main():
    args = sys.argv[1:]
    if len(args) != 5:
        print 'usage: python main.py dowhat verbose stat_debug parser_debug writefiles'
        print '\twritefiles 0 for single file, 1 for distinct files:'
        print '\tdowhat is a string with the following values:'
        print '\t\t y\t to extract the list of years'
        print '\t\t c\t to extract the list of conferences'
        print '\t\t s\t to extract the list of submissions'
        print '\t\t a\t to extract the list of authors'
        print '\t\t p\t to extract the list of papers'
        print '\t\t ap\t to extract the list of papers and connected authors'
        print '\t\t r\t to extract the list of resources'
        print '\t\t rn\t to extract the list of normalized resources'
        print '\t\t rt\t to extract the list of template resources'
        print '\t\t all\t to extract all the map'
       
        sys.exit(-1)
        
    
    outfile=sys.stdout    
    #outfile="./out/stdout"
    now=datetime.datetime.now()
    print '---------------------------'
    print "\t Started: "+now.strftime("%Y-%m-%d %H:%M:%S")
    lremap(outfile,args[0], int(args[1]), int(args[2]), int(args[3]),int(args[4]))
    now=datetime.datetime.now()
    print '---------------------------'
    print "\t Ended: "+now.strftime("%Y-%m-%d %H:%M:%S")
    
    now=datetime.datetime.now()
    print '---------------------------'    


if __name__ == '__main__':
    main()