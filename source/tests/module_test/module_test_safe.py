# [ TEST ] Safe

import os
import csv
from urllib.parse import urlparse

db_url_list = [
    "module_test_data/top-1m.csv",
]

"""
Get ".txt" File from ".csv" File
"""
def get_txt_from_csv(csv_path):
    txt_path = os.path.splitext(csv_path)[0] + ".txt"

    with open(csv_path, newline='') as csvfile, open(txt_path, 'w') as txtfile :
        reader = csv.reader(csvfile)

        for row in reader :

            if len(row) >= 2 :

                domain = row[1].strip()
                url = f"https://{domain}"
                txtfile.write(url + "\n")

    # print(f"[ DEBUG ] \".txt\" File : {txt_path}")

    return txt_path

"""
Get URL Data from "Safe" Data File
"""
def get_url_data(file_path) :
    with open(file_path, "r") as file :
        return [line.strip() for line in file if line.strip()]

"""
Scan with Module
"""
def test(module_class, urls, data_file_index) :    
    print(f"\nNumber of URLs to TEST: {len(urls)}\n")

    results = []

    for index, url in enumerate(urls, 1) :
        # print(f"[ + ] [{index:04d}] {url}")

        try :
            module_instance = module_class(url)
            is_suspicious = module_instance.scan()  # Return Value : True / False
        except Exception as e :
            print(f"[ ERROR ] ? : {e}") # Keep Loop
            is_suspicious = False  # To-Do

        if is_suspicious :
            result = "Suspicious"
        else :
            result = "OK"

        hostname = urlparse(url).hostname or ""

        results.append({
            "result": result,
            "url": url,
            "hostname": hostname
        })

        # print(f"[ Result ] {result}")
        # print("-" * 60)

    result_csv = f"module_test_results/safe_result_{module_class}_{data_file_index}.csv"

    with open(result_csv, mode="w", newline='', encoding="utf-8") as f :
        writer = csv.DictWriter(f, fieldnames=["result", "url", "hostname"])
        writer.writeheader()
        writer.writerows(results)

    total = len(results)
    ok_count = sum(1 for result in results if result["result"] == "OK")
    suspicious_count = sum(1 for result in results if result["result"] == "Suspicious")

    print(f"\n[ ( TEST ) Result ]")
    print(f">>>> OK URLs / Total URLs : {ok_count} / {total}")
    print(f">>>> Suspicious URLs / Total URLs : {suspicious_count} / {total}")
    print(f">>>> ( % ) : {suspicious_count / total * 100}")

    print(f"\nSuccess of \"TEST\" => {result_csv}\n")

"""
Main
"""
if __name__ == "__main__" :
    from url_homograph import UrlHomograph # Example ( Url Modules - "url_homograph.py" )
    
    for index, data_file_path in enumerate(db_url_list, 1) :
        txt_file_path = get_txt_from_csv(data_file_path)

        print(f"[ # {index} ] TEST")
        print(f">>>> Data File : {txt_file_path}")

        urls = get_url_data(txt_file_path)
        
        test(UrlHomograph, urls, index)
