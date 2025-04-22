# [ Script ] Create File : White List

import os
import csv

input_file_path_list = [
    "top-1m.csv",
]

"""
Get "_url.txt" File from ".csv" File
"""
def get_url_txt_from_csv(csv_path) :
    output_file_path = "white_list_" + os.path.splitext(csv_path)[0] + "_url.txt"

    with open(csv_path, newline='') as csvfile, open(output_file_path, 'w') as txtfile :
        reader = csv.reader(csvfile)

        for row in reader :

            if len(row) >= 2 :

                domain = row[1].strip()
                url = f"https://{domain}"
                txtfile.write(url + "\n")

    print(f"[ DEBUG ] \"_url.txt\" File : {output_file_path}")

    return output_file_path

"""
Get "_domain.txt" File from ".csv" File
"""
def get_hostname_txt_from_csv(csv_path) :
    output_file_path = "white_list_" + os.path.splitext(csv_path)[0] + "_domain.txt"

    with open(csv_path, newline='') as csvfile, open(output_file_path, 'w') as txtfile :
        reader = csv.reader(csvfile)

        for row in reader :

            if len(row) >= 2 :

                domain = row[1].strip()
                txtfile.write(domain + "\n")

    print(f"[ DEBUG ] \"_domain.txt\" File : {output_file_path}")

    return output_file_path

"""
Get "_brand.txt" File from ".csv" File
"""
def get_brand_txt_from_csv(csv_path) :
    output_file_path = "white_list_" + os.path.splitext(csv_path)[0] + "_brand.txt"

    with open(csv_path, newline='') as csvfile, open(output_file_path, 'w') as txtfile :
        reader = csv.reader(csvfile)

        for row in reader :

            if len(row) >= 2 :

                domain = row[1].strip()

                # To-Do
                brand = ""

                txtfile.write(brand + "\n")

    print(f"[ DEBUG ] \"_brand.txt\" File : {output_file_path}")

    return output_file_path

"""
Main
"""
if __name__ == "__main__" :    
    for index, input_file_path in enumerate(input_file_path_list, 1) :
        get_url_txt_from_csv(input_file_path)
        get_hostname_txt_from_csv(input_file_path)
        get_brand_txt_from_csv(input_file_path)
