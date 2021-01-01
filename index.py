#Import necessary modules

from data_store.main import DataStore

# Create object
Data1 = DataStore()

#Create a datastore
Data1.create_datastore(filepath="index.json")

#Write in the datastore
Data1.write_data("age1", 24)

#Read in the datastore
Data1.read_data("age1")




