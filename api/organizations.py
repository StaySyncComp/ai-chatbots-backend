from tools.utils import send_request
import api.requestsApi as requestsApi
from supabaseApi import process_supabase_files
from tools.geminiClient import client


def fetch_all_organizations():
    """Fetch all organizations from the API."""
    print("Fetching organizations")
    response = send_request("get", "organizations")
    if response.status_code == 200:
        return {"organizations": response.json()}
    else:
        print(f"Error fetching organizations: {response.status_code}, {response.text}")
        return {
            "error": f"Failed to fetch organizations {response.text} {response.status_code}"
        }


def fetch_organization():
    """Fetch a specific organization by ID."""
    organizationId = requestsApi.request_context.payload.organizationId
    print(f"Fetching organization with an id of: {organizationId}")
    response = send_request(
        "get",
        f"organizations/find?organizationId={organizationId}",
        {"organizationId": organizationId},
    )
    if response.status_code == 200:
        return {"organization data": response.json()}
    else:
        print(f"Error fetching organizations: {response.status_code}, {response.text}")
        return {
            "error": f"Failed to fetch organizations {response.text} {response.status_code}"
        }


def fetch_organization_ai_context():
    id = requestsApi.request_context.payload.organizationId
    """Fetch a specific organization by ID."""
    print(f"Fetching organization with an id of: {id}")
    response = send_request(
        "get", f"ai/context?organizationId={id}", {"organizationId": id}
    )
    if response.status_code == 200:
        data = response.json()
        # if data["fileUrls"]:
        #    data = process_supabase_files(
        #             data["fileUrls"], gemini_client=client, delete_files=False
        #         )
        return data
    else:
        print(f"Error fetching organizations: {response.status_code}, {response.text}")
        return {
            "error": f"Failed to fetch organizations {response.text} {response.status_code}"
        }


def get_organization_id():
    return requestsApi.request_context.body["organizationId"]
