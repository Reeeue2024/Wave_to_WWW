# [ Kernel ] Module - AI : ai.py

from kernel.plugins._base_module import BaseModule
from kernel.kernel_resource import kernel_resource_instance
from kernel.plugins.ai_modules.ai_source.extract_features_0603 import extract_features

import sys
import pandas as pd

class Ai(BaseModule) :
    def __init__(self, input_url) :
        super().__init__(input_url)

        self.model = None
        self.scaler = None

    """
    IN  : 
    OUT : 
    """
    def load_model(self) :
        mdoel_bundle = kernel_resource_instance.get_resource("ai_model_bundle")
        scalar_bundle = kernel_resource_instance.get_resource("ai_scalar_bundle")

        if not mdoel_bundle or not scalar_bundle :
        
            return False

        self.model = mdoel_bundle
        self.scaler = scalar_bundle

        return True
    
    """
    IN  : 
    OUT : 
    """
    async def scan(self) :
        load_model_flag = self.load_model()

        if not load_model_flag :

            self.module_run = False
            self.module_error = "[ ERROR ] Fail to Get AI Model / Scalar From Kernel Resource."
            self.module_result_flag = False
            self.module_result_data = None

        else :

            try :
                threshold = 0.7

                features, updated_feature_names, domain = extract_features(self.input_url)

                features_df = pd.DataFrame([features])[updated_feature_names]

                # 모델 추론
                scaled_array = self.scaler.transform(features_df)
                scaled_features = pd.DataFrame(scaled_array, columns=features_df.columns)
                raw_prob = self.model.predict_proba(scaled_features)[0][1]

                # 점수 보정
                row = features_df.iloc[0]
                boost = 0

                # 피싱 보정
                if row['phish_hints'] == 1: boost += 0.10
                if row['prefix_suffix'] == 1: boost += 0.06
                if row['Favicon'] == 1: boost += 0.05
                if row['shortest_word_host'] <= 2: boost += 0.04
                if row['longest_words_raw'] > 20: boost += 0.03
                if row['ratio_digits_url'] > 0.3: boost += 0.03
                if row['nb_hyperlinks'] < 5: boost += 0.03
                if row['ratio_intHyperlinks'] < 0.3: boost += 0.02
                if row['longest_words_raw'] > 30: boost += 0.03
                if row['longest_word_path'] > 20: boost += 0.03
                if row['Favicon'] == 1 and row['ratio_intHyperlinks'] < 0.3: boost += 0.04
                if row['prefix_suffix'] == 1 and row['shortest_word_host'] <= 2: boost += 0.04

                # 정상 보정
                if row['ratio_intHyperlinks'] > 0.6: boost -= 0.04
                if row['domain_in_title'] == 1: boost -= 0.02
                if row.get('Iframe', 1) == 0: boost -= 0.01
                if row['nb_hyperlinks'] > 20: boost -= 0.03
                # 신뢰 도메인 완화
                trusted_domains = ['google', 'netflix', 'naver', 'amazon', 'microsoft', 'akamai', 'apple']
                if any(t in domain for t in trusted_domains):
                    boost -= 0.04
                # 내부링크 충분한 경우
                if row['ratio_intHyperlinks'] > 0.5 and row['nb_hyperlinks'] > 5:
                    boost -= 0.03
                # 긴 host지만 CDN 패턴 포함 시 보정
                if row['length_hostname'] > 30 and any(x in domain for x in ['elb.amazonaws.com', 'akadns.net']):
                    boost -= 0.03

                # 제한 조정
                boost = min(max(boost, -0.08), 0.25)
                prob = min(max(raw_prob + boost, 0.0), 1.0)
                pred_label = int(prob >= threshold)  # threshold는 여전히 0.65

                if pred_label == 1 :
            
                    result_flag = True
                
                else :

                    result_flag = False

                self.module_run = True
                self.module_error = None            
                self.module_result_flag = result_flag
                self.module_result_data["reason"] = f"Probability of Result : {prob:.2%}"
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

        print("How to Use : python3 ai.py < URL >")

        sys.exit(1)
    
    input_url = sys.argv[1]

    module_instance = Ai(input_url)
    
    module_instance.scan()
