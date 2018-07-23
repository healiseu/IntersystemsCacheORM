# Demo of Intersystems Cache Python binding with Samples namespace and Sample.Person class
import intersys.pythonbind3

# Create a connection to SAMPLES namespace
user="_SYSTEM";
password="123";
host = "localhost";
port = "1972";
url = host+"["+port+"]:SAMPLES"  
conn = intersys.pythonbind3.connection( )
conn.connect_now(url, user, password, None)
samplesDB = intersys.pythonbind3.database(conn)

# create a query
cq = intersys.pythonbind3.query(samplesDB)
cq.prepare_class("Sample.Person", "ByName")
cq.set_par(1,"A")

#%%
# Execute and fetch rows
cq.execute()
for x in range(0,8): 
    print(cq.fetch([None]))
