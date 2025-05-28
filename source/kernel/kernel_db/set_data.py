# [ Kernel ] Data - Script : set_data.py

from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

ENV_DIRECTORY_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ENV_FILE_PATH = os.path.join(ENV_DIRECTORY_PATH, ".env")

load_dotenv(ENV_FILE_PATH)

uri = os.getenv("MONGO_URI")
client = MongoClient(uri, server_api = ServerApi("1"))
db = client["kernel"]

# print(f"[ DEBUG ] ENV_FILE_PATH : {ENV_FILE_PATH}")

BASE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
BLACK_LIST_DIRECTORY = os.path.join(BASE_DIRECTORY, "data_black_list")
WHITE_LIST_DIRECTORY = os.path.join(BASE_DIRECTORY, "data_black_list")
ETC_DIRECTORY = os.path.join(BASE_DIRECTORY, "data_etc")

# [ Black List ] File List
BLACK_LIST_LINK_FILE_LIST = [
    "black_list_link_active.txt",
    "black_list_link_inactive.txt",
    "black_list_link_today.txt",
]
BLACK_LIST_DOMAIN_SUFFIX_FILE_LIST = [
    "black_list_domain_suffix_active.txt",
    "black_list_domain_suffix_inactive.txt",
    "black_list_domain_suffix_today.txt",
]
BLACK_LIST_BRAND_FILE_LIST = [
    "black_list_brand_active.txt",
    "black_list_brand_inactive.txt",
    "black_list_brand_today.txt",
]

# [ White List ] File List
WHITE_LIST_DOMAIN_SUFFIX_FILE_LIST = [
    "white_list_domain_suffix.txt",
]
WHITE_LIST_BRAND_FILE_LIST = [
    "white_list_brand.txt",
]

# [ ETC ] File List

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

def insert_black_list_link() :
    link_set = set()

    for black_list_link_file in BLACK_LIST_LINK_FILE_LIST :

        file_path = os.path.join(BLACK_LIST_DIRECTORY, black_list_link_file)

        if not os.path.exists(file_path) :

            print(f"[ ! ] Fail to Get File : {file_path}")

            continue

        with open(file_path, "r", encoding="utf-8") as file :

            for line in file :

                line = line.strip()

                if line :

                    link_set.add(line)

    data = [{ "url" : url } for url in link_set]

    db["black_list_url"].delete_many({})
    db["black_list_url"].insert_many(data)

    print(f"[ + ] \"black_list_url\" : {len(data)}")

# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #
# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #

def insert_black_list_domain_suffix() :
    domain_suffix_set = set()

    for black_list_domain_suffix_file in BLACK_LIST_DOMAIN_SUFFIX_FILE_LIST :

        file_path = os.path.join(BLACK_LIST_DIRECTORY, black_list_domain_suffix_file)

        if not os.path.exists(file_path) :

            print(f"[ ! ] Fail to Get File : {file_path}")

            continue

        with open(file_path, "r", encoding="utf-8") as file :

            for line in file :

                line = line.strip()

                if line :

                    domain_suffix_set.add(line)

    data = [{ "domain_suffix" : domain_suffix } for domain_suffix in domain_suffix_set]

    db["black_list_domain_suffix"].delete_many({})
    db["black_list_domain_suffix"].insert_many(data)

    print(f"[ + ] \"black_list_domain_suffix\" : {len(data)}")

# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #
# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #

def insert_black_list_brand() :
    brand_set = set()

    for black_list_brand_file in BLACK_LIST_BRAND_FILE_LIST :

        file_path = os.path.join(BLACK_LIST_DIRECTORY, black_list_brand_file)

        if not os.path.exists(file_path) :

            print(f"[ ! ] Fail to Get File : {file_path}")

            continue

        with open(file_path, "r", encoding="utf-8") as file :

            for line in file :

                line = line.strip()

                if line :

                    brand_set.add(line)

    data = [{ "brand" : brand } for brand in brand_set]

    db["black_list_brand"].delete_many({})
    db["black_list_brand"].insert_many(data)

    print(f"[ + ] \"black_list_brand\" : {len(data)}")

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

