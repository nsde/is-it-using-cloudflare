# is-it-using-cloudflare
Checks if a website uses Cloudflare or not using multiple methods.

It's as simple as that!
```bash
$ python checkflare

 Enter a URL: example.com
 Checking example.com...
 {'server': False, 'ray': False, 'cache': False}
```

## Bulk Check

1. Add a list of URLs to `urls.txt`
2. Run `python checkflare urls.txt`
3. Don't worry, errors will be ignored.
4. Check the `results.json`.
5. Profit!
```bash
...
 "freegpt.one": {
     "server": true,
     "ray": true,
     "cache": false
 },
...
 "aitianhu.com": {
     "error": "HTTPConnectionPool(host='aitianhu.com', port=80): Max retries exceeded with url: / (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x0000019AB773DED0>: Failed to establish a new connection: [Errno 11001] getaddrinfo failed'))"
 },
...
```

