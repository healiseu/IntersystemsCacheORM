# Demo of Intersystems Cache Python binding with Samples namespace and Sample.Person class
import intersys.pythonbind3

conn = intersys.pythonbind3.connection( )
conn.connect_now('localhost[1972]:SAMPLES', '_SYSTEM', '123', None)
samplesDB = intersys.pythonbind3.database(conn)

#%% Create a new instance of Sample.Person to be husband
husband =  samplesDB.create_new("Sample.Person", None)
ssn1 = samplesDB.run_class_method("%Library.PopulateUtils","SSN",[])
dob1 = samplesDB.run_class_method("%Library.PopulateUtils","Date",[])
husband.set("Name","Hatzis, Athanassios I")
husband.set("SSN",ssn1)
husband.set("DOB",dob1)

# Save husband
husband.run_obj_method("%Save",[])
print ("Saved id: "+str(husband.run_obj_method("%Id",[])))

#%% Create a new instance of Sample.Person to be wife
wife =  samplesDB.create_new("Sample.Person", None);
ssn2 = samplesDB.run_class_method("%Library.PopulateUtils","SSN",[])
dob2 = samplesDB.run_class_method("%Library.PopulateUtils","Date",[])
wife.set("Name","Kalamari, Panajota");
wife.set("SSN",ssn2)
wife.set("DOB",dob2)

# Save wife
wife.set("Spouse",husband);
wife.run_obj_method("%Save",[]);
print ("Saved id: " + str(wife.run_obj_method("%Id",[])))

#%% Relate them
husband.set("Spouse",wife);
husband.run_obj_method("%Save",[]);

wife.set("Spouse",husband);
wife.run_obj_method("%Save",[]);

#%%
# check if ID exists in the database by defining a function
def CheckID(db,id):
    if not db.run_class_method("Sample.Person","%ExistsId",[str(id)]):
        print("There is no person with id "+ str(id) + " in the database." )
        return 0
    else:
        print('OK, ID exists')
        return 1

# Open an instance of the Sample.Person object
athanID=217
if CheckID(samplesDB,athanID):    
    athanPerson = samplesDB.openid("Sample.Person",str(athanID),-1,-1)

# Open another instance
otherID=3
otherPerson = samplesDB.openid("Sample.Person",str(otherID),-1,-1)   
 
# Fetch some properties
print ("ID:   " + otherPerson.run_obj_method("%Id",[]))
print ("Name: " + otherPerson.get("Name"))
print ("SSN:  " + otherPerson.get("SSN"))
print ("DOB:  " + str(otherPerson.get("DOB")))
print ("Age: " + str(otherPerson.get("Age")))
    
#Attempt to bring in an embedded object
addr = otherPerson.get("Home");
print ("Street: " + addr.get("Street"))
print ("City:   " + addr.get("City"))
print ("State:  " + addr.get("State"))
print ("Zip:  " + addr.get("Zip"))    
print ("Sample finished running")

