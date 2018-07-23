from intersys import pythonbind3
import sys

user="_SYSTEM"
password="1233"
host = "localhost"
port = "1972"

def print_exception(err):
    print()
    print(' ********** InterSystems Cache exception ********** ')
    print('Exception Type      : ',sys.exc_info()[0])
    print('Exception Value     : ',sys.exc_info()[1])
    print('Exception Traceback : ',sys.exc_info()[2])
    print(' ************************************************** ')
    print('Exception Error     : ',str(err))

#%%
try:
    url = host+"["+port+"]:SAMPLES"  
    conn = pythonbind3.connection( )
    conn.connect_now(url, user, password, None)
    database = pythonbind3.database( conn)
    person =  database.create_new("Sample.Person", None)
    person.set("Name","Doe, Joe A")

    # Save instance of Person
    person.run_obj_method("%Save",[])

    # Create a new instance of Sample.Person to be spouse
    spouse =  database.create_new("Sample.Person", None)
    spouse.set("Name","Doe, Mary")
    person.set("Spouse",spouse)
    person.run_obj_method("%Save",[])

    # Save instance of Person
    spouse.set("Spouse",person)
    spouse.run_obj_method("%Save",[])
        
    print("Sample finished running")
except pythonbind3.cache_exception as err:
    print_exception(err)