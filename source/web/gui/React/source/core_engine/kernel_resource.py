# [ Core ] Kernel - Kernel Resource : kernel_resource.py

from pymongo import MongoClient # pip install pymongo
from pymongo.server_api import ServerApi
from dotenv import load_dotenv # pip install python-dotenv
import os

class KernelResource :
    def __init__(self) :
        self.resource_dictionary = {}

    """
    IN : 
    OUT : 
    """
    def load_resources(self) :
        print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(" [ Kernel Resource ] Load Resources ...")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

        load_dotenv() # [ .env ] Load "MONGODB_URI"

        try :
            uri = os.getenv("MONGODB_URI")
            client = MongoClient(uri, server_api = ServerApi("1")) # [ MongoDB ] Stable API Version 1
            db = client["kernel"]

            print("  [ Start Log ]  Connect to \"MongoDB\"")

        except Exception as e :
            print("  [ Fail ]  Connect to \"MongoDB\"")

            return

        function_dictionary = {
            # Black List
            "black_list_url" : lambda : list(db["black_list_url"].find({}, {"_id" : 0})), # ( Example ) "https://google.com"
            "black_list_domain_suffix" : lambda : list(db["black_list_domain_suffix"].find({}, {"_id" : 0})),  # ( Example ) "google.com"
            "black_list_brand" : lambda : list(db["black_list_brand"].find({}, {"_id" : 0})),  # ( Example ) "google"

            # White List
            "white_list_url" : lambda : list(db["white_list_url"].find({}, {"_id" : 0})),
            "white_list_domain_suffix" : lambda : list(db["white_list_domain_suffix"].find({}, {"_id" : 0})),
            "white_list_brand" : lambda : list(db["white_list_brand"].find({}, {"_id" : 0})),

            # ETC
            "tiny_domain_list" : lambda : list(db["tiny_domain_list"].find({}, {"_id" : 0})),
            "ssl_free_ca_list" : lambda : list(db["ssl_free_ca_list"].find({}, {"_id" : 0})),
            "ssl_low_trust_ca_list" : lambda : list(db["ssl_low_trust_ca_list"].find({}, {"_id" : 0})),
            "free_tld_list" : lambda : list(db["free_tld_list"].find({}, {"_id" : 0})),
            "country_tld_list" : lambda : list(db["country_tld_list"].find({}, {"_id" : 0})),
        }

        for resource_name, function in function_dictionary.items() :

            try :
                self.resource_dictionary[resource_name] = function()

                print(f"  [ + ]  {resource_name:<15} ( Load Resource - Success )")
            
            except Exception as e :
                print(f"  [ ! ]  {resource_name:<15} ( Load Resource - Fail )")
                print(f"{e}")
        
        print()

    """
    IN : 
    OUT : 
    """
    def get_resource(self, resource_name) :
        return self.resource_dictionary.get(resource_name)

# Single Instance
kernel_resource_instance = KernelResource()
