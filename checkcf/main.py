"""Checks if a site is using Cloudflare"""

import requests

from rich import print

def check_headers(response: requests.Response) -> bool:
    """Check if the response headers indicate that the site is using Cloudflare."""""

    result = {
        'server': False,
        'ray': False,
        'cache': False
    }

    headers = [header.lower() for header in response.headers]

    if response.headers.get('server') == 'cloudflare':
        result['server'] = True

    if 'cf-ray' in headers:
        result['ray'] = True

    if 'cf-cache-status' in headers:
        result['cache'] = True

    return result

def check_cookies(response: requests.Response) -> bool:
    """Check if the response cookies indicate that the site is using Cloudflare."""

    result = {
        'session': False
    }

    if '__cf_bm' in response.cookies:
        result['session'] = True

    return result

def is_using_cloudflare(url: str) -> bool:
    """Check if a site is using Cloudflare by making a request to it and checking the
    response."""

    if not url.startswith('http'):
        url = f'http://{url}'

    response = requests.get(url, timeout=10)

    results = {
        'headers': check_headers(response),
        'cookie': check_cookies(response)
    }

    return results

def main():
    """Example"""

    while True:
        url = input('Enter a URL: ')
        print(f'Checking {url}...')
        results = is_using_cloudflare(url)
        print(results)

if __name__ == '__main__':
    main()
