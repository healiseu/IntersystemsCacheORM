import sys
import pandas as pd

from intersys import pythonbind3

## *********************************************************************************
# ******************************** Module Function Definitions *********************

def print_exception(err):
    print()
    print(' ********** InterSystems Cache exception ********** ')
    print('Exception Type      : ',sys.exc_info()[0])
    print('Exception Value     : ',sys.exc_info()[1])
    print('Exception Traceback : ',sys.exc_info()[2])
    print(' ************************************************** ')
    print('Exception Error     : ',str(err))

# *****************************************************************************
# ******************************** Classes Specifications *********************
# *****************************************************************************

class CacheClient(object):
    """
    This is the super class of CachePython module. 
    It wraps two functions from intersys.pythonbind module
    pythonbind3.connection() and  pythonbind3.database(). 
    """        
    def __init__(self, host='localhost', port=1972, 
                 username='_SYSTEM', password='SYS', 
                 namespace='SAMPLES', dl=0):

        """
        CacheClient.__init__
        ----------------------
        Initialization of a CacheClient object
        
        
        Optional Keyword Arguments
        ---------------------------
        host : string  -- (default = 'localhost')
            Intersystems Cache database server

        port : integer -- (default = 1972)
            Intersystems Cache Server TCP/IP port that is used to accept incoming client requests

        username : string  -- (default = '_SYSTEM')
            Intersystems Cache username

        password : string -- (default = 'SYS')
            Intersystems Cache authentication method with password

        namespace : string -- (default = 'SAMPLES')
            Intersystems Cache Namespace containing the objects to be used.
            This namespace must have the Caché system classes compiled,
            and must contain the objects you want to manipulate
            
        debug : boolean -- (default = False)
            print messages for debugging purposes
        
        Private Instance Attributes 
        ---------------------------
        _connection : Intersystems Cache Connection instance (intersys.pythonbind.connection)
        
        _database   : Intersystems Cache Database instance (intersys.pythonbind.database)
       
        """
        
        self.cache_host = host
        self.cache_port = port
        self.cache_username = username
        self.cache_password  = password
        self.cache_namespace = namespace
        self.debug_level = dl        

        # Debug messages
        if self.debug_level==99:
            print('Cache Python Object-Relational Mapper Module : ')
            print('Enhanced OOP porting of Intersystems Cache python binding modules')
            print('(C) 2017-2018 HEALIS.EU - Athanassios I. Hatzis\n')
            print('GNU Lesser General Public License v3.0\n')

        # try to create intersys.pythonbind.connection object                
        try:
            self._connection = pythonbind3.connection()
            
            url = self.cache_host+'['+str(self.cache_port)+']:'+self.cache_namespace
            self._connection.connect_now(url, self.cache_username, self.cache_password, None)
            if self.debug_level>1:
                print('CACHE Connection object to ', self.cache_namespace, ' is created successfully.')
            
            self.connection_version = self._connection.get_implementation_version()
            if self.debug_level>1:
                print('CACHE Connection Implementation Version : ',self.connection_version)
            
        except pythonbind3.cache_exception as err:
            print_exception(err)

        # try to create intersys.pythonbind.database object        
        try:
            self._database = pythonbind3.database(self._connection)
            if self.debug_level>1:
                print('CACHE Database object is created successfully')
            
        except  pythonbind3.database_exception as err:
            print_exception(err)
 
    def __repr__(self):
        return f"{self.cache_host}, {self.cache_port}, {self.cache_username}, {self.cache_password}, {self.cache_namespace}"

       
    def __str__(self):
        return f"host='{self.cache_host}', port={self.cache_port}, username='{self.cache_username}', password='{self.cache_password}', namespace='{self.cache_namespace}'"
    
    @property    
    def private_attributes(self):
        type1 = type(self._database)
        type2 = type(self._connection)
        return f'CACHE_Database   : {type1} \nCACHE_Connection : {type2}'
    
    
# *********************************************************************************
# ************************** End of CacheClient ***********************************
# *********************************************************************************

