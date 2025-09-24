from tools.utils import send_request
import api.requestsApi as requestsApi


def fetch_all_roles():
    """Fetch all roles from the API."""
    print("Fetching roles")
    organizationId = requestsApi.request_context.payload.organizationId
    response = send_request("get", f"roles?organizationId={organizationId}")
    if response.status_code == 200:
        return {"roles": response.json()}
    else:
        print(f"Error fetching roles: {response.status_code}, {response.text}")
        return {
            "error": f"Failed to fetch roles {response.text} {response.status_code}"
        }


def fetch_role(id):
    """Fetch a specific role by ID."""
    print(f"Fetching role with an id of: {id}")
    organizationId = requestsApi.request_context.payload.organizationId
    response = send_request("get", f"roles/{id}?organizationId={organizationId}")
    if response.status_code == 200:
        print(response.json())
        return {"role data": response.json()}
    else:
        print(f"Error fetching roles: {response.status_code}, {response.text}")
        return {
            "error": f"Failed to fetch roles {response.text} {response.status_code}"
        }


def update_role(id, name):
    """Update a specific role by ID."""
    print(f"Updating role with an id of: {id}")
    response = send_request("put", f"roles/{id}", {"name": name})
    if response.status_code == 200:
        return {"role data": response.json()}
    else:
        print(f"Error updating roles: {response.status_code}, {response.text}")
        return {
            "error": f"Failed to update roles {response.text} {response.status_code}"
        }


def create_role(name):
    """Create a new role."""
    print(f"Creating role with name: {name}")
    organizationId = requestsApi.request_context.payload.organizationId

    response = send_request(
        "post", "roles", {"name": name, "organizationId": organizationId}
    )
    if response.status_code == 201:
        return {"role data": response.json()}
    else:
        print(f"Error creating roles: {response.status_code}, {response.text}")
        return {
            "error": f"Failed to create roles {response.text} {response.status_code}"
        }
