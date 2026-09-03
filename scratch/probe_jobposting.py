import httpx

client = httpx.Client(follow_redirects=True, timeout=10.0, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

urls = [
    'https://applicants.bairesdev.com/api/JobPosting?JobPostingId=286773',
    'https://applicants.bairesdev.com/api/JobPosting?jobPostingId=286773',
    'https://applicants.bairesdev.com/api/JobPosting?id=286773',
    'https://applicants.bairesdev.com/api/JobPosting/286773',
    'https://applicants-pre.bairesdev.dev/api/JobPosting?JobPostingId=286773',
    'https://applicants.bairesdev.com/api/v1/JobPosting?JobPostingId=286773',
    'https://applicants.bairesdev.com/api/job-opportunity?id=286773',
    'https://talent.bairesdev.com/api/JobPosting?JobPostingId=286773',
]

for u in urls:
    try:
        r = client.get(u)
        print(u, '->', r.status_code)
        if r.status_code == 200:
            print('FOUND 200:', r.text[:1000])
    except Exception as e:
        print(u, '->', e)
