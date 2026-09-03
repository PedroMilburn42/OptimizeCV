import httpx
import re
import json

client = httpx.Client(follow_redirects=True, timeout=10.0, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

r_main = client.get('https://applicants.bairesdev.com/main.415d083e7c553898.js')
if r_main.status_code == 200:
    api_calls = set(re.findall(r'/api/[a-zA-Z0-9_/-]+', r_main.text))
    print('API calls in main.js:', sorted(api_calls))

# Let us also test common endpoints for job 286773
endpoints = [
    'https://applicants.bairesdev.com/api/job-opportunity/286773',
    'https://applicants.bairesdev.com/api/job/286773',
    'https://applicants.bairesdev.com/api/jobs/286773',
    'https://applicants.bairesdev.com/api/job-posting/286773',
    'https://applicants.bairesdev.com/api/job/1/286773',
    'https://applicants.bairesdev.com/api/v1/job/286773',
    'https://applicants.bairesdev.com/api/jobOpportunity/286773',
    'https://applicants.bairesdev.com/api/JobOpportunity/286773',
    'https://applicants.bairesdev.com/api/Job/286773',
    'https://applicants.bairesdev.com/api/Jobs/286773',
]

for ep in endpoints:
    res = client.get(ep)
    print(ep, '-> status:', res.status_code)
    if res.status_code == 200:
        print('RESPONSE:', res.text[:500])
