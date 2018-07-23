# Demo of Intersystems Cache Python binding with Samples namespace and Sample.Person class
import intersys.pythonbind3

# version of Caché running on the Python client machine
print(intersys.pythonbind3.get_client_version())

#%%
# Create a connection 
user="_SYSTEM";
password="123";
host = "localhost";
port = "1972";
url = host+"["+port+"]:SAMPLES"  
conn = intersys.pythonbind3.connection()

# Connect Now to SAMPLES namespace
conn.connect_now(url, user, password, None)

# Create a database object
samplesDB = intersys.pythonbind3.database(conn)

#%%
# create a query object
cq = intersys.pythonbind3.query(samplesDB)

# prepare and execute query
sql = "SELECT ID, Name, DOB, SSN FROM Sample.Person"
cq.prepare(sql)
cq.execute()

# Fetch rows
for x in range(0,10): 
    print(cq.fetch([None]))

