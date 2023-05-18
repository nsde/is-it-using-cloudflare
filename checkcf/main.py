"""Checks if a site is using Cloudflare"""

import json
import requests

from rich import print
from concurrent.futures import ThreadPoolExecutor

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

def is_using_cloudflare(url: str) -> bool:
    """Check if a site is using Cloudflare by making a request to it and checking the
    response."""

    if not url.startswith('http'):
        url = f'http://{url}'

    response = requests.get(url, timeout=10)
    results = check_headers(response)

    return results

def bulk_check_single(url: str):
    """Wrapper for is_using_cloudflare that catches ConnectionErrors."""

    print(f'Checking {url}...')
    try:
        return is_using_cloudflare(url)
    except requests.exceptions.ConnectionError as err:
        print(f'[red]{url} failed: {err}[/red]]')
        return {
            'error': str(err)
        }

def bulk_check(file_path: str) -> None:
    """When given a list of URLs separated by newlines, this tool
checks if each one is using Cloudflare, and writes the results to
results.json"""

    with open(file_path, 'r', encoding='utf8') as file:
        lines = file.read().splitlines()

    results = {}
    urls = []

    for line in lines:
        url = line.strip()

        if not url:
            continue

        urls.append(url)

    with ThreadPoolExecutor(max_workers=100) as executor:
        for url, result in zip(urls, executor.map(bulk_check_single, urls)):
            results[url] = result

    with open('results.json', 'w', encoding='utf8') as file:
        json.dump(results, file, indent=4)

def main():
    """Example"""

    while True:
        url = input('Enter a URL: ')
        print(f'[blue]Checking {url}...[/blue]')

        try:
            results = is_using_cloudflare(url)
        except requests.exceptions.ConnectionError as err:
            print(f'[red]Error: {err}[/red]]')
            continue

        print(results)

if __name__ == '__main__':
    # main()

    bulk_check('urls.txt')

