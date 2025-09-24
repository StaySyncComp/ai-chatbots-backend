from tools.utils import send_request
import api.requestsApi as requestsApi


def fetch_areas():
    """Fetch areas by organization ID."""
    organizationId = requestsApi.request_context.payload.organizationId
    response = send_request(
        "get",
        f"areas?organizationId={organizationId}",
    )
    if response.status_code == 200:
        return {"areas data": response.json()}
    else:
        print(f"Error fetching areas: {response.status_code}, {response.text}")
        return {
            "error": f"Failed to fetch areas {response.text} {response.status_code}"
        }


def create_area(name, color):
    """Create a new area."""
    print(f"creating areas with an name of: {name}")
    organizationId = requestsApi.request_context.payload.organizationId
    response = send_request(
        "post",
        f"areas",
        {
            "organizationId": organizationId,
            "name": name,
            "color": color,
        },
    )
    if response.status_code == 201:
        return {"areas data": response.json()}
    else:
        print(f"Error fetching areas: {response.status_code}, {response.text}")
        return {
            "error": f"Failed to fetch areas {response.text} {response.status_code}"
        }


def update_area(id, name, color):
    """Update an existing area."""
    print(f"updating areas with an name of: {name}")
    organizationId = requestsApi.request_context.payload.organizationId
    response = send_request(
        "put",
        f"areas/{id}",
        {
            "organizationId": organizationId,
            "name": name,
            "color": color,
            "id": id,
        },
    )
    if response.status_code == 200:
        return {"areas data": response.json()}
    else:
        print(f"Error fetching areas: {response.status_code}, {response.text}")
        return {
            "error": f"Failed to fetch areas {response.text} {response.status_code}"
        }
