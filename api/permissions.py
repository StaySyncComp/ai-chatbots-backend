from tools.utils import send_request


# def fetch_all_permissions(id):
#     """Fetch all permissions from the API."""
#     print("Fetching permissions")
#     response = send_request("get", f"permissions?roleId={id}")
#     if response.status_code == 200:
#         return {"permissions": response.json()}
#     else:
#         print(f"Error fetching permissions: {response.status_code}, {response.text}")
#         return {"error": "Failed to fetch permissions"}


def update_permissions(id, action, scope, resource):
    """Update a specific role by ID."""
    print(f"Updating permissions with an id of: {id}")
    response = send_request(
        "put",
        f"permissions/{id}",
        {
            "action": action,
            "scope": scope,
            "resource": resource,
        },
    )
    if response.status_code == 200:
        return {"permissions data": response.json()}
    else:
        print(f"Error updating permissions: {response.status_code}, {response.text}")
        return {
            "error": f"Failed to update permissions {response.text} {response.status_code}"
        }
