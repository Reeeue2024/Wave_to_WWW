# [ Core - DB ] Script : Get Data

import os
import requests
from urllib.parse import urlparse
import tldextract

# [ White List ] Get from ( Day By Day ) : "https://tranco-list.eu/api/list/latest"
TRANCO_ID = "PN43J"

BASE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
BLACK_LIST_DIRECTORY = os.path.join(BASE_DIRECTORY, "..", "db_data", "black_list")
WHITE_LIST_DIRECTORY = os.path.join(BASE_DIRECTORY, "..", "db_data", "white_list")

os.makedirs(BLACK_LIST_DIRECTORY, exist_ok=True)
os.makedirs(WHITE_LIST_DIRECTORY, exist_ok=True)

GET_BLACK_LIST_DATA_LIST = [
    {
        "url" : "https://raw.githubusercontent.com/Phishing-Database/Phishing.Database/refs/heads/master/phishing-links-ACTIVE.txt",
        "link_file_name" : "black_list_link_active.txt",
        "domain_suffix_file_name" : "black_list_domain_suffix_active.txt",
        "brand_file_name" : "black_list_brand_active.txt",
    },
    {
        "url" : "https://raw.githubusercontent.com/Phishing-Database/Phishing.Database/refs/heads/master/phishing-links-INACTIVE.txt",
        "link_file_name" : "black_list_link_inactive.txt",
        "domain_suffix_file_name" : "black_list_domain_suffix_inactive.txt",
        "brand_file_name" : "black_list_brand_inactive.txt",
    },
    {
        "url" : "https://raw.githubusercontent.com/Phishing-Database/Phishing.Database/refs/heads/master/phishing-links-NEW-today.txt",
        "link_file_name" : "black_list_link_today.txt",
        "domain_suffix_file_name" : "black_list_domain_suffix_today.txt",
        "brand_file_name" : "black_list_brand_today.txt",
    },
]
GET_WHITE_LIST_DATA_LIST = [
    {
        "url" : f"https://tranco-list.eu/download/{TRANCO_ID}/TXT",
        "link_file_name" : "white_list_link.txt",
        "domain_suffix_file_name" : "white_list_domain_suffix.txt",
        "brand_file_name" : "white_list_brand.txt",
    },
]

# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #
# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #
# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #
# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #
# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #
# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #
# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #
# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #
# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #
# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #

def extract_data_black_list(url_list) :
    domain_suffix_set = set()
    brand_set = set()

    for url in url_list :
        url = url.strip()

        if not url.startswith("http://") and not url.startswith("https://") :
            url = "http://" + url

        try :
            extract_result = tldextract.extract(url)
            if extract_result.domain and extract_result.suffix :
                domain_suffix = f"{extract_result.domain}.{extract_result.suffix}"
                brand = extract_result.domain

                domain_suffix_set.add(domain_suffix)
                brand_set.add(brand)
        except :
            continue

    return sorted(domain_suffix_set), sorted(brand_set)

def get_data_black_list() :
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(" [ Black List ] Get Data ...")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

    # [ 1. ] Black List
    for item in GET_BLACK_LIST_DATA_LIST :
        print(f"[ + ] Work : {item['url']}")

        response = requests.get(item["url"])
        response.raise_for_status()
        url_list = response.text.strip().splitlines()

        # [ 1-1. ] Black List - Link File
        link_file_path = os.path.join(BLACK_LIST_DIRECTORY, item["link_file_name"])
        with open(link_file_path, "w", encoding="utf-8") as file :
            file.write("\n".join(url_list))
        print(f"    => Save Link File ( Path ) : {item['link_file_name']}")

        domain_suffix_list, brand_list = extract_data_black_list(url_list)

        # [ 1-2. ] Black List - Domain + Suffix File
        domain_suffix_file_path = os.path.join(BLACK_LIST_DIRECTORY, item["domain_suffix_file_name"])
        with open(domain_suffix_file_path, "w", encoding="utf-8") as file :
            file.write("\n".join(domain_suffix_list))
        print(f"    => Save Domain + Suffix File ( Path ) : {item['domain_suffix_file_name']}")

        # [ 1-3. ] Black List - Brand File
        brand_file_path = os.path.join(BLACK_LIST_DIRECTORY, item["brand_file_name"])
        with open(brand_file_path, "w", encoding="utf-8") as file :
            file.write("\n".join(brand_list))
        print(f"    => Save Brand File ( Path ) : {item['brand_file_name']}")

# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #
# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #
# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #
# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #
# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #
# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #
# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #
# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #
# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #
# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #

def extract_data_white_list(domain_suffix_list) :
    brand_set = set()

    for domain_suffix in domain_suffix_list :
        domain_suffix = domain_suffix.strip()

        if not domain_suffix :
            continue

        try :
            extract_result = tldextract.extract(domain_suffix)

            if extract_result.domain and extract_result.suffix :
                brand = extract_result.domain
                brand_set.add(brand)
        except :
            continue

    return sorted(brand_set)

def get_data_white_list() :
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(" [ White List ] Get Data ...")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

    # [ 2. ] White List
    for item in GET_WHITE_LIST_DATA_LIST :
        domain_suffix_list = []

        print(f"[ + ] Work : {item['url']}")

        response = requests.get(item["url"])
        response.raise_for_status()
        csv_file = response.text.strip().splitlines()

        for line in csv_file :
            line = line.strip()

            if not line or "," not in line :
                continue

            try :
                domain_suffix = (line.split(",", 1))[1]
                domain_suffix_list.append(domain_suffix.strip())
            except :
                continue

        # print(f"[ DEBUG ] \"domain_suffix_list\"")
        # print(f"Number of \"\domain_suffix_list\" : {len(domain_suffix_list)}")
        # print(f"{domain_suffix_list}")

        # [ 2-1. ] White List - Domain + Suffix File
        domain_suffix_file_path = os.path.join(WHITE_LIST_DIRECTORY, item["domain_suffix_file_name"])
        with open(domain_suffix_file_path, "w", encoding="utf-8") as file :
            file.write("\n".join(domain_suffix_list))
        print(f"    => Save Domain + Suffix File ( Path ) : {item['domain_suffix_file_name']}")

        brand_list = extract_data_white_list(domain_suffix_list)

        # [ 2-2. ] White List - Brand File
        brand_file_path = os.path.join(WHITE_LIST_DIRECTORY, item["brand_file_name"])
        with open(brand_file_path, "w", encoding="utf-8") as file :
            file.write("\n".join(brand_list))
        print(f"    => Save Brand File ( Path ) : {item['brand_file_name']}")

# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #
# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #
# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #
# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #
# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #
# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #
# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #
# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #
# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #
# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #

if __name__ == "__main__":
    get_data_black_list()
    get_data_white_list()

    print()
