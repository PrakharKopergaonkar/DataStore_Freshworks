from data_store.main import DataStore

# Create object
Data1 = DataStore()

#Create a datastore
Data1.create_datastore(filepath="index.json")

#Write in the datastore
Data1.write_data("age1", 24)
Data1.write_data("age2", 26)

#Read in the datastore
Data1.read_data("age1")

#Delete in the datastore
Data1.delete_key("age2")