class CacheQuery(CacheClient):
    '''
    A subclass of CacheClient that wraps methods of the intersys.pythonbind.database 
    class and intersys.pythonbind.query class. Provides enhanced usage of Cache Queries.
    '''            
    
    def __init__(self, cachepackage='Sample', cacheclass = 'Person', **kwargs):
        """
        CacheQuery.__init__
        --------------------------------
        CacheQuery initialization method 
        
        
        Private Instance Attributes
        --------------------------    
        _query : Intersystems Cache query object (intersys.pythonbind.query)        
                
        
        Examples
        ----------
        >>> samples_query = CacheQuery(namespace = "SAMPLES")
        >>> samples_query = CacheQuery(username='athanassios', password='123', namespace='SAMPLES')
        """        
        
        # invoke CacheClient __init__ method
        super().__init__(**kwargs) 
        self.cache_package           = cachepackage
        self.cache_classname         = cacheclass
        self.cache_classname_package = self.cache_package + '.' + self.cache_classname
        self.cache_classname_full    = self.cache_namespace + '.' + self.cache_package + '.' + self.cache_classname
        
        try:
            # create intersys.pythonbind.query object        
            self._query = pythonbind3.query(self._database)
            
            if self.debug_level>1:
                print('CACHE Query object created successfully')        
            
            self.total_records=0          # total number of records in the result set
            self.counter = 0              # count records fetched from result_set
            self.record_set = None        # Pandas DataFrame to display result_set
        except pythonbind3.cache_exception as err:
            print_exception(err)     


    def __repr__(self):
        return "CacheQuery(" + super().__repr__() + f", {self.cache_package}, {self.cache_classname})"
       
        
    def __str__(self):
        return "CacheQuery(" + super().__str__() + f", cachepackage='{self.cache_package}', cacheclass='{self.cache_classname}')" 

        
    @property    
    def private_attributes(self):        
        return f'CACHE_Query      : {type(self._query)} \n' + super().private_attributes
        

    @property
    def result_set(self):        
        """
        This is a generator based on the result set 
        that is fetched through the cache_query attribute
        
        Returns
        ---------
        returns records from the result set, one record at a time
        
        """                        
        while True:
            single_record = self._query.fetch([None])
            # If the list of single_record is empty break else yield the record
            if not single_record:
                break
            else:
                yield single_record 


    # result set columns - getter method
    @property
    def columns(self):
        """
        get the column header of the result set
        
        Returns
        ---------
        A python list of names for each of the columns in the query result set
        
        Examples
        ----------
        >>> samples_query.columns
        """
        return [self._query.col_name(idx) for idx in range(1,self._query.num_cols()+1)]
    

    # columns types - getter method
    @property
    def columns_types(self):
        """
        get the sql types for each column in the header of the result set 
        
        Returns
        ---------
        A python list of sql types for each of the columns in the query result set
        
        Examples
        ----------
        >>> samples_query.columns_types
        """
        
        return [self._query.col_sql_type(idx) for idx in range(1,self._query.num_cols()+1)]

    def execute(self):
        self._query.execute()  # execute generates the record result set
        self.counter = 0       # reset the counter
        if self.debug_level>1 :
            print('result set is now ready and can be fetched')

    def execute_call(self, clname, procname, *params):
        """
        prepares and executes an SQL procedure call.
        This is usually a class method or class query 
        that is exposed as an SQL stored procedure
        
        Notice
        ------
        you can invoke SQL stored procedure with the CALL statement
        by passing an sql string to execute_sql
        
        
        Keyword argument
        ----------------
        class_name : string
            name of Cache class that is defined in the current namespace.package
        proc_name : string
            either the name of a class method or class query         

        
        Examples
        ----------        
        >>> samples_query.execute_call('Person', 'Extent')
        >>> samples_query.execute_call('Person', 'ByName', 'A')
        """
        clname=self.cache_package+'.'+clname
        self._query.prepare_class(clname, procname)
        idx = 0
        for par in params:            
            idx = idx+1
            self._query.set_par(idx, par)        
        self.execute()        

    def execute_sql(self, sql, *params):
        """
        prepares and executes an SQL query
        
        Notice
        ---------------
        the result set is fetched from the result_set generator

        Keyword arguments
        ----------------
        sql : string
            SQL commands to be executed
        
        Examples
        ----------
        >>> samples_query.execute_query_sql('SELECT ID, Name, DOB, SSN FROM Sample.Person')
        >>> samples_query.execute_query_sql('CALL HYPEDB.Node_ViewUnionByType')
        """
        self._query.prepare(sql)
        idx = 0
        for par in params:            
            idx = idx+1
            self._query.set_par(idx, par)
        self.execute()
        
    # total number of records in the result set
    def count_records(self):
        self.total_records=0
        while True:
            try:
                next(self.result_set)
                self.counter=self.counter+1
                self.total_records=self.total_records+1
            except StopIteration:
                return self.total_records
                break

    def display_records(self, iterations=10, maxrows=False, maxwidth=180):
        # Set display width for PANDAS Data Frame
        pd.set_option('display.width', maxwidth)
        
        # Check whether to display ALL rows of the PANDAS Data Frame or NOT
        if maxrows and self.total_records>0:
            pd.set_option('display.max_rows',self.total_records)                
        else:
            pd.reset_option('display.max_rows')
        
        # Fill Pandas Data Frame with a number of records that are fetched from the query result set
        self.record_set = pd.DataFrame(columns = self.columns)
        for i in range(iterations):
            try:
                elem = next(self.result_set)
                self.record_set.loc[i]=elem
                self.counter=self.counter+1
            except StopIteration:
                print("Execution reached the end of the result set")
                return self.record_set
                break
        return self.record_set
        
    def print_records(self, iterations=10):        
        for i in range(iterations):
            try:
                elem = next(self.result_set)
                self.counter=self.counter+1
                print(f"Iter: {i}, Cnt: {self.counter} - Element: {elem}")
            except (StopIteration, pythonbind3.cache_exception) as err:
                print_exception(err)
                print("Execution reached the end of the result set")
                break
    
    def skip_records(self, iternum=1):
        for i in range(iternum):
            try:
                next(self.result_set)
                self.counter=self.counter+1
            except StopIteration:
                print("Execution reached the end of the result set")
                break

