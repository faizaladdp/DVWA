import json, os
from github import Github

repo_name = os.getenv("GITHUB_REPOSITORY")
token = os.getenv("GITHUB_TOKEN")
g = Github(token)
repo = g.get_repo(repo_name)

report_path = "reports/dependency-check-report.json"
if not os.path.exists(report_path):
    print("❌ No dependency report found")
    exit(1)

with open(report_path) as f:
    data = json.load(f)

vulns = []
for dep in data.get("dependencies", []):
    for vuln in dep.get("vulnerabilities", []):
        vulns.append({
            "name": dep.get("fileName"),
            "cve": vuln.get("name"),
            "severity": vuln.get("severity"),
            "desc": vuln.get("description")
        })

if not vulns:
    print("✅ No vulnerabilities found")
    exit(0)

body = "### ⚠️ Vulnerabilities Found\n"
for v in vulns[:5]:
    body += f"- **{v['name']}** → {v['cve']} ({v['severity']})\n"

repo.create_issue(
    title=f"[AutoRemediate] {len(vulns)} Vulnerabilities Detected",
    body=body + "\nPlease review and fix or trigger dependency upgrade."
)

print("🟡 Issue created successfully.")
