import json
import re
from pathlib import Path

content = Path(r"C:\Users\pierr\.gemini\antigravity\brain\6a210910-9008-4dfc-8b7f-e9f746d36717\.system_generated\steps\347\content.md").read_text(encoding="utf-8")

match = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', content)
if match:
    data = json.loads(match.group(1))
    props = data.get("props", {}).get("pageProps", {})
    # print all top keys in pageProps
    print("PageProps keys:", props.keys())
    job = props.get("job") or props.get("jobPosting") or props.get("initialJob") or props
    out_file = Path("scratch/sparq_job.json")
    out_file.write_text(json.dumps(props, indent=2), encoding="utf-8")
    print("Saved pageProps to scratch/sparq_job.json")
else:
    print("__NEXT_DATA__ not found")
