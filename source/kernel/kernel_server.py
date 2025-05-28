# [ Kernel ] Kernel Server : kernel_server.py

from kernel.kernel_service import KernelService
from kernel.kernel_resource import kernel_resource_instance

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title = "[ Kernel ] Kernel Server")

@app.on_event("startup")
def startup_event() :
    kernel_resource_instance.load_resource() # Load Kernel Resources

class KernelRequest(BaseModel) :
    input_url : str
    engine_type : str

@app.post("/detect/url")
def kernel_request_response(request : KernelRequest) :
    kernel_service_instance = KernelService()

    kernel_result = kernel_service_instance.run_kernel(request.input_url, request.engine_type) # Receive Request from Server
    
    return kernel_result # Send Response to Server
