import os
import requests
import base64

organization = "veereshambavarapu222"
project = "Project-1"
pat = os.getenv("AZURE_DEVOPS_PAT")   # must match GitHub secret name

work_item_id = 7
import os

pat = os.getenv("AZURE_DEVOPS_PAT")

print("PAT Loaded:", pat is not None)

if pat:
    print("PAT Length:", len(pat))
else:
    print("PAT is None")
credentials = base64.b64encode(f":{pat}".encode()).decode()

headers = {
    "Authorization": f"Basic {credentials}",
    "Content-Type": "application/json"
}

url = f"https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/{work_item_id}?api-version=7.1"

response = requests.get(url, headers=headers)
print(response.status_code)
print(response.json())