# ************************************************************************************
# ************************ End of CacheQuery Class ************************************
# *************************************************************************************

class CacheClass(CacheClient):
    ''' 
    A subclass of CacheClient, that wraps methods of 
    the intersys.pythonbind.Database class and the intersys.pythonbind.object class
    '''

    def __init__(self, cachepackage='Sample', cacheclass='Person', objectID=None, **kwargs):
        """
        CacheClass.__init__
        --------------------
        CacheClass initialization method 
       
        
        Keyword argument
        ----------------        
        cachepackage : string -- (default = Sample)
        cacheclass   : string -- (default = Person)
        objectID     : string -- (default = None)
            An object identifier. 
            A value that uniquely identifies a specific instance within a particular Cache extent
            The ID refers to an on-disk version of an object. 
            It does not include any class-specific information.


        Private Instance Attributes
        --------------------------        
        _instance : Intersystems Cache object (intersys.pythonbind.object)
            it is set with a call to either cache_database.create_new() or cache_database.openid(                
    
        
                                    
        Examples
        ----------        
        >>> personClass = CacheClass(cacheclass='Employee')
        >>> person = CacheClass(namespace = 'SAMPLES', cacheclass='Sample.Person', objectID='1')
        >>> person = CacheInstance()
        """

        # invoke CacheClient __init__ method
        super().__init__(**kwargs) 
        self.cache_package           = cachepackage
        self.cache_classname         = cacheclass
        self.cache_classname_package = self.cache_package + '.' + self.cache_classname
        self.cache_classname_full    = self.cache_namespace + '.' + self.cache_package + '.' + self.cache_classname
        self._cache_id = objectID

        # set an instance of intersys.pythonbind.object
        if objectID:
            # open an instance of intersys.pythonbind.database object with ID
            self._instance, self._cache_id = self.open_id(objectID) 
        else:
            self._instance=None
        
        if self.debug_level>1:
            print('CACHE Class object is created successfully')
            print('CACHE Instance object is created successfully')
                                            
    # There are three cases
    def __repr__(self):
        
        # a) Instance of the CacheClass no CACHE Object is created and no CACHE Object is open
        if self._instance is None:
            return "CacheClass(" + CacheClient.__repr__(self) + f", '{self.cache_classname_full}', 'No Object Set')"
        
        # b) Instance of the CacheClass with a new CACHE Object created
        elif (self._instance is not None) and (self._cache_id is None):
            return "CacheClass Object(" + CacheClient.__repr__(self) + f", '{self.cache_classname_full}', 'New Object Set')"
        
        # c) Instance of the CacheClass with a CACHE Object that exists in the database
        elif self._cache_id is not None:
            return "CacheClass Object(" + CacheClient.__repr__(self) + f", '{self.cache_classname_full}', '{self._cache_id}')"

    # There are three cases
    def __str__(self):
        # a) Instance of the CacheClass no CACHE Object is created and no CACHE Object is open
        if self._instance is None:
            return "CacheClass(" + CacheClient.__str__(self) + f", cacheclass='{self.cache_classname_full}', 'No Object Set')"
        
        # b) Instance of the CacheClass with a new CACHE Object created
        elif (self._instance is not None) and (self._cache_id is None):       
            return "CacheClass(" + CacheClient.__str__(self) + f", cacheclass='{self.cache_classname_full}', 'New Object Set')"
        
        # c) Instance of the CacheClass with a CACHE Object that exists in the database
        elif self._cache_id is not None:
            return "CacheClass(" + CacheClient.__str__(self) + f", cacheclass='{self.cache_classname_full}', objectID='{self._cache_id}')"

        
    @property    
    def private_attributes(self):
        return f'CACHE_Object     : {type(self._instance)} \n' + super().private_attributes

                         
    @property
    def id(self):
         if not self._cache_id:
             return None
         else:
             return self.object_method('%Id')

    @property
    def cache_objref(self):
        return self._instance

    
    @property
    def description(self):
        return self._instance.get_obj_desc()
                
