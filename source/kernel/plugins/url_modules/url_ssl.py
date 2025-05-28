# [ Kernel ] Module - URL : url_ssl.py

from kernel.plugins._base_module import BaseModule

import sys
import ssl
import socket
from urllib.parse import urlparse
from cryptography import x509
from cryptography.hazmat.backends import default_backend
import certifi
import asyncio

class UrlSsl(BaseModule) :
    def __init__(self, input_url) :
        super().__init__(input_url)

        self.ssl_free_ca_list = self.get_kernel_resource("ssl_free_ca_list")
        self.ssl_not_trust_ca_list = self.get_kernel_resource("ssl_not_trust_ca_list")

        self.certificate = None

    """
    IN : 
    OUT : 
    """
    def get_certificate(self) :
        # import time

        # time.sleep(15)

        try :
            urlparse_result = urlparse(self.input_url)
            hostname = urlparse_result.hostname

            ssl_context = ssl.create_default_context(cafile = certifi.where())
            ssl_socket = ssl_context.wrap_socket(socket.socket(socket.AF_INET), server_hostname = hostname)
            ssl_socket.settimeout(5)
            ssl_socket.connect((hostname, 443))

            certificate_der = ssl_socket.getpeercert(binary_form = True)
            certificate = x509.load_der_x509_certificate(certificate_der, default_backend())

            return certificate

        except Exception as e :
            return None

    """
    IN : 
    OUT : 
    """
    def scan_free_ca(self) :
        issuer_string = self.certificate.issuer.rfc4514_string()

        # print(f"[ DEBUG ] Issuer ( String ) : {issuer_string}")
        
        for ssl_free_ca_element in self.ssl_free_ca_list :

            ssl_free_ca = ssl_free_ca_element.get("ssl_free_ca")

            if ssl_free_ca and ssl_free_ca in issuer_string :

                return True, ssl_free_ca
        
        return False, None

    """
    IN : 
    OUT : 
    """
    def scan_not_trust_ca(self) :
        issuer_string = self.certificate.issuer.rfc4514_string()

        # print(f"[ DEBUG ] Issuer ( String ) : {issuer_string}")

        for not_trust_ca_element in self.ssl_not_trust_ca_list :

            not_trust_ca = not_trust_ca_element.get("not_trust_ca")

            if not_trust_ca and not_trust_ca in issuer_string :

                return True, not_trust_ca
        
        return False, None

    """
    IN : 
    OUT : 
    """
    async def scan(self) :        
        loop = asyncio.get_running_loop()

        try :
            self.certificate = await asyncio.wait_for(loop.run_in_executor(None, self.get_certificate), timeout = self.module_time_out)

            # print("[ DEBUG ] \"Not\" Time Out.")

        except asyncio.TimeoutError :
            # print("[ DEBUG ] Time Out.")

            self.module_run = False
            self.module_error = "[ ERROR : Time Out ] Fail to Get SSL Certificate."
            self.module_result_flag = False
            self.module_result_data = None

            self.create_module_result()
            
            # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

            return self.module_result_dictionary

        # self.certificate = self.get_certificate()

        # Run Fail Case #1
        if not self.certificate :

            self.module_run = False
            self.module_error = "[ ERROR ] Fail to Get SSL Certificate."
            self.module_result_flag = False
            self.module_result_data = None

            self.create_module_result()

            return self.module_result_dictionary

        # [ 1. ] Free CA => ( Run : True ) + ( Scan : True )
        free_ca_flag, free_ca_data = self.scan_free_ca()

        if free_ca_flag :

            self.module_run = True
            self.module_error = None
            self.module_result_flag = True
            self.module_result_data["reason"] = "Use Free CA in SSL Certificate."
            self.module_result_data["reason_data"] = free_ca_data

            self.create_module_result()

            return self.module_result_dictionary

        # [ 2. ] Not Trust CA => ( Run : True ) + ( Scan : True )
        not_trust_flag, not_trust_data = self.scan_not_trust_ca()

        if not_trust_flag :

            self.module_run = True
            self.module_error = None
            self.module_result_flag = True
            self.module_result_data["reason"] = "Use Not Trust CA in SSL Certificate."
            self.module_result_data["reason_data"] = not_trust_data

            self.create_module_result()

            return self.module_result_dictionary

        # ( Run : True ) + ( Scan : False )
        self.module_run = True
        self.module_error = None
        self.module_result_flag = False
        self.module_result_data["reason"] = "Not Use Free CA / Not Trust CA in SSL Certificate."
        self.module_result_data["reason_data"] = None
        
        self.create_module_result()

        # print(f"[ DEBUG ] Module Result Dictionary : {self.module_result_dictionary}")

        return self.module_result_dictionary

# Module Main
if __name__ == "__main__" :

    # Input : URL
    if len(sys.argv) != 2 :

        print("How to Use : python3 url_ssl.py < URL >")

        sys.exit(1)
    
    input_url = sys.argv[1]

    module_instance = UrlSsl(input_url)
    
    module_instance.scan()
