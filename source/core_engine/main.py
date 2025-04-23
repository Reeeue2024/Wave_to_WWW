# [ Core ] Kernel : main.py

from kernel import Kernel
import sys

if __name__ == "__main__" :
    if len(sys.argv) != 2 :
        print("How to Use : python3 main.py < URL >")
        sys.exit(1)

    input_url = sys.argv[1]

    kernel_instance = Kernel(input_url)

    result_flag = kernel_instance.start()

    print()
    print("* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * ")
    print(" [ Kernel ]")
    print(f"   [ * ] URL : {input_url}")
    if result_flag == True : 
        print(f"   [ * ] ⚠️ Suspicious")
    else :
        print(f"   [ * ] ✅ OK")
    print("* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * ")
    print()
    