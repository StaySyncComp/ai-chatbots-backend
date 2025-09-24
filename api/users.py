from tools.utils import send_request
import api.requestsApi as requestsApi


def fetch_all_users():
    """Fetch all users from the API."""
    organizationId = requestsApi.request_context.payload.organizationId
    response = send_request("get", f"users?organizationId={organizationId}")

    if response.status_code == 200:
        return {"users": response.json()}
    else:
        print(f"Error fetching users: {response.status_code}, {response.text}")
        return {
            "error": f"Failed to fetch users {response.text} {response.status_code}"
        }


def fetch_current_user_data():
    """Fetch the current user's data from the API."""
    response = send_request("get", "users/find")

    if response.status_code == 200:
        return {"users": response.json()}
    else:
        print(f"Error fetching users: {response.status_code}, {response.text}")
        return {
            "error": f"Failed to fetch users {response.text} {response.status_code}"
        }


def fetch_user_organization_role():
    organizationId = requestsApi.request_context.payload.organizationId
    """Returns detailed information about current user organizationRole Model"""
    response = send_request(
        "get",
        f"organizations/role?organizationId={organizationId}",
    )
    if response.status_code == 200:
        return {"organizationRole": response.json()}
    else:
        print(f"Error fetching organizations: {response.status_code}, {response.text}")
        return {
            "error": f"Failed to fetch organizations {response.text} {response.status_code}"
        }
