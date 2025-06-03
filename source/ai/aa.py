def analyze_url(url, threshold=0.65):
    from urllib.parse import urlparse
    import re
    import pandas as pd
    import requests
    from bs4 import BeautifulSoup
    import time

    parsed = urlparse(url)
    domain = parsed.netloc
    features = {}

    features['length_url'] = len(url)
    features['length_hostname'] = len(domain)
    features['ip'] = 1 if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", domain) else 0
    features['nb_dots'] = url.count('.')
    features['nb_qm'] = url.count('?')
    features['nb_eq'] = url.count('=')
    features['nb_slash'] = url.count('/')
    features['nb_www'] = url.count('www')
    features['ratio_digits_url'] = sum(c.isdigit() for c in url) / len(url)
    features['ratio_digits_host'] = sum(c.isdigit() for c in domain) / len(domain) if domain else 0
    features['tld_in_subdomain'] = 1 if re.search(r'\.(com|net|org|info)', parsed.netloc.split('.')[0]) else 0
    features['prefix_suffix'] = 0 if any(x in domain for x in ['azure', 'google', 'amazonaws', 'akamai', 'cloudfront']) else (1 if '-' in domain else 0)

    words_host = domain.split('.')
    path = parsed.path.split('/')
    features['shortest_word_host'] = min((len(word) for word in words_host), default=0)
    features['longest_words_raw'] = max((len(word) for word in url.split('/')), default=0)
    features['longest_word_path'] = max((len(word) for word in path), default=0)

    hints = ['secure', 'account', 'update', 'verify', 'login']
    features['phish_hints'] = 1 if any(h in url.lower() for h in hints) else 0

    # HTML 분석
    try:
        response = requests.get(url, timeout=2)
        soup = BeautifulSoup(response.content, 'html.parser')

        features['nb_hyperlinks'] = len(soup.find_all('a'))
        internal = [a for a in soup.find_all('a') if domain in (a.get('href') or '')]
        features['ratio_intHyperlinks'] = len(internal) / len(soup.find_all('a')) if soup.find_all('a') else 0
        features['empty_title'] = 1 if not (soup.title and soup.title.string and soup.title.string.strip()) else 0
        features['domain_in_title'] = 1 if soup.title and domain.split('.')[-2] in soup.title.string.lower() else 0

        features['nb_hyperlinks.1'] = features['nb_hyperlinks']
        features['ratio_intHyperlinks.1'] = features['ratio_intHyperlinks']

        favicon = soup.find("link", rel=lambda x: x and 'icon' in x.lower())
        if favicon and 'href' in favicon.attrs:
            href = favicon['href']
            features['Favicon'] = 1 if domain not in href else 0
        else:
            features['Favicon'] = 0

        features['URL_of_Anchor'] = 1 if any(a.get('href', '').startswith('#') for a in soup.find_all('a')) else 0
        features['Links_in_tags'] = len(soup.find_all(['meta', 'script', 'link']))
        features['SFH'] = 1 if soup.find('form', action="/") else 0
        features['Iframe'] = 1 if soup.find('iframe') else 0

    except:
        for k in ['nb_hyperlinks', 'ratio_intHyperlinks', 'empty_title', 'domain_in_title',
                  'nb_hyperlinks.1', 'ratio_intHyperlinks.1', 'empty_title.1', 'Favicon',
                  'Request_URL', 'URL_of_Anchor', 'Links_in_tags', 'SFH', 'Iframe']:
            features[k] = 0

    # WHOIS 및 고정 값
    features['domain_age'] = 0
    features['page_rank'] = 0
    features['google_index'] = 0
    features['Request_URL'] = 0 
    features['empty_title'] = 0
    features['empty_title.1'] = 0
    features['nb_hyperlinks.1'] = 0
    features['ratio_intHyperlinks.1'] = 0

    # 누락된 feature 채움
    for col in updated_feature_names:
        if col not in features:
            features[col] = 0

    features_df = pd.DataFrame([features])[updated_feature_names]

    # 모델 추론
    scaled_array = scaler.transform(features_df)
    raw_prob = model.predict_proba(scaled_array)[0][1]

    # 점수 보정
    row = features_df.iloc[0]
    boost = 0
    if row['phish_hints'] == 1: boost += 0.07
    if row['prefix_suffix'] == 1: boost += 0.03
    if row['ratio_digits_url'] > 0.3: boost += 0.03
    if row['domain_age'] < 0.2: boost += 0.04
    if row['Favicon'] == 1: boost += 0.03
    if boost > 0.15: boost = 0.15
    prob = min(raw_prob + boost, 1.0)
    pred_label = int(prob >= threshold)

    # 의심 특징 출력
    suspicious_features = []
    for col in features_df.columns:
        val = row[col]
        if col == 'ip' and val == 1:
            suspicious_features.append(f"{col} (Uses IP address)")
        elif col == 'nb_qm' and val > 2:
            suspicious_features.append(f"{col} (Many '?' characters)")
        elif col == 'nb_eq' and val > 2:
            suspicious_features.append(f"{col} (Many '=' characters)")
        elif col == 'nb_slash' and val > 10:       
            suspicious_features.append(f"{col} (Many '/' characters)")
        elif col == 'nb_www' and val > 1:
            suspicious_features.append(f"{col} (Repeated 'www')")
        elif col == 'ratio_digits_url' and val > 0.3:
            suspicious_features.append(f"{col} (High digit ratio in URL)")
        elif col == 'ratio_digits_host' and val > 0.3:
            suspicious_features.append(f"{col} (High digit ratio in host)")
        elif col == 'tld_in_subdomain' and val == 1:
            suspicious_features.append(f"{col} (TLD in subdomain)")                   
        elif col == 'prefix_suffix' and val == 1:
            suspicious_features.append(f"{col} (Contains hyphen)")
        elif col == 'shortest_word_host' and val < 3:
            suspicious_features.append(f"{col} (Very short word in host)")                
        elif col == 'longest_words_raw' and val > 40:
            suspicious_features.append(f"{col} (Very long word in URL)")
        elif col == 'longest_word_path' and val > 30:
            suspicious_features.append(f"{col} (Long word in path)")
        elif col == 'phish_hints' and val == 1:
            suspicious_features.append(f"{col} (Contains phishing keywords)")
        elif col == 'nb_hyperlinks' and val < 3:
            suspicious_features.append(f"{col} (Few hyperlinks)")
        elif col == 'ratio_intHyperlinks' and val < 0.2:
            suspicious_features.append(f"{col} (Low internal link ratio)")
        elif col == 'domain_in_title' and val == 1:
            suspicious_features.append(f"{col} (Domain name not in title)")            
        elif col == 'Favicon' and val == 1:
            suspicious_features.append(f"{col} (External domain favicon)")
        elif col == 'Request_URL' and val == 1:
            suspicious_features.append(f"{col} (External object request)")
        elif col == 'URL_of_Anchor' and val == 1:
            suspicious_features.append(f"{col} (External anchor link)")
        elif col == 'Links_in_tags' and val == 1:
            suspicious_features.append(f"{col} (Tags with external links)")
        elif col == 'SFH' and val == 1:
            suspicious_features.append(f"{col} (Suspicious form behavior)")
        elif col == 'Iframe' and val == 1:
            suspicious_features.append(f"{col} (Uses <iframe>)")

    # 출력
    print(f"\n🔍 URL: {url}")
    if pred_label == 1:
        print(f"⚠️ 피싱 사이트로 탐지됨 (확률: {prob:.2%})")
    else:
        print(f"✅ 정상 사이트로 판단됨 (확률: {prob:.2%})")

    print("의심스러운 특징:")
    if suspicious_features:
        for feat in suspicious_features:
            print(f" - {feat}")
    else:
        print(" - 없음 (모든 특성 양호)")
        
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("사용법: python3 analyze_url.py <URL>")
    else:
        analyze_url(sys.argv[1])
