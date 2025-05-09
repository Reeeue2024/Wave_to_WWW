# [ Core ] Kernel - Kernel Service : main.py

from kernel_service import KernelService

if __name__ == "__main__" :

    request_payload = {
        "input_url": "https://google.com",
        "engine_type": "full",
    }

    kernel_service = KernelService()

    kernel_result = kernel_service.run_kernel(request_payload["input_url"], request_payload["engine_type"])

    print()
    print("* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * ")
    print(" [ Kernel Service ]")
    print(f"   [ * ] Input URL : {request_payload["input_url"]}")
    print(f"   [ * ] Engine Type : {request_payload["engine_type"]}")
    print(f"   [ * ] Kernel Result : {kernel_result}")
    print("* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * ")
    print()
