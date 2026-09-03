import httpx

client = httpx.Client(follow_redirects=True, timeout=10.0, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

res = client.get('https://applicants.bairesdev.com/api/job/1/286773')
print('status:', res.status_code)
print('headers:', dict(res.headers))
print('body:', res.text)

res2 = client.get('https://applicants.bairesdev.com/assets/scripts/struct-job-postings.js')
print('struct-job-postings.js:', res2.text[:1000])
