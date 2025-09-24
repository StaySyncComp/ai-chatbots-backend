from tools.utils import send_request
import api.requestsApi as requestsApi


def fetch_guest_calls(id, locationId):
    """Fetch guest calls by organization ID."""
    print(f"Fetching guest calls with an id of: {id}")
    response = send_request(
        "get",
        f"calls?organizationId={id}&locationId={locationId}",
    )
    if response.status_code == 200:
        return {"guest calls data": response.json()}
    else:
        print(f"Error fetching guest calls: {response.status_code}, {response.text}")
        return {
            "error": f"Failed to fetch guest calls {response.text} {response.status_code}"
        }


def fetch_calls():
    """Fetch calls by organization ID."""
    print(f"Fetching calls")
    organization_id = requestsApi.request_context.payload.organizationId
    response = send_request(
        "get",
        f"calls?organizationId={organization_id}",
    )
    if response.status_code == 200:
        return {"calls data": response.json()}
    else:
        print(f"Error fetching calls: {response.status_code}, {response.text}")
        return {
            "error": f"Failed to fetch calls {response.text} {response.status_code}"
        }


def create_call(
    description,
    locationId,
    callCategoryId,
):
    """Create a new call."""
    organizationId = requestsApi.request_context.payload.organizationId
    print(f"creating calls with an callCategoryId of: {callCategoryId}")
    response = send_request(
        "post",
        f"calls",
        {
            "description": description,
            "locationId": locationId,
            "callCategoryId": callCategoryId,
            "organizationId": organizationId,
        },
    )
    if response.status_code == 200:
        return {"calls data": response.json()}
    else:
        print(f"Error fetching calls: {response.status_code}, {response.text}")
        return {
            "error": f"Failed to fetch calls {response.text} {response.status_code}"
        }


def update_call(
    title,
    description,
    locationId,
    departmentId,
    assignedToId,
    closedById,
    status,
    callCategoryId,
    organizationId,
):
    """Update an existing call."""
    print(f"updating calls with an title of: {title}")
    response = send_request(
        "put",
        f"calls/{title}",
        {
            "title": title,
            "description": description,
            "locationId": locationId,
            "departmentId": departmentId,
            "assignedToId": assignedToId,
            "closedById": closedById,
            "status": status,
            "callCategoryId": callCategoryId,
            "organizationId": organizationId,
        },
    )
    if response.status_code == 200:
        return {"call data": response.json()}
    else:
        print(f"Error updating call: {response.status_code}, {response.text}")
        return {
            "error": f"Failed to updating call {response.text} {response.status_code}"
        }


def upsert_calls(calls):
    print("Upserting calls")
    response = send_request("post", "calls/upsert", calls)
    if response.status_code == 200:
        return {"calls data": response.json()}
    else:
        print(f"Error upserting calls: {response.status_code}, {response.text}")
        return {
            "error": f"Failed to upserting calls {response.text} {response.status_code}"
        }
