from tools.utils import send_request
import api.requestsApi as requestsApi


def fetch_departments():
    """Fetch departments by organization ID."""
    id = requestsApi.request_context.payload.organizationId
    print(f"Fetching departments with an id of: {id}")
    response = send_request(
        "get", f"departments?organizationId={id}", {"organizationId": id}
    )
    if response.status_code == 200:
        return {"departments data": response.json()}
    else:
        print(f"Error fetching departments: {response.status_code}, {response.text}")
        return {
            "error": f"Failed to fetch departments {response.text} {response.status_code}"
        }


def create_department(name):
    """Create a new department."""
    organization_id = requestsApi.request_context.payload.organizationId
    print(f"creating departments with an name of: {name}")
    response = send_request(
        "post", f"departments", {"organizationId": organization_id, "name": name}
    )
    if response.status_code == 201:
        return {"departments data": response.json()}
    else:
        print(f"Error creating department: {response.status_code}, {response.text}")
        return {
            "error": f"Failed to create department {response.text} {response.status_code}"
        }


def update_department(department_id, name):
    """Update an existing department."""
    print(f"creating departments with an name of: {name}")
    organization_id = requestsApi.request_context.payload.organizationId
    response = send_request(
        "put",
        f"departments/{department_id}",
        {"organizationId": organization_id, "name": name},
    )
    if response.status_code == 200:
        return {"departments data": response.json()}
    else:
        print(f"Error update department: {response.status_code}, {response.text}")
        return {
            "error": f"Failed to update department {response.text} {response.status_code}"
        }
