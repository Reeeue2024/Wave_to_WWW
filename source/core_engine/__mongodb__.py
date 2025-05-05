# [ Core ] Kernel - Kernel Resource - ( MongoDB ) : __mongodb__.py

from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

load_dotenv()

uri = os.getenv("MONGODB_URI")
client = MongoClient(uri, server_api = ServerApi("1"))
db = client["kernel"]

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

def insert_black_list_url() :
    data = [
        { "url" : "http://google.com" },
        { "url" : "http://apple.com" },
    ]

    db["black_list_url"].delete_many({})
    db["black_list_url"].insert_many(data)
    
    print(f"[ + ] \"black_list_url\" : {len(data)}")

# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #
# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #

def insert_black_list_domain_suffix() :
    data = [
        { "domain_suffix" : "google.com" },
        { "domain_suffix" : "apple.com" },
    ]

    db["black_list_domain_suffix"].delete_many({})
    db["black_list_domain_suffix"].insert_many(data)

    print(f"[ + ] \"black_list_domain_suffix\" : {len(data)}")

# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #
# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #

def insert_black_list_brand() :
    data = [
        { "brand" : "google" },
        { "brand" : "apple" },
    ]

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
    data = [
        { "domain_suffix" : "google.com" },
        { "domain_suffix" : "apple.com" },
        { "domain_suffix" : "microsoft.com" },
        { "domain_suffix" : "paypal.com" },
        { "domain_suffix" : "naver.com" },
        { "domain_suffix" : "kakao.com" },
    ]

    db["white_list_domain_suffix"].delete_many({})
    db["white_list_domain_suffix"].insert_many(data)

    print(f"[ + ] \"white_list_domain_suffix\" : {len(data)}")

# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #
# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #

def insert_white_list_brand() :
    data = [
        { "brand" : "google" },
        { "brand" : "apple" },
        { "brand" : "microsoft" },
        { "brand" : "paypal" },
        { "brand" : "naver" },
        { "brand" : "kakao" },
    ]

    db["white_list_brand"].delete_many({})
    db["white_list_brand"].insert_many(data)
    
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

def insert_tiny_domain_list() :
    data = [
        { "tiny_domain" : domain } for domain in [
            "bit.ly", "goo.gl", "t.co", "ow.ly", "tinyurl.com",
            "is.gd", "buff.ly", "adf.ly", "bit.do", "mcaf.ee",
            "rebrand.ly", "su.pr", "shorte.st", "cli.gs", "v.gd",
            "url.kr", "buly.kr", "alie.kr", "link24.kr", "lrl.kr",
            "tr.ee", "t.ly", "t.me", "rb.gy", "shrtco.de",
            "chilp.it", "cutt.ly", "vvd.bz", "IRI.MY", "LINC.kr",
            "abit.ly", "chzzk.me", "flic.kr", "glol.in", "gourl.kr",
            "han.gl", "juso.ga", "muz.so", "na.to", "site.naver.com",
            "t2m.kr", "tny.kr", "tuney.kr", "twr.kr", "ual.kr",
            "url.sg", "vo.la", "wo.to", "yao.ng", "zed.kr",
            "zxcv.be",
        ]
    ]

    db["tiny_domain_list"].delete_many({})
    db["tiny_domain_list"].insert_many(data)

    print(f"[ + ] \"tiny_domain_list\" : {len(data)}")

# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #
# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #

def insert_ssl_free_ca_list() :
    data = [
        { "free_ca" : domain } for domain in [
            "Let's Encrypt", "ZeroSSL", "Buypass",
            "SSL For Free", "FreeSSL", "Basic DV",
            "GeoTrust DV", "cPanel Inc", "Sectigo (DV Only)", "RapidSSL",
        ]
    ]

    db["ssl_free_ca_list"].delete_many({})
    db["ssl_free_ca_list"].insert_many(data)

    print(f"[ + ] \"ssl_free_ca_list\" : {len(data)}")

# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #
# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #

