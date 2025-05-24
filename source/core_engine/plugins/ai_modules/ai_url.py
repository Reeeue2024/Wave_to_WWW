# [ Kernel ] Module - AI : ai_url.py

from core_engine.plugins._base_module import BaseModule
from core_engine.kernel_resource import kernel_resource_instance
from core_engine.plugins.ai_modules.ai_source.extract_features import extract_features

import sys
import pandas as pd

class AiUrl(BaseModule) :
    def __init__(self, input_url) :
        super().__init__(input_url)

        self.model = None
        self.scaler = None

    """
    IN  : 
    OUT : 
    """
    def load_model(self) :
        bundle = kernel_resource_instance.get_resource("ai_model_bundle")

        if not bundle :
        
            return False

        self.model = bundle["model"]
        self.scaler = bundle["scaler"]

        return True
    
    """
    IN  : 
    OUT : 
    """
    async def scan(self) :
        load_model_flag = self.load_model()

        if not load_model_flag :

            self.module_run = False
            self.module_error = "[ ERROR ] Fail to Get AI Model From Kernel Resource."
            self.module_result_flag = False
            self.module_result_data = None

        else :

            try :
                features = extract_features(self.input_url)
                X_input = pd.DataFrame([features])
                X_scaled = self.scaler.transform(X_input)
                
                result_flag = self.model.predict(X_scaled)[0]
                result_probability = round(self.model.predict_proba(X_scaled)[0][1], 2)

                self.module_run = True
                self.module_error = None
                self.module_result_flag = bool(result_flag)
                self.module_result_data["reason"] = f"Probability of Result : {float(result_probability)}"
                self.module_result_data["reason_data"] = features

            except Exception as e :
                self.module_run = False
                self.module_error = f"{e}"
                self.module_result_flag = False
                self.module_result_data = None

        self.create_module_result()

        # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

        return self.module_result_dictionary

# Module Main
if __name__ == "__main__" :

    # Input : URL
    if len(sys.argv) != 2 :

        print("How to Use : python3 ai_url.py < URL >")

        sys.exit(1)
    
    input_url = sys.argv[1]

    module_instance = AiUrl(input_url)
    
    module_instance.scan()
