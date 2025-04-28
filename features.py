# features.py

import re
from urllib.parse import urlparse, parse_qs

def extract_features(url):
    parsed = urlparse(url)
    protocol = parsed.scheme
    domain = parsed.netloc
    path = parsed.path
    query = parsed.query

    # Các đặc trưng liên quan đến URL và domain
    len_url = len(url)
    len_domain = len(domain)
    len_path = len(path)
    num_dots = domain.count('.')
    num_slashes = path.count('/')

    # Query params
    query_params = parse_qs(query)
    num_query_params = len(query_params)

    # Kiểm tra IP trong domain
    ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    has_ip = 1 if re.search(ip_pattern, domain) else 0

    # Kiểm tra https
    is_https = 1 if protocol == 'https' else 0

    # Từ khóa thường thấy trong URL phishing
    keywords = ['login', 'signin', 'account', 'secure', 'update', 'verify', 'bank',
                'password', 'credit', 'card', 'confirm', 'suspend', 'alert', 'service',
                'access', 'identity', 'online', 'webscr', 'cmd', 'ebayisapi']
    has_keyword = 1 if any(keyword in url.lower() for keyword in keywords) else 0

    # Ký tự đặc biệt trong URL
    special_chars = ['-', '@', '%', '&', '=', '?', '_', '~']
    num_special_chars = sum(url.count(c) for c in special_chars)

    return {
        'len_url': len_url,
        'len_domain': len_domain,
        'len_path': len_path,
        'num_dots': num_dots,
        'num_slashes': num_slashes,
        'num_query_params': num_query_params,
        'has_ip': has_ip,
        'is_https': is_https,
        'has_keyword': has_keyword,
        'num_special_chars': num_special_chars
    }
