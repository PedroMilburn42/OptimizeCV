import httpx
import json

client = httpx.Client(follow_redirects=True, timeout=10.0, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
r = client.get('https://applicants.bairesdev.com/api/JobPosting?JobPostingId=286773')
data = r.json()
with open('scratch/bairesdev_job.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print('Title:', data.get('title'))
print('EmploymentType:', data.get('employmentType'))
print('HiringOrganization:', data.get('hiringOrganization'))
print('Description length:', len(data.get('description', '')))
