import json
from github import Github

token = os.getenv("GITHUB_TOKEN")
repo_name = os.getenv("GITHUB_REPOSITORY")
vuln_file = "results/vulnerabilities.json"  # example file

g = Github(auth=github.Auth.Token(token))
repo = g.get_repo(repo_name)

with open(vuln_file, "r") as f:
    data = json.load(f)

vulnerabilities = data.get("vulnerabilities", [])

if not isinstance(vulnerabilities, list):
    print("⚠️ vulnerabilities data not in expected format")
    exit(1)

print(f"⚠️ {len(vulnerabilities)} vulnerabilities found. Preparing auto-fix...")

for item in vulnerabilities:
    # Safely handle both dicts and strings
    if isinstance(item, dict):
        name = item.get("name", "Unknown")
        severity = item.get("severity", "N/A")
    else:
        name = str(item)
        severity = "N/A"

    print(f"🔧 Processing: {name} (Severity: {severity})")
    # Do your fix logic here (e.g., create issue, commit fix, etc.)
