import httpx
import re
import json

client = httpx.Client(follow_redirects=True, timeout=10.0, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

r_env = client.get('https://applicants.bairesdev.com/assets/env.js')
print('=== ENV.JS ===')
print(r_env.text)

r_main = client.get('https://applicants.bairesdev.com/main.415d083e7c553898.js')
if r_main.status_code == 200:
    print('=== MATCHES IN MAIN.JS ===')
    matches = set(re.findall(r'https?://[a-zA-Z0-9.-]+\.bairesdev\.com[^\s"\'`]*', r_main.text))
    for m in sorted(matches):
        print('Found domain match:', m)
