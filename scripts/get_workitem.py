import os
import requests
import base64

#Get Azure DevOps User Story Details
organization = "veereshambavarapu222"
project = "Project-1"
pat = os.getenv("AZURE_DEVOPS_PAT")   # must match GitHub secret name

work_item_id = input("Enter Work Item ID: ")
import os

pat = os.getenv("AZURE_DEVOPS_PAT")

credentials = base64.b64encode(f":{pat}".encode()).decode()

headers = {
    "Authorization": f"Basic {credentials}",
    "Content-Type": "application/json"
}

url = f"https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/{work_item_id}?api-version=7.1"

response = requests.get(url, headers=headers)
print(response.status_code)
print(response.json())
