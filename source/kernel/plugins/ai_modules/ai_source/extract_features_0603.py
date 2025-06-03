# [ Kernel ] Module - AI : ai_url.py - extract_features.py

import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# feature 목록
updated_feature_names = [
    'length_url', 'length_hostname', 'ip', 'nb_dots', 'nb_qm', 'nb_eq', 'nb_slash',
    'nb_www', 'ratio_digits_url', 'ratio_digits_host', 'tld_in_subdomain', 'prefix_suffix',
    'shortest_word_host', 'longest_words_raw', 'longest_word_path', 'phish_hints',
    'nb_hyperlinks', 'ratio_intHyperlinks', 'empty_title', 'domain_in_title', 'domain_age',
    'google_index', 'page_rank', 'nb_hyperlinks.1', 'ratio_intHyperlinks.1', 'empty_title.1',
    'Favicon', 'Request_URL', 'URL_of_Anchor', 'Links_in_tags', 'SFH', 'Iframe'
]

# feature 추출 함수
def extract_features(url, threshold=0.7):
    parsed = urlparse(url)
    domain = parsed.netloc
    features = {}
    suspicious_reasons = []

    features['length_url'] = len(url)
    if features['length_url'] > 100:
        suspicious_reasons.append("length_url (long URL)")
    features['length_hostname'] = len(domain)
    if features['length_hostname'] > 30:
        suspicious_reasons.append("length_hostname (long hostname)")
    features['ip'] = 1 if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", domain) else 0
    if features['ip'] == 1:
        suspicious_reasons.append("ip (Uses IP address)")

    features['nb_dots'] = url.count('.')
    if features['nb_dots'] > 4:
        suspicious_reasons.append("nb_dots (Many '.' in URL)")
    features['nb_qm'] = url.count('?')
    if features['nb_qm'] > 2:
        suspicious_reasons.append("nb_qm (Many '?' characters)")

    features['nb_eq'] = url.count('=')
    if features['nb_eq'] > 2:
        suspicious_reasons.append("nb_eq (Many '=' characters)")

    features['nb_slash'] = url.count('/')
    if features['nb_slash'] > 10:
        suspicious_reasons.append("nb_slash (Many '/' characters)")

    features['nb_www'] = url.count('www')
    if features['nb_www'] > 1:
        suspicious_reasons.append("nb_www (Repeated 'www')")

    features['ratio_digits_url'] = sum(c.isdigit() for c in url) / len(url)
    if features['ratio_digits_url'] > 0.3:
        suspicious_reasons.append("ratio_digits_url (High digit ratio in URL)")

    features['ratio_digits_host'] = sum(c.isdigit() for c in domain) / len(domain) if domain else 0
    if features['ratio_digits_host'] > 0.3:
        suspicious_reasons.append("ratio_digits_host (High digit ratio in host)")

    features['tld_in_subdomain'] = 1 if re.search(r'\.(com|net|org|info)', parsed.netloc.split('.')[0]) else 0
    if features['tld_in_subdomain'] == 1:
        suspicious_reasons.append("tld_in_subdomain (TLD in subdomain)")

    features['prefix_suffix'] = 0 if any(x in domain for x in ['azure', 'google', 'amazonaws', 'akamai', 'cloudfront']) else (1 if '-' in domain else 0)
    if features['prefix_suffix'] == 1:
        suspicious_reasons.append("prefix_suffix (Contains hyphen)")

    words_host = domain.split('.')
    path = parsed.path.split('/')
    features['shortest_word_host'] = min((len(word) for word in words_host), default=0)
    if features['shortest_word_host'] < 3:
        suspicious_reasons.append("shortest_word_host (Very short word in host)")

    features['longest_words_raw'] = max((len(word) for word in url.split('/')), default=0)
    if features['longest_words_raw'] > 40:
        suspicious_reasons.append("longest_words_raw (Very long word in URL)")

    features['longest_word_path'] = max((len(word) for word in path), default=0)
    if features['longest_word_path'] > 30:
        suspicious_reasons.append("longest_word_path (Long word in path)")

    hints = ['secure', 'account', 'update', 'verify', 'login']
    features['phish_hints'] = 1 if any(h in url.lower() for h in hints) else 0
    if features['phish_hints'] == 1:
        suspicious_reasons.append("phish_hints (Contains phishing keywords)")

    # HTML 분석
    try:
        response = requests.get(url, timeout=1)
        soup = BeautifulSoup(response.content, 'html.parser')

        features['nb_hyperlinks'] = len(soup.find_all('a'))
        if features['nb_hyperlinks'] < 3:
            suspicious_reasons.append("nb_hyperlinks (Few hyperlinks)")

        internal = [a for a in soup.find_all('a') if domain in (a.get('href') or '')]
        features['ratio_intHyperlinks'] = len(internal) / len(soup.find_all('a')) if soup.find_all('a') else 0
        if features['ratio_intHyperlinks'] < 0.2:
            suspicious_reasons.append("ratio_intHyperlinks (Low internal link ratio)")

        features['empty_title'] = 1 if not (soup.title and soup.title.string and soup.title.string.strip()) else 0
        
        features['domain_in_title'] = 1 if soup.title and domain.split('.')[-2] in soup.title.string.lower() else 0
        if features['domain_in_title'] == 1:
            suspicious_reasons.append("domain_in_title (Domain name not in title)")

        favicon = soup.find("link", rel=lambda x: x and 'icon' in x.lower())
        if favicon and 'href' in favicon.attrs:
            href = favicon['href']
            features['Favicon'] = 1 if domain not in href else 0
        else:
            features['Favicon'] = 0
        if features['Favicon'] == 1:
            suspicious_reasons.append("Favicon (External domain favicon)")

        features['URL_of_Anchor'] = 1 if any(a.get('href', '').startswith('#') for a in soup.find_all('a')) else 0
        if features['URL_of_Anchor'] == 1:
            suspicious_reasons.append("URL_of_Anchor (External anchor link)")

        features['Links_in_tags'] = len(soup.find_all(['meta', 'script', 'link']))
        if features['Links_in_tags'] == 1:
            suspicious_reasons.append("Links_in_tags (Tags with external links)")

        features['SFH'] = 1 if soup.find('form', action="/") else 0
        if features['SFH'] == 1:
            suspicious_reasons.append("SFH (Suspicious form behavior)")

        features['Iframe'] = 1 if soup.find('iframe') else 0
        if features['Iframe'] == 1:
            suspicious_reasons.append("Iframe (Uses <iframe>)")

    except:
        for k in ['nb_hyperlinks', 'ratio_intHyperlinks', 'empty_title', 'domain_in_title',
                  'nb_hyperlinks.1', 'ratio_intHyperlinks.1', 'empty_title.1', 'Favicon',
                  'Request_URL', 'URL_of_Anchor', 'Links_in_tags', 'SFH', 'Iframe']:
            features[k] = 0

    # WHOIS (생략 또는 고정)
    features['domain_age'] = 0
    features['page_rank'] = 0
    features['google_index'] = 0
    features['Request_URL'] = 0 
    features['empty_title'] = 0
    features['empty_title.1'] = 0
    features['nb_hyperlinks.1'] = 0
    features['ratio_intHyperlinks.1'] = 0

    # 누락된 feature 보완
    for col in updated_feature_names:
        if col not in features:
            features[col] = 0
    
    return features, updated_feature_names, domain
