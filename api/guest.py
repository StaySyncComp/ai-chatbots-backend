from tools.utils import send_request
import api.requestsApi as requestsApi


def fetch_call_guest_categories():
    id = requestsApi.request_context.payload.organizationId
    """Fetch call categories by organization ID."""
    print(f"Fetching call categories with an id of: {id}")
    response = send_request(
        "get",
        f"guest/list?organizationId={id}",
    )
    if response.status_code == 200:
        data = response.json()
        return {"call categories data": data, "count": len(data)}
    else:
        print(
            f"Error fetching call categories: {response.status_code}, {response.text}"
        )
        return {
            "error": f"Failed to fetch call categories {response.text} {response.status_code}"
        }


def fetch_guest_information():
    id = requestsApi.request_context.payload.organizationId
    """Fetch guest information by organization ID."""
    print(f"Fetching guest information with an id of: {id}")
    response = send_request(
        "get",
        f"guest?organizationId={id}",
    )
    if response.status_code == 200:
        data = response.json()
        print(data)
        return {"guest information data": data}
    else:
        print(
            f"Error fetching guest information: {response.status_code}, {response.text}"
        )
        return {
            "error": f"Failed to fetch guest information {response.text} {response.status_code}"
        }


def fetch_organization_guest():
    response = send_request(
        "get",
        f"guest/organization",
    )
    if response.status_code == 200:
        data = response.json()
        print(data)
        return {"guest information data": data}
    else:
        print(
            f"Error fetching guest information: {response.status_code}, {response.text}"
        )
        return {
            "error": f"Failed to fetch guest information {response.text} {response.status_code}"
        }


def create_guest_call(
    description,
    callCategoryId,
):
    """Create a new call."""
    print(f"creating calls with an callCategoryId of: {callCategoryId}")
    response = send_request(
        "post",
        f"guest/call",
        {
            "description": description,
            "callCategoryId": callCategoryId,
        },
    )
    if response.status_code == 200:
        return {"calls data": response.json()}
    else:
        print(f"Error fetching calls: {response.status_code}, {response.text}")
        return {
            "error": f"Failed to fetch calls {response.text} {response.status_code}"
        }
