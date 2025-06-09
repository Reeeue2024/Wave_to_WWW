# [ Kernel ] Kernel Resource : kernel_resource.py

from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
import pickle

class KernelResource :
    def __init__(self) :
        self.resource_dictionary = {}

    """
    IN : 
    OUT : 
    """
    def load_resource(self) :
        print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(" [ Kernel Resource ] Load Resource ...")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

        load_dotenv() # [ .env ] Load "MONGO_URI"

        try :
            uri = os.getenv("MONGODB_URI")

            if not uri or not isinstance(uri, str) :
                raise ValueError("[ ERROR ] \"MONGODB_URI\" is INVALID.")
            
            client = MongoClient(uri, server_api = ServerApi("1")) # [ Mongo ] API Version 1
            db = client["kernel"]

            # print(f"[ DEBUG ] URI : {uri}")

            # print("  [ Start Log ]  Connect to \"Mongo\"")

        except Exception as e :
            print(f"[ ERROR ] Fail to Run - Kernel Resource : {type(e).__name__}")
            print(f"{e}")

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
            "short_domain_list" : lambda : list(db["short_domain_list"].find({}, {"_id" : 0})),
            "ssl_free_ca_list" : lambda : list(db["ssl_free_ca_list"].find({}, {"_id" : 0})),
            "ssl_not_trust_ca_list" : lambda : list(db["ssl_not_trust_ca_list"].find({}, {"_id" : 0})),
            "free_tld_list" : lambda : list(db["free_tld_list"].find({}, {"_id" : 0})),
            "country_tld_list" : lambda : list(db["country_tld_list"].find({}, {"_id" : 0})),
        }

        for resource_name, function in function_dictionary.items() :

            # print(f"  [ DEBUG ] Load Resource : {resource_name}")

            try :
                self.resource_dictionary[resource_name] = function()

                print(f"  [ + ]  {resource_name:<25} ( Load Resource - Success )")
            
            except Exception as e :
                self.resource_dictionary[resource_name] = []
                
                print(f"  [ ! ]  {resource_name:<25} ( Load Resource - Fail )")
                print(f"{e}")
        
        # ( AI ) Get PKL File - Model + Scalar
        try :
            base_directory = os.path.dirname(os.path.abspath(__file__))
            model_pkl_file_path = os.path.join(base_directory, "plugins", "ai_modules", "ai_model", "rf_29features_0603.pkl")
            scalar_pkl_file_path = os.path.join(base_directory, "plugins", "ai_modules", "ai_model", "rf_29features_scaler_0603.pkl") 

            if not os.path.exists(model_pkl_file_path) :

                raise FileNotFoundError(f"[ ERROR ] Fail to Get AI Model File : {model_pkl_file_path}")

            if not os.path.exists(scalar_pkl_file_path) :

                raise FileNotFoundError(f"[ ERROR ] Fail to Get AI Scalar File : {scalar_pkl_file_path}")

        except Exception as e :
            self.resource_dictionary["ai_model_bundle"] = None
            self.resource_dictionary["ai_scalar_bundle"] = None
            
            print(f"  [ ! ]  {'ai_model_bundle':<25} ( Get Resource - Fail )")
            print(f"  [ ! ]  {'ai_scalar_bundle':<25} ( Get Resource - Fail )")
            print(f"{e}")
        
        # ( AI ) Load PKL File - Model
        try :
            with open(model_pkl_file_path, "rb") as f :

                model_bundle = pickle.load(f)

            self.resource_dictionary["ai_model_bundle"] = model_bundle

            print(f"  [ + ]  {'ai_model_bundle':<25} ( Load Resource - Success )")

        except Exception as e :
            self.resource_dictionary["ai_model_bundle"] = None
            
            print(f"  [ ! ]  {'ai_model_bundle':<25} ( Load Resource - Fail )")
            print(f"{e}")
        
        # ( AI ) Load PKL File - Scalar
        try :
            with open(scalar_pkl_file_path, "rb") as f :

                scalar_bundle = pickle.load(f)

            self.resource_dictionary["ai_scalar_bundle"] = scalar_bundle

            print(f"  [ + ]  {'ai_scalar_bundle':<25} ( Load Resource - Success )")
        
        except Exception as e :
            self.resource_dictionary["ai_scalar_bundle"] = None
            
            print(f"  [ ! ]  {'ai_scalar_bundle':<25} ( Load Resource - Fail )")
            print(f"{e}")
        
        print()

    """
    IN : 
    OUT : 
    """
    def get_resource(self, resource_name) :
        return self.resource_dictionary.get(resource_name, [])

# Single Instance
kernel_resource_instance = KernelResource()