def insert_white_list_url() :
    data = [
        { "url" : "https://google.com" },
        { "url" : "https://apple.com" },
        { "url" : "https://microsoft.com" },
        { "url" : "https://paypal.com" },
        { "url" : "https://naver.com" },
        { "url" : "https://kako.com" },
    ]

    db["white_list_url"].delete_many({})
    db["white_list_url"].insert_many(data)
    
    print(f"[ + ] \"white_list_url\" : {len(data)}")

# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #
# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #

def insert_white_list_domain_suffix() :
    domain_suffix_set = set()

    for black_list_domain_suffix_file in WHITE_LIST_DOMAIN_SUFFIX_FILE_LIST :

        file_path = os.path.join(WHITE_LIST_DIRECTORY, black_list_domain_suffix_file)

        if not os.path.exists(file_path) :

            print(f"[ ! ] Fail to Get File : {file_path}")

            continue

        with open(file_path, "r", encoding="utf-8") as file :

            for line in file :

                line = line.strip()

                if line :

                    domain_suffix_set.add(line)

    db["white_list_domain_suffix"].delete_many({})

    domain_suffix_list = sorted(domain_suffix_set)

    part_size = 100000

    domain_suffix_list_part = domain_suffix_list[0 : part_size]

    data = [{ "domain_suffix" : domain_suffix } for domain_suffix in domain_suffix_list_part]

    db["white_list_domain_suffix"].insert_many(data)

    # batch_size = 1000000

    # domain_suffix_count = len(domain_suffix_list)

    # for i in range(0, domain_suffix_count, batch_size) :

    #     batch = domain_suffix_list[i : i + batch_size]

    #     data = [{ "domain_suffix": domain_suffix } for domain_suffix in batch]

    #     db["white_list_domain_suffix"].insert_many(data)

    #     print(f"[ DEBUG ] Success to Insert : {i + len(batch)} / {domain_suffix_count}")

    print(f"[ + ] \"white_list_domain_suffix\" : {len(data)}")

# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #
# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #

def insert_white_list_brand() :
    brand_set = set()

    for black_list_brand_file in WHITE_LIST_BRAND_FILE_LIST :

        file_path = os.path.join(WHITE_LIST_DIRECTORY, black_list_brand_file)

        if not os.path.exists(file_path) :

            print(f"[ ! ] Fail to Get File : {file_path}")

            continue

        with open(file_path, "r", encoding="utf-8") as file :

            for line in file :

                line = line.strip()

                if line :

                    brand_set.add(line)

    db["white_list_brand"].delete_many({})

    brand_list = sorted(brand_set)

    part_size = 100000

    brand_list_part = brand_list[0 : part_size]

    data = [{ "brand" : brand } for brand in brand_list_part]

    db["white_list_brand"].insert_many(data)

    # batch_size = 1000000

    # brand_list_count = len(brand_list)

    # for i in range(0, brand_list_count, batch_size) :

    #     batch = brand_list[i : i + batch_size]

    #     data = [{ "brand" : brand } for brand in batch]

    #     db["white_list_brand"].insert_many(data)
        
    #     print(f"[ DEBUG ] Success to Insert : {i + len(batch)} / {brand_list_count}")
        
    print(f"[ + ] \"white_list_brand\" : {len(data)}")

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

def insert_short_domain_list() :
    short_domain_set = set()

    file_path = os.path.join(ETC_DIRECTORY, "etc_short_domain.txt")

    if not os.path.exists(file_path) :

        print(f"[ ! ] Fail to Get File : {file_path}")

        return

    with open(file_path, "r", encoding="utf-8") as file :

        for line in file :

            line = line.strip()

            if line :

                short_domain_set.add(line)
    
    data = [{ "short_domain" : short_domain } for short_domain in short_domain_set]

    db["short_domain_list"].delete_many({})
    db["short_domain_list"].insert_many(data)

    print(f"[ + ] \"short_domain_list\" : {len(data)}")

# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #
# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #

def insert_ssl_free_ca_list() :
    ssl_free_ca_set = set()

    file_path = os.path.join(ETC_DIRECTORY, "etc_ssl_free_ca.txt")

    if not os.path.exists(file_path) :

        print(f"[ ! ] Fail to Get File : {file_path}")

        return

    with open(file_path, "r", encoding="utf-8") as file :

        for line in file :

            line = line.strip()

            if line :

                ssl_free_ca_set.add(line)
    
    data = [{ "ssl_free_ca" : ssl_free_ca } for ssl_free_ca in ssl_free_ca_set]

    db["ssl_free_ca_list"].delete_many({})
    db["ssl_free_ca_list"].insert_many(data)

    print(f"[ + ] \"ssl_free_ca_list\" : {len(data)}")

# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #
# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #

def insert_ssl_not_trust_ca_list() :
    ssl_not_trust_ca_set = set()

    file_path = os.path.join(ETC_DIRECTORY, "etc_ssl_not_trust_ca.txt")

    if not os.path.exists(file_path) :

        print(f"[ ! ] Fail to Get File : {file_path}")

        return

    with open(file_path, "r", encoding="utf-8") as file :

        for line in file :

            line = line.strip()

            if line :

                ssl_not_trust_ca_set.add(line)
    
    data = [{ "ssl_not_trust_ca" : ssl_not_trust_ca } for ssl_not_trust_ca in ssl_not_trust_ca_set]

    db["ssl_not_trust_ca_list"].delete_many({})
    db["ssl_not_trust_ca_list"].insert_many(data)

    print(f"[ + ] \"ssl_not_trust_ca_list\" : {len(data)}")

# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #
# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #

def insert_free_tld_list() :
    free_tld_set = set()

    file_path = os.path.join(ETC_DIRECTORY, "etc_free_tld.txt")

    if not os.path.exists(file_path) :

        print(f"[ ! ] Fail to Get File : {file_path}")

        return

    with open(file_path, "r", encoding="utf-8") as file :

        for line in file :

            line = line.strip()

            if line :

                free_tld_set.add(line)
    
    data = [{ "free_tld" : free_tld } for free_tld in free_tld_set]

    db["free_tld_list"].delete_many({})
    db["free_tld_list"].insert_many(data)

    print(f"[ + ] \"free_tld_list\" : {len(data)}")

# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #
# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #

def insert_country_tld_list() :
    country_tld_set = set()

    file_path = os.path.join(ETC_DIRECTORY, "etc_country_tld.txt")

    if not os.path.exists(file_path) :

        print(f"[ ! ] Fail to Get File : {file_path}")

        return

    with open(file_path, "r", encoding="utf-8") as file :

        for line in file :

            line = line.strip()

            if line :

                country_tld_set.add(line)
    
    data = [{ "country_tld" : country_tld } for country_tld in country_tld_set]

    db["country_tld_list"].delete_many({})
    db["country_tld_list"].insert_many(data)

    print(f"[ + ] \"country_tld_list\" : {len(data)}")

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

# insert_black_list_link()
# insert_black_list_domain_suffix()
# insert_black_list_brand()

print(f"[ DEBUG ] Count of \"black_list_url\" : {db['black_list_url'].count_documents({})}")
print(f"[ DEBUG ] Count of \"black_list_domain_suffix\" : {db['black_list_domain_suffix'].count_documents({})}")
print(f"[ DEBUG ] Count of \"black_list_brand\" : {db['black_list_brand'].count_documents({})}")

# insert_white_list_url()
# insert_white_list_domain_suffix()
# insert_white_list_brand()

print(f"[ DEBUG ] Count of \"white_list_url\" : {db['white_list_url'].count_documents({})}")
print(f"[ DEBUG ] Count of \"white_list_domain_suffix\" : {db['white_list_domain_suffix'].count_documents({})}")
print(f"[ DEBUG ] Count of \"white_list_brand\" : {db['white_list_brand'].count_documents({})}")

insert_short_domain_list()
insert_ssl_free_ca_list()
insert_ssl_not_trust_ca_list()
insert_free_tld_list()
insert_country_tld_list()