# ************************************************************************
# ======= METHODS SECTION =======    
                        
    def class_method(self, method_name, *kargs):
        try:
            return self._database.run_class_method(self.cache_classname_package, method_name, list(kargs))
        except  pythonbind3.cache_exception as err:
            print_exception(err)
    
    # Create a new object in CACHE _database that is already connected in the instance of CacheClass
    # Attention: We do not open another connection here to create the object    
    def new(self):
        self._cache_id=None
        # create a new instance of intersys.pythonbind.database object
        self._instance = self._database.create_new(self.cache_classname_package, None)
        return self


    def save(self):
        if self._instance is None:
            raise RuntimeError("No Object has been created or opened in the database")
        else:
            result = self.object_method("%Save")
            self._cache_id = self.object_method("%Id")
        
        return self, result
    

    def open_id(self, object_id):
        # check if there is a record with this ID in the class        
        if not self.exists_id(object_id):
            message = "Record with objectID " + object_id + " does not exist in " + self.cache_classname_full
            raise ValueError(message)
        else:
            intersysobj = self._database.openid(self.cache_classname_package, object_id, -1, -1)                    
            return intersysobj, object_id
    

    def get(self, prop_name):
        if self._instance is None:
            raise RuntimeError("No Object has been created or opened in the database")
        else:
            return self._instance.get(prop_name)        
    

    def set_value(self, prop_name, value):
        if self._instance is None:
            raise RuntimeError("No Object has been created or opened in the database")
        else:
            self._instance.set(prop_name, value)


    def set_embobj(self, classname, propname, **kwargs):
        # we create a new intersys.pythonbind3.object
        # because an attempt to pass a reference with the set_value()
        # results to the same cache ID (see testCacheInstance2)
        # and an attempt to save it result in circular reference        
        intersysobj = self._database.create_new(classname, None)
        self._instance.set(propname, intersysobj)
        return intersysobj


    def set_refobj(self, prop_name, cacheid):
        # we create a new intersys.pythonbind3.object
        # because an attempt to pass a reference with the set_value()
        # results to the same cache ID (see testCacheInstance2)
        #
        # check if there is a record with this ID in the class        
        if not self.exists_id(cacheid):
            message = "Record with objectID " + cacheid + " does not exist in " + self.cache_classname_full
            raise ValueError(message)
        else:
            intersysobj = self._database.openid(self.cache_classname_package, cacheid, -1, -1)
            self._instance.set(prop_name, intersysobj)
            return intersysobj
        
        
    def exists_id(self, object_id):
        result = self.class_method('%ExistsId', object_id)
        if result==1:
            return True
        elif result==0:
            return False


    def delete_id(self, object_id):
        if self.exists_id(object_id):
            result = self.class_method('%DeleteId', object_id)
        else:
            result = False
        return result
         
    
    def object_method(self, method_name, *kargs):
        try:
            return self._instance.run_obj_method(method_name, list(kargs))
        except  pythonbind3.cache_exception as err:
            print_exception(err)
    
# *********************************************************************************
# ************************** End of CacheClass ***********************************
# *********************************************************************************
