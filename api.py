
import requests
import random
import json

BASE_URL = 'https://10.5.180.217:443/helix-alm/api/v0/'

DEFAULT_TIMEOUT = 30  # seconds

def get_project_list(headers, timeout=DEFAULT_TIMEOUT):
    url = f"{BASE_URL}projects"
    try:
        response = requests.get(url=url, headers=headers, verify=False, timeout=timeout)
        response.raise_for_status()
        return {project['name']: project['uuid'] for project in response.json()['projects']}
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch projects: {str(e)}")

def get_test_cases_links(test_case_id, headers, uuid, timeout=DEFAULT_TIMEOUT):
    url = f"{BASE_URL}{uuid}/testCases/{test_case_id}/links"
    try:
        response = requests.get(url=url, headers=headers, verify=False, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch test cases: {str(e)}")

def add_requirement_link_to_test_case(ReqId, TestCaseId, headers, uuid, timeout=DEFAULT_TIMEOUT):
    data = {
        "linksData": [
            {
                "id": random.randint(0, 4294967295),
                "comment": "This is a list of linked related items",
                "linkDefinition": {"id": 2003, "name": "Requirement Tested By"},
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
    response = requests.post(url=url, headers=headers, data=json.dumps(data), verify=False, timeout=timeout)
    if response.status_code == 201:
        return response.json()
    else:
        raise Exception(f"Failed to add requirement link. Status Code: {response.status_code}")

def get_req_description(reqId, headers, uuid, *, session=None, timeout=DEFAULT_TIMEOUT):
    """Fetch a single requirement (Summary, Description, Discussion). Optionally reuse a requests.Session."""
    url = f"{BASE_URL}{uuid}/requirements/{reqId}?fields=Summary,Description,Discussion"
    try:
        sess = session or requests
        response = sess.get(url=url, headers=headers, verify=False, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch requirement {reqId}: {str(e)}")

def get_recordID(reqId, headers, uuid, timeout=DEFAULT_TIMEOUT):
    url = f"{BASE_URL}{uuid}/requirements/search"
    search_clause = (
        "("
        "'REQ / RE / TASK Type' = 'Software Requirement' and "
        f"'Tag' = 'SW-{str(reqId)}'"
        ") or ("
        "'REQ / RE / TASK Type' = 'Constant' and "
        f"'Tag' = 'CNST-{str(reqId)}'"
        ") or ("
        "'REQ / RE / TASK Type' = 'System Requirement' and "
        f"'Tag' = 'SYS-{str(reqId)}'"
        ") or ("
        "'REQ / RE / TASK Type' = 'Software Architecture Requirement' and "
        f"'Tag' = 'SWA-{str(reqId)}'"
        ") or ("
        "'REQ / RE / TASK Type' = 'System Architecture Requirement' and "
        f"'Tag' = 'SYSA-{str(reqId)}'"
        ")"
    )
    data = { "fields": ['linked Items'], "search": search_clause }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), verify=False, timeout=timeout)
        response.raise_for_status()
        reqs = response.json().get('requirements', [])
        if not reqs:
            raise Exception("No matching requirements found.")
        return reqs[0]['id']
    except requests.exceptions.RequestException as e:
        raise Exception(f"Something went wrong while getting requirements: {str(e)}")
