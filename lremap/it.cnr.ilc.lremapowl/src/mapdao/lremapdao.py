'''
Created on Apr 30, 2014

@author: riccardo
'''
import lreMapDbApi
class LreMapDAO:
    '''
    classdocs
    '''
    verbose=0
    __connection=None
    global accessmapdb

    def __init__(self, user, passwd, db, host, verbose):
        self.user = user
        self.passwd = passwd
        self.db = db
        self.host = host
        self.verbose=verbose
        #self.connect()
        
        
    
    
    def connect(self): 
        name="lremapdao.connect"
        if(self.verbose==1):
            print "Executing "+name
        
        
        accessmapdb=lreMapDbApi.LreMapDbAPI(self.host,self.user,self.passwd,self.db,self.verbose)
        conn=accessmapdb.connectToDb(self.host,self.user,self.passwd,self.db)
        self.set_connection(conn)
        return conn

    def get_connection(self):
        return self.__connection


    def set_connection(self, value):
        self.__connection = value


    def del_connection(self):
        del self.__connection

    connection = property(get_connection, set_connection, del_connection, "connection's docstring")
        
           
        

        