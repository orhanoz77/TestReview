import requests
import random
import json
from PyQt6.QtWidgets import QMessageBox

BASE_URL = 'https://10.5.180.217:443/helix-alm/api/v0/'

def get_project_list(headers):
    url = f"{BASE_URL}projects"
    try:
        response = requests.get(url=url, headers=headers, verify=False)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx, 5xx)
        return {project['name']: project['uuid'] for project in response.json()['projects']}
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch projects: {str(e)}")

def get_test_cases_links(test_case_id, headers, uuid):
    url = f"{BASE_URL}{uuid}/testCases/{test_case_id}/links"
    try:
        response = requests.get(url=url, headers=headers, verify=False)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch test cases: {str(e)}")

def add_requirement_link_to_test_case(ReqId, TestCaseId,headers, uuid):
    """
    Adds a requirement link to a test case in Helix ALM.
    """
    data = {
        "linksData": [
            {
                "id": random.randint(0, 4294967295),
                "comment": "This is a list of linked related items",
                "linkDefinition": {
                    "id": 2003,
                    "name": "Requirement Tested By"
                },
                "type": "parentChildren",
                "parentChildren": {
                    "parent": {
                        "itemID": ReqId,
                        "itemType": "requirements",
                        "isSuspect": False,
                        "link": f"{BASE_URL}{{{uuid}}}/requirements/{str(ReqId)}"
                    },
                    "children": [
                        {
                            "itemID": TestCaseId,
                            "itemType": "testCases",
                            "isSuspect": False,
                            "link": f"{BASE_URL}{{{uuid}}}/testcases/{str(TestCaseId)}"
                        }
                    ]
                }
            }
        ]
    }

    url = f"{BASE_URL}{uuid}/testCases/{str(TestCaseId)}/links"
    json_data = json.dumps(data)
    response = requests.post(url=url, headers=headers, data=json_data, verify=False)

    if response.status_code == 201:
        print("Operation successful.")
        return response.json()
    else:
        raise Exception(f"Failed to add requirement link. Status Code: {response.status_code}")

def get_req_description(reqId, headers, uuid):
    # print("get_req_description IN")
    # url = f"{BASE_URL}{uuid}/requirements/{reqId}"
    url = f"{BASE_URL}{uuid}/requirements/{reqId}?fields=Summary,Description,Discussion"

    try:
        response = requests.get(url=url, headers=headers, verify=False)
        # print(response.json())
        response.raise_for_status()
        # print("get_req_description OUT")
        return response.json()

    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch test cases: {str(e)}")


#Yusuf
"""
def get_recordID(reqId, headers, uuid):
    url = f"{BASE_URL}{uuid}/requirements/search"
    data = {"fields": ['ASIL', 'linked Items'],
            "search": f"'REQ / RE / TASK Type' = 'Software Requirement' and 'Tag' = 'SW-{str(reqId)}' or "  }
    data = json.dumps(data)
    response = requests.post(url, headers=headers, data=data, verify=False)
    if response.status_code == 200:
        recordID = response.json()['requirements'][0]['id']
        return recordID
    else:
        raise Exception(f"Something went wrong while getting requirements!  -- Status Code: "
                        f"{response.status_code}")

"""

def get_recordID(reqId, headers, uuid):
    url = f"{BASE_URL}{uuid}/requirements/search"
    search_clause = (
        "("
        "'REQ / RE / TASK Type' = 'Software Requirement' and "
        f"'Tag' = 'SW-{str(reqId)}'"
        ") or ("
        "'REQ / RE / TASK Type' = 'Constant' and "
        f"'Tag' = 'CNST-{str(reqId)}'"
        ")"
    )
    data = {
        "fields": ['ASIL', 'linked Items'],
        "search": search_clause
    }
    response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
    print(response.json())

    if response.status_code == 200:
        reqs = response.json().get('requirements', [])
        print(reqs[0]['id'])
        if not reqs:
            raise Exception("No matching requirements found.")
        return reqs[0]['id']
    else:
        raise Exception(
            f"Something went wrong while getting requirements!  -- Status Code: "
            f"{response.status_code}"
        )