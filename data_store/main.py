# This file is responsible for handling all the user requests.

import pathlib, json, os, sys
import time

# The path of the datastore and data it stores, the path will not change unless other filepath is specified by user

class DataStore:
    def __init__(self):
        self.path = os.getcwd()+"\\default.json"
        self.error_dict = {
                        "KEY_ERROR":" Key does not exist",
                        "KEY_MAX_LENGTH":" Longer than 32 character", 
                        "KEY_EXIST_ERROR":" Key already exist", 
                        "VALUE_MAX_LENGTH": " Given Value is greater than 16kb", 
                        "FILE_SIZE_EXCEED": "File is exceeding the 1GB limit"
                    }
    def create_datastore(self,**kwargs) :
        '''
            Argument :-
                arg1 : String
            Description :-
                This method will create the datastore. 
                Optional argument Filepath. 
                Default filename = "default.json" 
        '''
        if('filepath' in kwargs):
            self.path = kwargs['filepath']
        
        #Checks if the file exists or not
        isFile_exist = os.path.exists(self.path)
        if(not isFile_exist) :
            with open(self.path, "w") as f:
                json.dump({}, f)

    def write_data(self,key, value, **kwargs):
        """
            Description -     
                arg1: key,
                arg2: value,
                Optional kwargs: "time to live property of the given key" Default : 100
                This method writes the data into the file that has been passed as a argument.
        """
        if(self.check_key(key)):
            self.print_error(key,"KEY_EXIST_ERROR")
            return 

        if('time_to_live' in kwargs):
            time_to_live = kwargs['time_to_live']
        else:
            time_to_live = 100

        
        with open(self.path) as f:
            data = json.load(f)
            if(len(key) > 32):
                self.print_error(key,"KEY_MAX_LENGTH")
                return

            if(sys.getsizeof(value)> 16 * 1024):
                self.print_error(str(value), "VALUE_MAX_LENGTH")
                return

            final_value = {"value" : value, "timestamp": time.time(), "time_to_live":time_to_live}

            if(os.path.getsize(self.path)+sys.getsizeof(final_value)+sys.getsizeof(key)>1024*1024):
                self.print_error("\n", "FILE_SIZE_EXCEED")
                return

            data[key] = final_value
        
            with open(self.path,'w') as f:
                json.dump(data,f, indent=3)

    def delete_key(self,key):
        """
        arg1: key
        This method accepts key as argument and delete the given key, if present.
        """
        with open(self.path) as f:
            data = json.load(f)
        
        del data[key]

        with open(self.path, 'w') as f:
            json.dump(data, f, indent=3)

    def check_key(self,key):
        """
            Checks if the key is valid or not
            rtype: bool
        """
        with open(self.path) as f:
            data = json.load(f)
            try:
                if(time.time() - data[key]["timestamp"] < data[key]["time_to_live"]):
                    return True
                else:
                    self.delete_key(key)
                    raise KeyError
            except KeyError:
                return False

    def read_data(self,key):
        """
        arg1 : key
        This method accepts key as an argument and read the given key if present.
        """
        with open(self.path) as f:
            data = json.load(f)
            if(self.check_key(key)):
                print(data[key])
            else:
                self.print_error(key,"KEY_ERROR")

    def print_error(self,key, error_type):
        print(key+self.error_dict[error_type])







