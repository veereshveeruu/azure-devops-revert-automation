import os
import requests
import base64


def update_work_item(work_item_id, revert_pr_number):

    organization = "veereshambavarapu222"
    project = "Project-1"

    pat = os.getenv("AZURE_DEVOPS_PAT")

    credentials = base64.b64encode(
        f":{pat}".encode()
    ).decode()

    headers = {
        "Authorization": f"Basic {credentials}",
        "Content-Type": "application/json-patch+json"
    }

    url = (
        f"https://dev.azure.com/"
        f"{organization}/{project}"
        f"/_apis/wit/workitems/{work_item_id}"
        f"?api-version=7.1"
    )

    payload = [
        {
            "op": "add",
            "path": "/fields/System.History",
            "value": f"Rollback PR Created: {revert_pr_number}"
        }
    ]

    response = requests.patch(
        url,
        headers=headers,
        json=payload
    )

    print("Update Status:", response.status_code)

    return response