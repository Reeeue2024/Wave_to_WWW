from urllib.parse import urlparse, unquote
import re
import math
from collections import Counter

def shannon_entropy(s):
    p, lns = Counter(s), float(len(s))
    return -sum(count / lns * math.log2(count / lns) for count in p.values())

def extract_features(url):
    parsed = urlparse(url)
    domain = parsed.netloc
    path = parsed.path
    query = parsed.query
    full_url = url
    decoded_url = unquote(url)
    domain_parts = domain.split('.')

    # suspicious words
    suspicious_keywords = ['login', 'secure', 'verify', 'update', 'account', 'bank']

    # 특수문자 수
    special_chars = "!#$%&()*+,-./:;<=>?@[\]^_`{|}~"
    count_special_chars = sum(c in special_chars for c in full_url)

    # URL 길이 구간화
    url_length = len(full_url)
    if url_length < 50:
        url_length_level = 0
    elif url_length < 100:
        url_length_level = 1
    else:
        url_length_level = 2

    # 경로 분석
    segments = [seg for seg in path.strip('/').split('/') if seg]
    file_path_depth = len(segments)
    avg_segment_len = round(sum(len(seg) for seg in segments) / (file_path_depth + 1e-5), 2)
    num_numeric_segments = sum(bool(re.fullmatch(r'\d+', seg)) for seg in segments)

    return {
        # 구조 기반으로 분해된 경로 피처
        'file_path_depth': file_path_depth,
        'avg_path_segment_len': avg_segment_len,
        'num_numeric_segments': num_numeric_segments,

        'url_length_level': url_length_level,
        'count_special_characters': count_special_chars,
        'len_sub_domain': sum(len(part) for part in domain_parts[:-2]) if len(domain_parts) > 2 else 0,
        'value_entropy_url': round(shannon_entropy(full_url), 4),
        'ratio_alpha_numeric': round(
            sum(c.isalpha() for c in full_url) / (sum(c.isalnum() for c in full_url) + 1e-5), 4),
        'domain_complexity': len(domain) + round(shannon_entropy(domain), 4),
        'is_ip': int(bool(re.fullmatch(r'(\d{1,3}\.){3}\d{1,3}', domain))),
        'is_ip_and_long': int(url_length > 100 and bool(re.fullmatch(r'(\d{1,3}\.){3}\d{1,3}', domain))),
        'has_suspicious_word': int(any(word in full_url.lower() for word in suspicious_keywords)),
        'path_entropy': round(shannon_entropy(path), 4),
        'query_length_category': (
            0 if len(query) == 0 else
            1 if len(query) < 50 else
            2
        )
    }