def insert_ssl_low_trust_ca_list() :
    data = [
        { "low_trust_ca" : domain } for domain in [
            "StartCom", "WoSign", "WoTrus", "TrustAsia", "CNNIC",
            "Symantec", "Unizeto", "Comodo", "SwissSign",
            "Certum", "DigiNotar", "PKIoverheid",
        ]
    ]

    db["ssl_low_trust_ca_list"].delete_many({})
    db["ssl_low_trust_ca_list"].insert_many(data)

    print(f"[ + ] \"ssl_low_trust_ca_list\" : {len(data)}")

# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #
# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #

def insert_free_tld_list() :
    data = [
        { "free_tld" : domain } for domain in [
            "tk", "ml", "ga", "cf", "gq", "xyz",
        ]
    ]

    db["free_tld_list"].delete_many({})
    db["free_tld_list"].insert_many(data)

    print(f"[ + ] \"free_tld_list\" : {len(data)}")

# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #
# = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = #

def insert_country_tld_list() :
    data = [
        { "country_tld" : domain } for domain in [
            "af", "ax", "al", "dz", "as", "ad", "ao", "ai", "aq", "ag", "ar", "am", "aw", "ac", "au", "at", "az", "bs", "bh", "bd", "bb", "eu", "by", "be", "bz", "bj", "bm", "bt", "bo", "bq", "an", "nl", "ba", "bw", "bv", "br", "io", "vg", "bn", "bg", "bf", "mm", "bi", "kh", "cm", "ca", "cv", "ca", "ky", "cf", "td", "cl", "cn", "cx", "cc", "co", "km", "cd", "cg", "ck", "cr", "ci", "hr", "cu", "cw", "cy", "cz", "dk", "dj", "dm", "do", "tl", "tp", "ec", "eg", "sv", "gq", "er", "ee", "et", "eu", "fk", "fo", "fm", "fj", "fi", "fr", "gf", "pf", "tf", "ga", "ga", "gm", "ps", "ge", "de", "gh", "gi", "gr", "gl", "gd", "gp", "gu", "gt", "gg", "gn", "gw", "gy", "ht", "hm", "hn", "hk", "hu", "is", "in", "id", "ir", "iq", "ie", "im", "il", "it", "jm", "jp", "je", "jo", "kz", "ke", "ki", "kw", "kg", "la", "lv", "lb", "ls", "lr", "ly", "li", "lt", "lu", "mo", "mk", "mg", "mw", "my", "mv", "ml", "mt", "mh", "mq", "mr", "mu", "yt", "mx", "md", "mc", "mn", "me", "ms", "ma", "mz", "mm", "na", "nr", "np", "nl", "nc", "nz", "ni", "ne", "ng", "nu", "nf", "nc", "tr", "kp", "mp", "no", "om", "pk", "pw", "ps", "pa", "pg", "py", "pe", "ph", "pn", "pl", "pt", "pr", "qa", "ro", "ru", "rw", "re", "bq", "an", "bl", "gp", "fr", "sh", "kn", "lc", "mf", "gp", "fr", "pm", "vc", "ws", "sm", "st", "sa", "sn", "rs", "sc", "sl", "sg", "bq", "an", "nl", "sx", "an", "sk", "si", "sb", "so", "so", "za", "gs", "kr", "ss", "es", "lk", "sd", "sr", "sj", "sz", "se", "ch", "sy", "tw", "tj", "tz", "th", "tg", "tk", "to", "tt", "tn", "tr", "tm", "tc", "tv", "ug", "ua", "ae", "uk", "us", "vi", "uy", "uz", "vu", "va", "ve", "vn", "wf", "eh", "ma", "ye", "zm", "zw",
        ]
    ]

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

insert_black_list_url()
insert_black_list_domain_suffix()
insert_black_list_brand()

insert_white_list_url()
insert_white_list_domain_suffix()
insert_white_list_brand()

insert_tiny_domain_list()
insert_ssl_free_ca_list()
insert_ssl_low_trust_ca_list()
insert_free_tld_list()
insert_country_tld_list()
